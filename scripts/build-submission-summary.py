"""Build a Kazakh submission supplement from retained evidence; no network."""
from pathlib import Path
from html import escape
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/submission-summary-kk.pdf'
DATA = json.loads((ROOT / 'evidence/submission-readiness/checks.json').read_text(encoding='utf-8'))
PUBLIC = 'https://github.com/Aruzhaaan-06/devops-labs'
for name, file in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold')
NAVY = colors.HexColor('#17324D')
BODY = ParagraphStyle('Body', fontName='Arial', fontSize=10, leading=14, spaceAfter=8)
HEAD = ParagraphStyle('Head', parent=BODY, fontName='Arial-Bold', fontSize=18, leading=23, textColor=NAVY, spaceAfter=14)
SUB = ParagraphStyle('Sub', parent=BODY, fontName='Arial-Bold', fontSize=11, leading=15, textColor=NAVY, spaceBefore=5)
CELL = ParagraphStyle('Cell', parent=BODY, fontSize=9, leading=12, spaceAfter=0)
W = A4[0] - 36 * mm

def p(text, style=BODY):
    return Paragraph(text, style)

def table(rows, widths):
    result = Table([[p(escape(str(v)), CELL) for v in row] for row in rows], colWidths=widths, repeatRows=1)
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E4EDF4')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F8')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return result

def link(path, label):
    return f'<link href="{PUBLIC}/{path}" color="#175E9A">{escape(label)}</link>'

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Arial', 7)
    canvas.setFillColor(NAVY)
    canvas.drawString(18 * mm, 11 * mm, 'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о')
    canvas.drawRightString(A4[0] - 18 * mm, 11 * mm, str(doc.page))
    canvas.restoreState()

story = [p('DevOps жұмыстарын тапсыру<br/>Қорытынды толықтыру', HEAD),
    p('2026 жылғы 25 қазан · Қазақ тіліндегі есептерге қосымша'),
    table([['Мәлімет', 'Мәні'], ['Университет', 'ВКТУ'], ['Орындаған', 'Есімханова Аружан Түсіпханқызы'], ['Тобы', '25-ИСТК-2о'], ['Негізгі жинақ', '14 зертханалық есеп, 116 бет; v1.1.0 релизі']], [W * .30, W * .70]),
    Spacer(1, 5 * mm), p('Жинақтың мақсаты', SUB),
    p('Бұл толықтыру бұрынғы есептерді алмастырмайды. Ол код, тест және сақталған тәжірибе нәтижелерін тапсыру кезінде жетіспейтін интерфейс дәлелдері мен ұйымдастыру қадамдарынан ажыратады. Жұмыстар толық қабылданды немесе белгілі бір бағаға кепілдік берілді деп мәлімделмейді.'),
    p('Қайта тексерілген нәтижелер', SUB)]
rows = [['Нұсқа / қойма', 'Жиынтық', 'Нәтиже']]
for r in DATA['runs']:
    rows.append([r['sourceRef'] + ' / ' + r['storage'], 'Міндетті 24' if r['total'] == 24 else 'Толық 28', f"{r['passed']}/{r['total']}; қате {r['failed']}"])
story += [table(rows, [W * .50, W * .25, W * .25]), Spacer(1, 4 * mm),
    p('Бұл тестілер dotnet test арқылы орындалды. TRX қорытындысында нақты уақыт, бастапқы код SHA және жергілікті түпнұсқаның SHA-256 мәні бар. Test Explorer интерфейсінде орындау және оның суреті әзірге расталмаған.'),
    p('SQL тексеруі жеке demo_ui_checks дерекқорында орындалды. Екі іске қосудан кейінгі тек оқу тексеруінде 24 жоба мен 21 тапсырма болды. Негізгі demo дерекқоры пайдаланылмады. Қосылу құпиясы Git сыртындағы .NET User Secrets қоймасында сақталған.'),
    p(link('blob/main/evidence/submission-readiness/checks.json', 'Тест қорытындысы') + ' · ' + link('releases/tag/v1.1.0', 'Негізгі релиз') + ' · ' + link('pull/33', 'Толықтыру PR №33')),
    PageBreak(), p('Жетіспейтін интерфейс дәлелдері', HEAD),
    table([
        ['Жұмыс', 'Қажет дәлел'],
        ['1, 1-бөлім', 'Postman: demo-api коллекциясының атауы, сұраулар тізімі және нақты жауап. Бөлек көшірме: localhost:8094.'],
        ['1, 2-бөлім', 'lab01-required-24 шешіміндегі 24 жасыл тест; екі stats тесті көрінуі керек.'],
        ['1, 2-бөлім', 'F9/F10/F11 арқылы екі сұрау: Todo → Done (409), бөлек Todo → InProgress (200). Locals және Call Stack.'],
        ['2 · 03-материал', 'Docker Desktop → Settings → General: Use the WSL 2 based engine қосылғанының шынайы суреті.'],
        ['3 · 05-материал', 'Visual Studio іске қосу шығысында Хранилище: PostgreSQL; SQL Test Explorer-де 24 міндетті және бөлек 28 толық тест.'],
        ['4 · 07-материал', 'Қабылданбаған push терезесінің шынайы суреті. GH013 мәтіндік журналы бұрыннан сақталған.'],
        ['7 · 14-материал', 'Grafana UI арқылы JSON экспорты және ақау кезіндегі Grafana/Dozzle бақылауы. Қазіргі API/файл дәлелдері UI әрекеті ретінде саналмайды.'],
        ['8 · 15-материал', 'Нақты инциденттің Grafana p95 және ALERTS firing тарихының көріністері; кейін ашылған тарихи сурет ретінде белгілеу.'],
    ], [W * .24, W * .76]), Spacer(1, 4 * mm),
    p('Құралдың нақты шектеуі', SUB),
    p('Терезені қайта белсендіргеннен кейін де Visual Studio суреті FrameArrived timed out қатесімен аяқталды. Браузер құралы Local browser use is disabled in Work settings қатесін берді. Жаңа UI суреттері алынған немесе қолмен жөндеу орындалған деп көрсетілмейді.'),
    p('Жөндеу кезінде 409 тармағында жаңарту шақырылмайды. 200 тармағы ChangeStatusAsync → SetStatusAsync → Replace арқылы өтеді. Суреттер нақты іске қосу мен бастапқы код нұсқасына сәйкес келуі керек.'),
    PageBreak(), p('Тапсыру реті және ашық тармақтар', HEAD),
    p('1. Бірінші жұмыстың бөлек шешімін ашу', SUB),
    p('lab01-required-24/DemoApi.slnx; Debug және http профилі; localhost:8094. Міндетті 24 тестіні іске қосып, Postman мен екі жөндеу сценарийінің суреттерін сақтау.'),
    p('2. PostgreSQL дәлелдерін толықтыру', SUB),
    p('lab03-postgres/DemoApi.slnx; localhost:8095. Міндетті жиынтық үшін postgres-required24.runsettings, толық жиынтық үшін postgres-full28.runsettings таңдалады. Қосылу құпиясын кадрда ашуға болмайды.'),
    p('3. Мониторингтің тарихи көрінісі', SUB),
    p('2026 жылғы 24 қазан, 18:10-18:24 UTC; жергілікті уақыт 23:10-23:24 UTC+5. Grafana-да Latency p95; Prometheus-те ALERTS{alertname="ApiSlowRequests",alertstate="firing"}. Тарихи көріністі инцидент кезінде түсірілген түпнұсқа сурет деп беруге болмайды. Қазіргі inactive күйі өткен firing-ті дәлелдемейді.'),
    p('Инциденттің сақталған уақыты: T0 18:10:54 UTC, T1 18:14:18.726 UTC, T2 18:15:58.875 UTC. Ақаулы релиз сурет алу үшін қайта орнатылмайды; нақты JSON және есептегі деректер сақталған.'),
    p('4. Оқытушының немесе студенттің қатысуы', SUB),
    p('Оқытушының GitHub атауы әлі берілмеген. Екі ревью аккаунты бір адамға тиесілі: оны тәуелсіз жұптық жұмыс деп көрсетуге болмайды. Жеке B репозиторийінің орындалмаған кезеңін оқытушымен келісу қажет. 04-материалдың шарты жоқ; бұл оның орындалғанын білдірмейді.'),
    p('Курс форумында слотқа жазылу, 10 минуттық онлайн қорғауда экранды көрсету және екі сұраққа жауап беру, есептерді СДО-ға жүктеу студенттің қатысуын талап етеді. Осы құжат бұл әрекеттердің орнына жүрмейді.'),
    p('Жинақ және оның шекарасы', SUB),
    p('Негізгі 14 PDF өзгертілмейді. Бұл үш беттік толықтыру бөлек беріледі. Қорытынды архивте есептер, бірінші жұмыстың тарихи бастапқы коды, тексеру қорытындылары және SHA-256 тізімі болады. Құпиялар, .env, жергілікті тіркелгі файлдары және пайдаланушы жолдары архивке кірмейді. Performance baseline №30 осы аяқтау кезеңінің құрамына кірмейді.'),
    p(link('blob/main/docs/submission-checklist.md', 'Толық чек-парақ') + ' · ' + link('blob/main/reports/README.md', 'Барлық есептер'))]
SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=21*mm,
    title='DevOps - тапсыруға қорытынды толықтыру', author='Есімханова Аружан Түсіпханқызы').build(story, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(OUT)
assert len(reader.pages) == 3, len(reader.pages)
text = '\n'.join(page.extract_text() for page in reader.pages)
assert all(token in text for token in ['ВКТУ', 'Түсіпханқызы', '24/24', '28/28', 'орындалған деп көрсетілмейді'])
assert '\ufffd' not in text
print(json.dumps({'pages':len(reader.pages),'bytes':OUT.stat().st_size,'textVerified':True}))
