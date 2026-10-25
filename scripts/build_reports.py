"""JSON бастапқы файлдарынан академиялық PDF есептерін құру. Желіге шықпайды."""
from pathlib import Path
from html import escape, unescape
import argparse, hashlib, json, re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, Image, Spacer, PageBreak, KeepTogether, Flowable, CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reports/source'
CAT = json.loads((SOURCE/'catalog.json').read_text(encoding='utf-8'))
LEFT, RIGHT, TOP, BOTTOM = 30*mm, 15*mm, 20*mm, 20*mm
WIDTH, HEIGHT = A4[0]-LEFT-RIGHT, A4[1]-TOP-BOTTOM
PUBLIC = 'https://github.com/Aruzhaaan-06/devops-labs/blob/main/'

def setup_fonts(font_dir):
    for name, filename in [('Times','times.ttf'),('Times-Bold','timesbd.ttf'),('Times-Italic','timesi.ttf'),('Mono','consola.ttf')]:
        path = font_dir/filename
        if not path.is_file(): raise FileNotFoundError(f'Қаріп табылмады: {path}. --font-dir параметрін қолданыңыз.')
        pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('Times',normal='Times',bold='Times-Bold',italic='Times-Italic',boldItalic='Times-Bold')
    for name in ['Times','Times-Bold','Mono']:
        assert all(ord(c) in pdfmetrics.getFont(name).face.charToGlyph for c in 'ӘәҒғҚқҢңӨөҰұҮүҺһІі')

BODY=ParagraphStyle('AcademicBody',fontName='Times',fontSize=14,leading=21,firstLineIndent=12.5*mm,rightIndent=4,alignment=TA_JUSTIFY,spaceAfter=7,textColor=colors.black,splitLongWords=True)
HEADING=ParagraphStyle('AcademicHeading',parent=BODY,fontName='Times-Bold',firstLineIndent=0,fontSize=14,leading=21,alignment=TA_LEFT,spaceBefore=14,spaceAfter=10,keepWithNext=True)
SUB=ParagraphStyle('AcademicSubheading',parent=HEADING,spaceBefore=10,spaceAfter=7)
CENTER=ParagraphStyle('AcademicCenter',parent=BODY,alignment=TA_CENTER,firstLineIndent=0,spaceAfter=10)
CELL=ParagraphStyle('AcademicCell',parent=BODY,fontSize=12,leading=15,firstLineIndent=0,alignment=TA_LEFT,spaceAfter=0)
CODE=ParagraphStyle('AcademicCode',fontName='Mono',fontSize=10,leading=13,firstLineIndent=0,spaceAfter=0,alignment=TA_LEFT,splitLongWords=True)
CAPTION=ParagraphStyle('AcademicCaption',parent=BODY,fontSize=12,leading=16,firstLineIndent=0,alignment=TA_CENTER,spaceBefore=6,spaceAfter=10)
LABEL=ParagraphStyle('AcademicLabel',parent=CAPTION,keepWithNext=True)
REF=ParagraphStyle('AcademicReference',parent=BODY,firstLineIndent=0,alignment=TA_LEFT,spaceAfter=8,wordWrap='CJK')

def clean_markup(text):
    text=re.sub(r'</?font\b[^>]*>','',text)
    text=re.sub(r' color="[^"]*"',' color="#000000"',text)
    return text

def p(text, style=BODY): return Paragraph(clean_markup(text),style)
def plain(text): return unescape(re.sub('<[^>]+>','',text)).replace('\xa0',' ')

class ReportDoc(BaseDocTemplate):
    def __init__(self,path,meta):
        super().__init__(str(path),pagesize=A4,leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM,
            title=meta['title'],author=CAT['author'],subject='DevOps; 2025-2026; қазақша академиялық есеп')
        frame=Frame(LEFT,BOTTOM,WIDTH,HEIGHT,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='academic',frames=[frame],onPage=self.footer))
    def footer(self,canvas,doc):
        if doc.page>1:
            canvas.saveState();canvas.setFont('Times',12);canvas.drawCentredString(A4[0]/2,10*mm,str(doc.page));canvas.restoreState()
    def afterFlowable(self,flow):
        if isinstance(flow,Paragraph) and flow.style.name=='AcademicHeading':
            self.notify('TOCEntry',(0,flow.getPlainText(),self.page))

class Cover(Flowable):
    def __init__(self,meta):
        super().__init__();self.width=WIDTH;self.height=HEIGHT;self.meta=meta
    def draw(self):
        def at(text,y,style=CENTER):
            para=p(text,style);_,height=para.wrap(WIDTH,HEIGHT);para.drawOn(self.canv,0,y-height)
        at(CAT['institution'],HEIGHT-8*mm)
        at('«'+CAT['discipline']+'» пәні',HEIGHT-30*mm)
        number=self.meta['number'];parts=number.split('.')
        label='ЗЕРТХАНАЛЫҚ ЖҰМЫС № '+parts[0]
        if len(parts)>1: label+=', '+'.'.join(parts[1:])+'-бөлім'
        if number=='3.1-3.2':label='ЗЕРТХАНАЛЫҚ ЖҰМЫС № 3, 1-2-бөлімдер'
        if self.meta['kind']!='lab':label='ҚОРЫТЫНДЫ ЕСЕП'
        at('<b>'+label+'</b>',HEIGHT-83*mm)
        at(self.meta['title'],HEIGHT-102*mm)
        at('Орындаған: '+CAT['author'],HEIGHT-150*mm,REF)
        at('Тобы: '+CAT['group'],HEIGHT-166*mm,REF)
        at('Оқу жылы: '+CAT['academicYear'],HEIGHT-182*mm,REF)
        at(CAT['city']+' - '+CAT['publicationYear'],12*mm)

def code_block(text,markup=False):
    # Soft visual wraps do not change the executable text retained in the JSON source.
    text=plain(text) if markup else text
    return [p(escape(line).replace(' ','&nbsp;') or '&nbsp;',CODE) for line in text.splitlines()]

def render_nodes(nodes,stats):
    result=[];skip=set()
    for i,node in enumerate(nodes):
        if i in skip: continue
        kind=node['type']
        if kind=='originalPageBreak': continue
        if kind=='heading':
            text=plain(node['text'])
            if node.get('originalStyle') in ['Title','TitleRu','CoverRu','KickerRu']: continue
            stats['sub']+=1
            text=re.sub(r'^\d+(?:\.\d+)*\.\s+','',text)
            needed=110
            if i+1<len(nodes) and nodes[i+1]['type']=='code':
                next_node=nodes[i+1];lines=code_block(next_node['text'],bool(next_node.get('originalStyle')))
                if len(lines)<=18:needed=70+sum(line.wrap(WIDTH,HEIGHT)[1] for line in lines)
            result.append(CondPageBreak(min(needed,HEIGHT-1)))
            result.append(p(f"{stats.get('sectionPrefix','3')}.{stats['sub']} {escape(text)}",SUB))
        elif kind=='paragraph':
            if node.get('originalStyle') in ['KickerRu','CoverRu']: continue
            if re.match(r'^\d+-сурет',plain(node['text'])) and i+1<len(nodes) and nodes[i+1]['type']=='image':continue
            # Existing figure numbering is replaced by one sequential caption next to the same original image.
            result.append(p(node['text']))
        elif kind=='code':
            stats['code']+=1
            label=p(f"{stats['code']}-листинг - Код немесе сақталған команда шығысы",LABEL)
            lines=code_block(node['text'],bool(node.get('originalStyle')))
            if len(lines)<=18:result.append(KeepTogether([label,*lines,Spacer(1,8)]))
            else:result.extend([label,*lines,Spacer(1,8)])
        elif kind=='table':
            stats['table']+=1
            result.append(p(f"{stats['table']}-кесте - Орындау деректері мен тексеру нәтижелері",LABEL))
            rows=[]
            for row in node['rows']:
                converted=[]
                for cell in row:
                    vals=[]
                    for b in cell:
                        if b['type']=='code': vals.extend(code_block(b['text'],bool(b.get('originalStyle'))))
                        elif 'text' in b: vals.append(p(b['text'],CELL))
                    converted.append(vals or [p('',CELL)])
                rows.append(converted)
            count=max(map(len,rows))
            widths=node.get('widths')
            if not widths or len(widths)!=count: widths=[1]*count
            widths=[WIDTH*w/sum(widths) for w in widths]
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.black),
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#F0F0F0')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            result.extend([table,Spacer(1,9)])
        elif kind=='image':
            stats['image']+=1
            path=ROOT/node['path'];w,h=ImageReader(str(path)).getSize();scale=min(WIDTH/w,175*mm/h)
            caption=node['caption']
            previous_caption=i>0 and nodes[i-1]['type']=='paragraph' and re.match(r'^\d+-сурет',plain(nodes[i-1]['text']))
            if previous_caption:
                caption=re.sub(r'^\d+-сурет[.\s:-]*','',plain(nodes[i-1]['text']))
            if i+1<len(nodes) and nodes[i+1]['type']=='paragraph':
                candidate=plain(nodes[i+1]['text'])
                if not previous_caption and (re.match(r'^\d+-сурет',candidate) or nodes[i+1].get('originalStyle') in ['Small','SmallRu'] and len(candidate)<400):
                    caption=re.sub(r'^\d+-сурет[.\s:-]*','',candidate);skip.add(i+1)
            if caption.lower().endswith(('.png','.jpg','.jpeg')): caption='Сақталған түпнұсқа интерфейс көрінісі ('+caption+')'
            image=Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')
            original=f'<link href="{PUBLIC+node["path"]}" color="#000000">Түпнұсқаны толық ажыратымдылықта ашу</link>'
            result.append(KeepTogether([image,p(f"{stats['image']}-сурет - {escape(caption)}",CAPTION),p(original,CAPTION)]))
        else: raise ValueError(kind)
    return result

def external_sources(data):
    found=[]
    def walk(v):
        if isinstance(v,dict):
            if 'text' in v:
                for url,label in re.findall(r'<link href="([^"]+)"[^>]*>(.*?)</link>',v['text']):
                    if url.startswith('https://') and not url.startswith('https://github.com/Aruzhaaan-06/'):
                        item=(url,plain(label))
                        if item not in found: found.append(item)
            for x in v.values():
                if isinstance(x,(dict,list)): walk(x)
        elif isinstance(v,list):
            for x in v: walk(x)
    walk(data['blocks']);return found

def build(meta,output):
    data=json.loads((SOURCE/meta['source']).read_text(encoding='utf-8'))
    story=[Cover(meta),PageBreak(),p('МАЗМҰНЫ',CENTER)]
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('Contents',parent=REF,fontSize=14,leading=21,leftIndent=0,firstLineIndent=0)];story.extend([toc,PageBreak()])
    stats={'sub':0,'code':0,'table':0,'image':0,'sectionPrefix':'3' if meta['kind']=='lab' else '2'}
    def section(title,new_page=False):
        if new_page: story.append(PageBreak())
        story.append(p(title,HEADING))
    section('1 Жұмыстың мақсаты');story.append(p(meta['goal']))
    if meta['kind']=='lab':
        section('2 Теориялық мәліметтер');story.append(p(meta['theory']))
        section('3 Жұмыстың орындалу барысы',True)
    else: section('2 Орындау барысы',True)
    story.extend(render_nodes(data['blocks'],stats))
    offset=0 if meta['kind']=='lab' else -1
    section(str(4+offset)+' Жұмыс нәтижелері',True);story.append(p(meta['results']))
    story.append(p(f'Тест нәтижелері мен журналдар <link href="{PUBLIC+meta["evidence"]}/README.md" color="#000000">жұмыс материалдарында</link> [1], іске қосу командалары <link href="{PUBLIC+meta["doc"]}" color="#000000">нұсқаулықта</link> [2] берілген.'))
    section(str(5+offset)+' Талдау');story.append(p(meta['analysis']))
    section(str(6+offset)+' Қорытынды');story.append(p(meta['conclusion']))
    section(str(7+offset)+' Пайдаланылған әдебиеттер тізімі',True)
    refs=[(PUBLIC+meta['evidence']+'/README.md','DemoApi оқу репозиторийі. Нақты тексерулер мен сақталған дәлелдер'),(PUBLIC+meta['doc'],'DemoApi оқу репозиторийі. Жұмыстың орындалу тәртібі')]+external_sources(data)
    for i,(url,label) in enumerate(refs,1):
        story.append(p(f'[{i}] {escape(label)}. Электрондық ресурс. <link href="{escape(url,quote=True)}" color="#000000">{escape(url)}</link>. Қаралған күні: 25.10.2026.',REF))
    story.append(p('DevOps пәнінің оқу материалдары: Devops (1).zip мұрағаты, зертханалық тапсырмалар және бақылау нүктелерінің шарттары.',REF))
    story.append(p('ГОСТ 7.32-2017. Ғылыми-зерттеу жұмысы туралы есеп. Құрылымы және рәсімдеу ережелері. 6-бөлім.',REF))
    output.mkdir(parents=True,exist_ok=True)
    path=output/meta['file'];ReportDoc(path,meta).multiBuild(story)
    return {'file':meta['file'],'source':meta['source'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'elements':stats}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only',nargs='*');parser.add_argument('--output-dir',type=Path,default=ROOT/'reports');parser.add_argument('--font-dir',type=Path,default=Path('C:/Windows/Fonts'));args=parser.parse_args()
    setup_fonts(args.font_dir);results=[]
    for meta in CAT['reports']:
        if args.only and meta['id'] not in args.only: continue
        result=build(meta,args.output_dir);results.append(result);print(json.dumps(result,ensure_ascii=True),flush=True)
    if not results: parser.error('Есеп таңдалмады')

if __name__=='__main__':main()
