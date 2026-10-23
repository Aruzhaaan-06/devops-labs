"""Kazakh report built from retained, actual laboratory 08 evidence."""
from pathlib import Path
from html import escape
import json
import shutil
import textwrap
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader

REPO = Path(__file__).resolve().parents[1]
EV = REPO/'evidence/lab04-release'
OUT = REPO/'reports/lab04-release-report.pdf'
PUBLIC = 'https://github.com/Aruzhaaan-06/devops-labs'
W = A4[0]-36*mm
NAVY = colors.HexColor('#17324D')
INK = colors.HexColor('#223447')
PALE = colors.HexColor('#F1F5F8')
MUTED = colors.HexColor('#596A7B')
for font, file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(font, str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
BODY = ParagraphStyle('Body',fontName='Arial',fontSize=10,leading=14,textColor=INK,spaceAfter=8)
SMALL = ParagraphStyle('Small',parent=BODY,fontSize=8.5,leading=11.5,textColor=MUTED)
TITLE = ParagraphStyle('Title',parent=BODY,fontName='Arial-Bold',fontSize=24,leading=30,textColor=NAVY,spaceAfter=18)
H = ParagraphStyle('Heading',parent=BODY,fontName='Arial-Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=13)
SUB = ParagraphStyle('Sub',parent=BODY,fontName='Arial-Bold',fontSize=10.5,leading=14,textColor=NAVY,spaceBefore=5)
CELL = ParagraphStyle('Cell',parent=BODY,fontSize=8.8,leading=12,spaceAfter=0)
HEAD = ParagraphStyle('Head',parent=CELL,fontName='Arial-Bold',textColor=colors.white)
CODE = ParagraphStyle('Code',fontName='Mono',fontSize=7.4,leading=10.3,textColor=INK)

def p(text,style=BODY):
    return Paragraph(text,style)

def link(path,label):
    return f'<link href="{PUBLIC}/{path}" color="#175E9A">{label}</link>'

def table(rows,widths=None):
    t=Table([[p(escape(str(x)),HEAD if i==0 else CELL) for x in row] for i,row in enumerate(rows)],
        colWidths=widths or [W*.36,W*.64],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def code(text):
    lines=[]
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line,100,break_long_words=False,break_on_hyphens=False,replace_whitespace=False) or [' '])
    t=Table([[p(escape(line).replace(' ','&nbsp;'),CODE)] for line in lines],colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LEFTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t

def fig(name,height=320):
    path=EV/'screenshots'/name
    w,h=ImageReader(str(path)).getSize()
    scale=min(W/w,height/h)
    return Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')

def footer(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
    canvas.line(18*mm,16*mm,A4[0]-18*mm,16*mm)
    canvas.setFont('Arial',7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 08')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page))
    canvas.restoreState()

load=lambda name:json.loads((EV/name).read_text(encoding='utf-8'))
checks=load('checks.json')
assert checks['technicalChecksPassed']==19
release=load('release-verification.json')
review=load('rename-final-review.json')
http=load('live-http.json')
rename=next(x for x in http['records'] if x['method']=='PUT' and x['status']==200)
story=[
    p('ВКТУ · DEVOPS · 08-МАТЕРИАЛ',SMALL),Spacer(1,10*mm),
    p('4-зертханалық жұмыс<br/>Git және GitHub',TITLE),
    p('2-бөлім: PR арқылы кодты өзгерту және алғашқы шығарылым',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
           ['Университет','ВКТУ'],['Күні','2026 жылғы 23 қазан'],['Тапсырма','08-материал, 7-9-бөлімдер және CODEOWNERS']]),
    Spacer(1,7*mm),
    p('Мақсаты',SUB),
    p('main тармағы қорғалған репозиторийде өзгерістерді жеке тармақ пен PR арқылы өткізу, пікірді ескеріп түзету, жоба атауын екі сақтау режимінде өзгерту және v0.1.0 шығарылымын жариялау.'),
    p('Нәтиже: техникалық бөлік орындалды',SUB),
    p('19 техникалық тексеру сәтті өтті. InMemory: 38/38, PostgreSQL: 38/38. Postman: 37 сұрау, 99 тексеру. Үш issue жабылып, Done бағанына өтті. Шығарылым жарияланды.'),
    p(link('','Репозиторий')+' · '+link('pull/14','API өзгерісінің PR-ы')+' · '+link('releases/tag/v0.1.0','v0.1.0 шығарылымы')),
    p('Ресми шектеу: бір адамның екі аккаунты пайдаланылды. Оқытушының логині берілмеген, сондықтан ол collaborators тізіміне қосылмаған. Бұл есеп басқа студентпен жұптық жұмыс пен бөлек B репозиторийіндегі кезеңнің орындалғанын мәлімдемейді.',SMALL),
    p('Түсіндірмелер қазақ тілінде жазылды. Код, пәрмендер, API жауаптары және шынайы экран суреттері дәлел ретінде бастапқы тілінде сақталды.',SMALL),
    PageBreak(),
    p('1. Репозиторийді баптау',H),
    p('Алдыңғы жұмыстың жалғасы ретінде бар репозиторий қолданылды. Жұмыс басында main таза болды; Git, PowerShell 7, .NET 10 SDK, Docker Desktop, Compose, GitHub CLI, Postman CLI және браузер пайдаланылды.'),
    p('PR үлгісі және Dependabot',SUB),
    p('Оқу kit жинағындағы екі файл оқылып, .github каталогына қосылды. PR үлгісіндегі Compose пәрменіне --wait қосылды: дайындықты күту тексеруге енгізілді. Үлгі авторға тесттерді, құжаттаманы және құпия деректердің жоқтығын тексеруді еске салады.'),
    table([['Файл','Міндеті'],['pull_request_template.md','Өзгеріс сипаттамасы, Closes #, іске қосу және тексеру чек-парағы'],
        ['dependabot.yml','NuGet, Docker және GitHub Actions тәуелділіктерін апта сайын тексеру'],
        ['CODEOWNERS','Барлық файлдар үшін екінші аккаунтты код иесі ретінде белгілеу']]),
    Spacer(1,5*mm),
    p(link('pull/9','PR #9')+' Closes #2 арқылы issue #2-ні жапты. Өзгеріс мақұлдаудан кейін squash тәсілімен main тармағына біріктірілді.'),
    p('CODEOWNERS және main қорғанысы',SUB),
    code('* @temirkhanerbolatovich-coder'),Spacer(1,3*mm),
    p('Қолданыстағы ruleset сақталып, Require review from Code Owners қосылды. Бір мақұлдау міндетті; bypass тізімі бос. Тікелей push, force-push және main тармағын жоюға қойылған шектеулер сақталды.'),
    p('Дайын PR #14 ашылғаннан кейін GitHub екінші аккаунтты code owner ретінде автоматты түрде тағайындады. Ревьюер қолмен сұратылған жоқ. CODEOWNERS қатесін тексеретін GitHub API бос қателер тізімін қайтарды.'),
    p('Dependabot нақты жұмыс істеді: бес NuGet жаңарту PR-ын жасады. Олар осы жұмыста біріктірілген жоқ; тәуелділіктердің қауіпсіздігі толық дәлелденді деген қорытынды жасалмайды. GitHub Actions CI 09-материалда қосылады.',SMALL),
    PageBreak(),
    p('2. Жоба атауын өзгерту',H),
    code('PUT /api/projects/{id}\nContent-Type: application/json\n\n{ "name": "Жаңа атау" }'),Spacer(1,4*mm),
    table([['HTTP жауабы','Шарты'],['200','Жоба атауы өзгертілді; id, name, createdAt қайтарылады'],
        ['400','name жоқ, null, бос, тек бос орындардан тұрады немесе 100 таңбадан ұзын'],
        ['404','Жоба табылмады; атаудың басқа жобада болуы бұл нәтижені өзгертпейді'],
        ['409','Атауды басқа жоба қолданып отыр']]),Spacer(1,4*mm),
    p('Қабаттар бойынша орындалуы',SUB),
    p('<b>Controller:</b> RenameProjectRequest үшін Required және StringLength(100) тексеруі. Жоба жоқ болса 404; атау басқа жобада болса 409. XML түсіндірмелері мен жауап түрлері OpenAPI құжаттамасына енгізілді.'),
    p('<b>Service:</b> ProjectService.RenameAsync репозиторийді шақырады; жоба табылып өзгертілсе ғана құрылымды журнал жазбасын шығарады.'),
    p('<b>InMemory:</b> lock (store.Sync) ішінде FindIndex арқылы жоба табылады. Жоқ болса null; атау басқа жобада болса қақтығыс. Бар жазба with { Name = name } көшірмесімен ауыстырылады.'),
    p('<b>PostgreSQL:</b> пайдаланушы деректері SQL мәтініне тікелей қосылмайды; id мен name бөлек параметрлер ретінде беріледі.'),
    code('UPDATE projects SET name = $2 WHERE id = $1\nRETURNING id, name, created_at'),Spacer(1,4*mm),
    p('Маңызды қасиеттер',SUB),
    p('Сол атаумен қайталанған PUT 200 қайтарады. Идентификатор, createdAt және тапсырмалар сақталады. Бір атауға қатар келген өзгерістерде бірегейлік InMemory lock және PostgreSQL UNIQUE арқылы қорғалады. SQL бірегейлік қақтығысы клиентке ішкі SQL деректерін ашпай HTTP 409 түрінде беріледі.'),
    p('Атаулар регистрге тәуелді; бос орындар автоматты түрде қысқартылмайды. Бұрынғы POST әрекетінің бәсекелес сұраулардағы мінез-құлқы осы жұмыста өзгертілмеді.',SMALL),
    PageBreak(),
    p('3. Нақты тексеру нәтижелері',H),
    table([['Тексеру','Нәтиже'],['InMemory тесттері','38/38: 7 модульдік және 31 интеграциялық'],
        ['PostgreSQL тесттері','38/38; бөлек demo_lab08_tests дерекқорында'],
        ['Postman толық жинағы','37 HTTP сұрауы, 99 тексеру, 0 қате, шығу коды 0'],
        ['Тікелей HTTP тексерулері','13 сұрау; күтілетін жауаптар алынды'],
        ['Compose','Образ құрастырылды; API және БД healthy'],
        ['OpenAPI','PUT әрекетінің 200/400/404/409 жауаптары бар']]),Spacer(1,4*mm),
    p('Қосылған 10 тест нұсқасы',SUB),
    p('Сәтті өзгеріс кезінде id, createdAt және тапсырманың сақталуы; бос емес бірегей атаудың қақтығысы; бос жол, тек бос орындар, null және 101 таңбалы атау; жоқ жоба; сол атаумен қайталанатын PUT; қатар келген екі өзгеріс; апострофы бар SQL-ге ұқсас мәтіннің жай дерек ретінде сақталуы тексерілді.'),
    p('Шынайы жауап үлгісі',SUB),
    code(json.dumps(rename['response'],ensure_ascii=False,indent=2)),Spacer(1,4*mm),
    p('200 жауабында атау өзгерді. Кейінгі 400 және 409 сұрауларынан соң GET бұрынғы сәтті нәтижені қайтарды. Тікелей тексеру тек өзі жасаған екі жобаны жойды. Postman-ның жаңа қалтасы да тәуелсіз екі жоба жасап, соңында оларды тазалады.'),
    p('Нұсқаны тексеру',SUB),
    p('Контейнердің GET / жауабындағы version өрісі тексерілген тармақтың SHA мәніне тең: '+http['testedCommit']+'. /health/live және /health/ready екеуі де 200 қайтарды.'),
    p('Postman нәтижесі жергілікті мәтіндік журналда сақталды. --output арқылы экспорт бұл орнатылымда аккаунтқа кіруді талап етті; бұл мүмкіндік қолданылмады. Кәдімгі жергілікті іске қосу сәтті аяқталды. Бұлтқа есеп жарияланды деген тұжырым жоқ.',SMALL),
    PageBreak(),
    p('4. Үш issue және Done тақтасы',H),
    table([['Issue','Жабылған PR'],['#1 - README нұсқаулығы','#4, алдыңғы бөлімде орындалған'],
        ['#2 - PR үлгісі және Dependabot','#9, осы бөлімде орындалған'],['#3 - жоба атауын өзгерту','#14, осы бөлімде орындалған']]),Spacer(1,5*mm),
    fig('board-done.jpg',350),Spacer(1,3*mm),
    p('1-сурет. GitHub Projects тақтасының шынайы көрінісі: Done бағанында #1, #2 және #3. Карточкаларда оларды жапқан #4, #9 және #14 PR сілтемелері көрсетілген.',SMALL),
    p('<link href="https://github.com/users/Aruzhaaan-06/projects/1" color="#175E9A">Тақтаны GitHub-та ашу</link>. Жаңартылған интерфейсте Todo = 0, In Progress = 0, Done = 3 екені тексерілді. Карточкалар қолмен көшірілген жоқ; issue жабылу оқиғалары арқылы ауысты.'),
    p('Есептегі сурет браузерден тікелей алынды. Done бағанын көрсету үшін тақта көлденең жылжытылды; суреттегі деректер өзгертілген жоқ.',SMALL),
    PageBreak(),
    p('5. Кодты пікір арқылы тексеру',H),
    p(link('pull/14','PR #14')+' feat/3-rename-project тармағынан main тармағына біріктірілді. Бастапқы код коммиті: 24d5292. Ревьюер қабаттарды, екі сақтау режимін, SQL параметрлерін және құпия деректердің жоқтығын қарады.'),
    p('Пікірдің қазақша мазмұны',SUB),
    p('Екі жобаны бір мезетте бір атауға өзгерту тесті жетіспейді: бірі 200, екіншісі 409 алуы, ал жаңа атау тек бір жобада қалуы керек. SQL параметрлеуін тексеру үшін апострофы бар атауға да нақты сұрау қосу ұсынылды.'),
    p(link('pull/14#discussion_r4357236131','Жолға қалдырылған бастапқы пікір')+' · '+link('commit/9b1780b286c4098684285284ae632ebf1e708531','Жеке түзету коммиті 9b1780b')),
    p('Автор екі тест қосып, пікірге коммит сілтемесімен жауап берді. Тест саны 36-дан 38-ге өсті. Содан кейін екінші аккаунт дәл осы соңғы SHA үшін Approve қойды. Қайта тексеру InMemory мен PostgreSQL режимдерінің екеуінде де өтті.'),
    fig('rename-pr.jpg',310),Spacer(1,3*mm),
    p('2-сурет. API өзгерісінің PR #14 беті: Merged күйі және Closes #3 байланысы. Бастапқы 36 тест пен кейінгі 38 тест туралы мәліметтер орындалу кезеңдерін көрсетеді.',SMALL),
    p('GitHub-тағы lab08/manual-verification жасыл мәртебесі нақты жергілікті нәтижелер негізінде қолмен жарияланды. Бұл автоматты CI емес. Ревью аккаунттарының екеуі де бір иеге тиесілі екені PR-да және осы есепте ашық көрсетілді.',SMALL),
    PageBreak(),
    p('6. v0.1.0 шығарылымы',H),
    p('Код мақұлданып, main тармағына біріктірілгеннен кейін аннотациясы бар v0.1.0 тегі жіберілді. GitHub шығарылымының сипаттамасы --generate-notes арқылы автоматты жасалды.'),
    code('git tag -a v0.1.0 -m "First course release"\ngit push origin v0.1.0\ngh release create v0.1.0 --verify-tag --generate-notes'),Spacer(1,5*mm),
    fig('release.jpg',315),Spacer(1,3*mm),
    p('3-сурет. Жарияланған v0.1.0 шығарылымы, оның тегі және автоматты What\'s Changed бөлімі.',SMALL),
    p(link('releases/tag/v0.1.0','Жарияланған шығарылымды ашу')+' · '+link('tree/v0.1.0','Тегтегі бастапқы код')),
    p('Тегтің нақты коммиті: '+release['commit']+'. Ол PR #14 біріктіру коммитіне тең. Шығарылым ағашы тесттер орындалған 9b1780b коммитінің файл ағашымен бірдей. Автоматты жазбаларда PR #9 және PR #14 бар; шығарылым draft немесе prerelease емес.'),
    p('Бастапқы жариялау кезінде осы жұмыс ішінде тег ертерек коммитке қойылғаны анықталды. Жаңа ғана жасалған қате шығарылым мен тег жойылып, код біріктірілгеннен кейін қайта жасалды. Жоғарыдағы SHA мен сілтемелер түпкілікті дұрыс нұсқаны көрсетеді.',SMALL),
    PageBreak(),
    p('7. Өзін-өзі тексеру сұрақтары',H),
    p('1. Git тармағы деген не?',SUB),
    p('Тармақ - коммитке сілтеме. Оны жасау файлдарды толық көшіруді қажет етпейді: жаңа сілтеме ғана қосылады.'),
    p('2. Индекс не үшін керек?',SUB),
    p('Индекс келесі коммитке енетін өзгерістерді таңдайды. Бір файлдағы барлық өзгерісті міндетті түрде бір коммитке біріктіру қажет емес.'),
    p('3. Ескі коммит өзгерсе, кейінгі хэштер неге өзгереді?',SUB),
    p('Коммит құрамына ата-ана коммитінің хэші кіреді. Ата-ана өзгерсе, одан тарайтын коммиттердің мазмұны мен хэштері де өзгереді.'),
    p('4. Fast-forward, merge commit және squash айырмасы қандай?',SUB),
    p('Fast-forward кезінде нысана тармақтың ұшы алға жылжиды, себебі ол біріктірілетін тармақтың атасы. Тарих екіге бөлінсе, кәдімгі merge ортақ коммит жасайды. Squash өзгерістерді бір жаңа коммитке жинайды, бастапқы тармақтың ата-аналық байланысын сақтамайды.'),
    p('5. Әртүрлі және бірдей жолдар өзгерсе не болады?',SUB),
    p('Git әртүрлі аймақтардағы өзгерістерді көбіне өзі біріктіреді. Бір аймаққа үйлеспейтін өзгерістер түссе, қолмен шешілетін конфликт пайда болады. Бірдей жолдағы өзгерістер толық бірдей болса, конфликт болмауы мүмкін.'),
    p('6. main үшін revert неге қолайлы?',SUB),
    p('revert бұрынғы коммитті жоймай, оның әсерін кері қайтаратын жаңа коммит жасайды. Ортақ тарих сақталады; reset және force-push әріптестердің тарихын бұзуы мүмкін.'),
    p('7. main тармағын қалай қорғаймыз?',SUB),
    p('Тікелей push пен force-push-ты, тармақты жоюды шектейміз; PR және code owner мақұлдауын талап етеміз. CI қосылғаннан кейін оның сәтті тексеруі де міндетті болуы тиіс.'),
    p('8. JSON өрісін жою және жаңа endpoint қосу нұсқаға қалай әсер етеді?',SUB),
    p('Тұрақты 1.x API-де үйлесімділікті бұзатын өрісті жою - major, кері үйлесімді endpoint қосу - minor өзгеріс. 0.x кезеңінде API тұрақсыз болуы мүмкін, сондықтан өзгеріс саясаты мен breaking change release notes ішінде анық жазылуы керек. Бұл жұмыста талап етілген алғашқы тег - v0.1.0.'),
    p('9. Құпия токен жарияланып кетсе не істеу керек?',SUB),
    p('Алдымен токенді дереу кері қайтарып, жаңасын қауіпсіз жерде орнату керек. Кейін қолжетімділік пен журналдар тексеріледі, қолданылған жерлер жаңартылады, қажет болса тарих тазаланады. Коммиттен жай өшіру жарияланған токенді жарамсыз етпейді.'),
    p('Қорытынды және тапсыру шектері',SUB),
    p('08-материалдың техникалық бөлігі мен CODEOWNERS қосымша тапсырмасы орындалды. Толық формалды тапсыру үшін оқытушыны қосу және екі аккаунтпен орындалған жұптық сценарийді келісу қажет. Алдыңғы жұмыстардағы қолмен жөндеу мен экран суреттері өз чек-парағында қалады. Келесі жұмыс - 09: CI.'),
]
OUT.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,
    topMargin=18*mm,bottomMargin=22*mm,title='ВКТУ | 08-материал | Git және GitHub, 2-бөлім',
    author='Есімханова Аружан Түсіпханқызы',subject='Қазақша есеп: PUT, PR, CODEOWNERS, v0.1.0')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
