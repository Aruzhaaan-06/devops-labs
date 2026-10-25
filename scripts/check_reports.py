"""PDF есептерінің пішімін, мәтінін және суреттерін тексеру."""
from pathlib import Path
from html import unescape
import argparse, hashlib, io, json, re, sys
import pdfplumber
from pypdf import PdfReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def compact(value): return re.sub(r'\s+','',value).replace('\xad','')
def plain(value): return unescape(re.sub('<[^>]+>','',value)).replace('\xa0',' ')
def paragraphs(value):
    if isinstance(value,dict):
        if value.get('type') in ['paragraph','heading','code'] and value.get('originalStyle') not in ['Title','TitleRu','CoverRu','KickerRu']:
            yield value
        for child in value.values():
            if isinstance(child,(dict,list)):yield from paragraphs(child)
    elif isinstance(value,list):
        for child in value: yield from paragraphs(child)

def inspect(path,root,strict):
    problems=[];warnings=[];reader=PdfReader(path)
    if reader.is_encrypted: problems.append('PDF шифрланған')
    total=len(reader.pages);bounds=[];blanks=[];bad_pages=[];number_errors=[];font_names=set();sizes=set();nonembedded=[]
    alltext=[];stream_text=[];image_hashes=set();body14=0
    for i,page in enumerate(reader.pages):
        for name,fontref in page.get('/Resources',{}).get('/Font',{}).items():
            font=fontref.get_object();base=str(font.get('/BaseFont',''));font_names.add(base)
            if base in ['/Helvetica','/Times-Roman']:continue # ReportLab's unused default resource has no drawn glyphs.
            descriptor=font.get('/FontDescriptor')
            if descriptor and not any(k in descriptor.get_object() for k in ['/FontFile','/FontFile2','/FontFile3']):nonembedded.append(base)
        extracted=page.extract_text() or ''
        if i>0:extracted=re.sub(r'^\s*'+str(i+1)+r'\s*\n','',extracted,count=1)
        stream_text.append(extracted)
        for ref in page.get('/Resources',{}).get('/XObject',{}).values():
            obj=ref.get_object()
            if obj.get('/Subtype')!='/Image':continue
            filters=str(obj.get('/Filter',''));raw=obj.get_data()
            if '/DCTDecode' in filters:
                # pypdf's convenience image export can re-encode JPEG; inspect original DCT bytes instead.
                img=Image.open(io.BytesIO(raw)).convert('RGB')
            elif obj.get('/ColorSpace')=='/DeviceRGB':
                img=Image.frombytes('RGB',(obj['/Width'],obj['/Height']),raw)
            else:continue
            image_hashes.add(hashlib.sha256(img.tobytes()).hexdigest())
    with pdfplumber.open(path) as pdf:
        for i,page in enumerate(pdf.pages):
            if abs(page.width-595.276)>1 or abs(page.height-841.89)>1:bad_pages.append(i+1)
            text=page.extract_text(x_tolerance=2) or '';alltext.append(text)
            if len(re.sub(r'\s','',text))<12:blanks.append(i+1)
            chars=page.chars
            sizes.update(round(c['size'],2) for c in chars)
            body14+=sum(abs(c['size']-14)<.1 and 'Times' in c['fontname'] for c in chars)
            for c in chars:
                if c['top']>page.height-45:continue
                if c['x0']<30*72/25.4-1.5 or c['x1']>page.width-15*72/25.4+1.5 or c['top']<20*72/25.4-2 or c['bottom']>page.height-20*72/25.4+2:
                    bounds.append({'page':i+1,'text':c['text'],'x0':round(c['x0'],2),'x1':round(c['x1'],2),'top':round(c['top'],2),'bottom':round(c['bottom'],2)})
            footer=[w for w in page.extract_words() if w['top']>page.height-42]
            if i==0:
                if footer:number_errors.append(1)
            elif not any(w['text']==str(i+1) and abs((w['x0']+w['x1'])/2-page.width/2)<2 for w in footer):number_errors.append(i+1)
    text='\n'.join(alltext);flat=compact('\n'.join(stream_text))
    if blanks:problems.append('Бос беттер: '+str(blanks))
    if bad_pages:problems.append('A4 емес беттер: '+str(bad_pages))
    if '\ufffd' in text or '\u25a0' in text:problems.append('Ауыстырылған немесе қара шаршы таңбалар бар')
    if strict:
        if bounds:problems.append('Мәтін шекарадан шыққан: '+str(len(bounds))+' таңба')
        if number_errors:problems.append('Бет нөмірі/орны: '+str(number_errors))
        if nonembedded:problems.append('Қаріп енгізілмеген: '+str(sorted(set(nonembedded))))
        if not body14:problems.append('14 pt Times New Roman мәтіні табылмады')
        required=['1 Жұмыстың мақсаты','3 Жұмыстың орындалу барысы','4 Жұмыс нәтижелері','5 Талдау','6 Қорытынды','7 Пайдаланылған әдебиеттер тізімі'] if path.name.startswith('lab') else ['1 Жұмыстың мақсаты','2 Орындау барысы','3 Жұмыс нәтижелері','4 Талдау','5 Қорытынды','6 Пайдаланылған әдебиеттер тізімі']
        for section in required:
            if compact(section) not in flat:problems.append('Бөлім жоқ: '+section)
        if path.name.startswith('lab') and compact('2 Теориялық мәліметтер') not in flat:problems.append('Теория бөлімі жоқ')
        for token in ['Д. Серікбаев','Түсіпханқызы','25-ИСТК-2о','2025-2026']:
            if compact(token) not in flat:problems.append('Титул дерегі жоқ: '+token)
        source=root/'reports/source'/(path.stem+'.json')
        if not source.exists():problems.append('Өңделетін бастапқы файл жоқ')
        else:
            data=json.loads(source.read_text(encoding='utf-8'));missing=[]
            for node in paragraphs(data['blocks']):
                snippet=node['text'] if node['type']=='code' and not node.get('originalStyle') else plain(node['text']);snippet=re.sub(r'^\d+(?:\.\d+)*\.\s+','',snippet) if node['type']=='heading' else snippet
                snippet=re.sub(r'^\d+-сурет[.\s:-]*','',snippet)
                normalized=compact(snippet)
                if len(normalized)>25 and normalized not in flat:missing.append(snippet[:130])
            if missing:problems.append('Мазмұн салыстыруында табылмаған блоктар: '+str(len(missing)))
            image_nodes=[b for b in data['blocks'] if b['type']=='image']
            absent_images=[]
            for node in image_nodes:
                img=Image.open(root/node['path']).convert('RGB');sha=hashlib.sha256(img.tobytes()).hexdigest()
                if sha not in image_hashes:absent_images.append(node['path'])
            if absent_images:problems.append('PDF ішінде түпнұсқа пиксельдері табылмаған сурет: '+str(absent_images))
            warnings.append('Скриншоттың ішкі мәтінін толық оқу үшін түпнұсқа сілтемесін пайдалану қажет болуы мүмкін') if image_nodes else None
    else:missing=[]
    return {'file':path.name,'pages':total,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'a4':not bad_pages,'fontResources':sorted(font_names),'fontSizes':sorted(sizes),'body14Characters':body14,'boundsViolations':bounds[:30],'pageNumberErrors':number_errors,'blankPages':blanks,'sourceTextMissing':missing[:20],'problems':problems,'warnings':warnings,'automaticPass':not problems,'humanChecks':['Қазақ тілінің толық филологиялық сараптамасы','Әдістеменің оқытушы тарапынан қабылдануы','Суреттердің оқу ыңғайлылығы және жалпы композиция']}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--directory',type=Path,default=ROOT/'reports');parser.add_argument('--output',type=Path,default=ROOT/'reports/quality-check.json');parser.add_argument('--baseline',action='store_true');args=parser.parse_args()
    paths=sorted(args.directory.glob('*.pdf'));rows=[]
    for path in paths:
        try:rows.append(inspect(path,ROOT,not args.baseline))
        except Exception as error:rows.append({'file':path.name,'automaticPass':False,'problems':[str(error)]})
    result={'scope':'PDF пішімі, мәтін және суреттер','pdfCount':len(rows),'labReportCount':sum(r['file'].startswith('lab') for r in rows),'totalPages':sum(r.get('pages',0) for r in rows),'passed':sum(r['automaticPass'] for r in rows),'failed':sum(not r['automaticPass'] for r in rows),'reports':rows}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['pdfCount','labReportCount','totalPages','passed','failed']},ensure_ascii=True))
    for row in rows:
        if row['problems']: print(row['file'],json.dumps(row['problems'],ensure_ascii=True))
    sys.exit(bool(result['failed']))

if __name__=='__main__':main()
