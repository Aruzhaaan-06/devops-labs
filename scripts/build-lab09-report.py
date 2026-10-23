"""Build the Kazakh material 09 report from retained CI evidence; does not run CI."""
from pathlib import Path
from html import escape
import json
import textwrap
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader

REPO=Path(__file__).resolve().parents[1]
EV=REPO/'evidence/lab05-ci'
OUT=REPO/'reports/lab05-ci-report.pdf'
PUBLIC='https://github.com/Aruzhaaan-06/devops-labs'
W=A4[0]-36*mm
NAVY=colors.HexColor('#17324D')
INK=colors.HexColor('#223447')
PALE=colors.HexColor('#F1F5F8')
MUTED=colors.HexColor('#596A7B')
for font,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(font,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold')
BODY=ParagraphStyle('Body',fontName='Arial',fontSize=10,leading=14,textColor=INK,spaceAfter=8)
SMALL=ParagraphStyle('Small',parent=BODY,fontSize=8.5,leading=11.5,textColor=MUTED)
TITLE=ParagraphStyle('Title',parent=BODY,fontName='Arial-Bold',fontSize=24,leading=30,textColor=NAVY,spaceAfter=18)
H=ParagraphStyle('Heading',parent=BODY,fontName='Arial-Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=13)
SUB=ParagraphStyle('Sub',parent=BODY,fontName='Arial-Bold',fontSize=10.5,leading=14,textColor=NAVY,spaceBefore=5)
CELL=ParagraphStyle('Cell',parent=BODY,fontSize=8.8,leading=12,spaceAfter=0)
HEAD=ParagraphStyle('Head',parent=CELL,fontName='Arial-Bold',textColor=colors.white)
CODE=ParagraphStyle('Code',fontName='Mono',fontSize=7.2,leading=10,textColor=INK)

def p(text,style=BODY):return Paragraph(text,style)

def link(path,label):return f'<link href="{PUBLIC}/{path}" color="#175E9A">{label}</link>'

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

def fig(name,height):
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
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 09')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page))
    canvas.restoreState()

load=lambda n:json.loads((EV/n).read_text(encoding='utf-8-sig'))
initial=load('initial-run.json')
failure=load('failure-run.json')
restored=load('restored-run.json')
assert load('checks.json')['technicalChecksPassed']==24
assert initial['conclusion']=='success' and failure['conclusion']=='failure' and restored['conclusion']=='success'
story=[
    p('ВКТУ · DEVOPS · 09-МАТЕРИАЛ',SMALL),Spacer(1,10*mm),
    p('5-зертханалық жұмыс<br/>Үздіксіз интеграция',TITLE),
    p('1-бөлім: пайплайн, міндетті тест және жергілікті runner',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
        ['Университет','ВКТУ'],['Күні','2026 жылғы 23 қазан'],['Тапсырма','09-материал, 1-5-тармақтар']]),Spacer(1,6*mm),
    p('Мақсаты',SUB),
    p('Әр PR үшін PostgreSQL қатысатын автоматты тесттерді іске қосу, қызыл test бар кезде main тармағына біріктіруге тыйым салу және келесі бөлімге жергілікті Windows runner мен құпия деректі дайындау.'),
    p('Нақты нәтиже',SUB),
    p('Жергілікті Release құрастыруы сәтті: 0 ескерту, 0 қате; PostgreSQL тесттері 38/38. GitHub-та үш нақты кезең орындалды: жасыл 38/38, әдейі бұзылған бір тестпен қызыл 37/38 және тест қалпына келтірілгеннен кейін жасыл 38/38. 24 техникалық тексеру сәтті өтті.'),
    p(link('pull/17','Workflow және бес жауап берілген PR #17')+' · '+link('tree/ci/pipeline','Жұмыс тармағы ci/pipeline')),
    p('Методичка бойынша PR осы бөлімде ашық қалдырылды. Біріктіру, GHCR-ға образ жіберу, жергілікті deploy және rollback 10-материалға жатады. Олардың орындалғаны осы есепте мәлімделмейді.',SMALL),
    p('Екі GitHub аккаунты бір иеге тиесілі. Ревью - GitHub механизмінің техникалық тексеруі; ол тәуелсіз студенттің тексеруі ретінде көрсетілмейді. Код, пәрмендер, лог жолдары және шынайы суреттер бастапқы тілінде сақталды.',SMALL),
    PageBreak(),
    p('1. Workflow және бес сұраққа жауап',H),
    p('1. PR, main push және v1.0.0 тегі',SUB),
    table([['Оқиға','Орындалатын жұмыстар'],['main тармағына PR','test; image және deploy skipped'],
        ['main push','test → image → deploy; келесі job алдыңғысына тәуелді'],
        ['v1.0.0 тегі','test → image; deploy skipped, себебі ref main емес']]),Spacer(1,4*mm),
    p('Бұл кесте workflow шарттарын түсіндіреді. Осы бөлімде нақты PR жолы тексерілді; push және тег арқылы жариялау келесі бөлімде тексеріледі.'),
    p('2. PostgreSQL қайдан алынады?',SUB),
    p('test job GitHub-hosted Ubuntu runner-де орындалады. services.postgres postgres:18-alpine контейнерін іске қосып, pg_isready арқылы оның дайындығын күтеді. Storage=Postgres және ConnectionStrings__Db тесттерді localhost:5432 мекенжайындағы уақытша demo дерекқорына бағыттайды. CI-дегі demo паролі жергілікті томның құпиясөзі емес.'),
    p('3. image ішіндегі GITHUB_TOKEN құқықтары',SUB),
    p('contents: read бастапқы кодты алуға, packages: write образды GHCR-ға жіберуге қажет. Қосымша write құқығы тек image job үшін берілген; негізгі workflow contents: read пайдаланады. Жеке PAT workflow файлына енгізілмейді.'),
    p('4. deploy қайда орындалады және неге?',SUB),
    p('self-hosted, Windows, X64, devops-labs белгілері бар жергілікті орындаушы агентте орындалады. Ол осы компьютердің Docker Desktop қызметіне қол жеткізеді; GitHub-hosted runner жергілікті Docker-ді көрмейді. deploy тек осы репозиторийдің main push оқиғасына арналған.'),
    p('5. Жаңа контейнер healthy болмаса не болады?',SUB),
    p('docker compose up пәрменіндегі --wait --wait-timeout 90 сәтсіз аяқталып, job қызыл болады. Кейінгі readiness smoke test орындалмайды. Smoke test орындалған кезде HTTP қатесі де job-ты сәтсіз етеді. Workflow автоматты rollback жасамайды; кері қайтару келесі материалда тексеріледі.'),
    p('Осы бес жауап PR #17 сипаттамасына да енгізілген. Жасыл CI тек тексерілген кодқа қатысты; ол жариялау немесе deploy автоматты түрде орындалды дегенді білдірмейді.',SMALL),
    PageBreak(),
    p('2. Жергілікті тексеру және бейімдеу',H),
    p('Алдымен Docker Compose дерекқоры іске қосылды. Жергілікті .env құпиясөзін өзгертпей, тек тесттерге арналған demo_lab09_tests дерекқоры дайындалды. Дерекқор құпиясөзі тек процесс ортасы арқылы берілді, журналға жазылған жоқ.'),
    code('docker compose up -d --wait db\ndotnet restore DemoApi.slnx\ndotnet build DemoApi.slnx --no-restore -c Release\ndotnet test DemoApi.slnx --no-build -c Release'),Spacer(1,4*mm),
    p('SQL тесттерін орындағанда Storage=Postgres және ConnectionStrings__Db айнымалылары бөлек тест дерекқорын көрсетті. Нәтиже: барлық 38 тест өтті, оның 7-еуі модульдік, 31-і интеграциялық.'),
    p('Оқу kit файлы қалай өзгертілді?',SUB),
    table([['Бейімдеу','Себебі'],['DemoApi.slnx нақты көрсетілді','Runner дұрыс шешімді restore/build/test етуі үшін'],
        ['6 action нақты SHA-ға бекітілді','Әр іске қосуда сол ресми action коды пайдаланылуы үшін'],
        ['persist-credentials: false','Checkout-тан кейін Git тіркелгі деректерін сақтамау үшін'],
        ['Windows/X64/devops-labs белгілері','Deploy дұрыс жергілікті runner-ге түсуі үшін'],
        ['15432, 8088 және 10.254.54.0/24','Қолданыстағы Compose порттары мен желісіне сәйкестендіру үшін']]),Spacer(1,4*mm),
    p('Тесті merge шартына айналдыру',SUB),
    p('Бірінші GitHub Actions run сәтті өткен соң, қолданыстағы main ruleset-ке required_status_checks ережесі қосылды. Контекст - test, дереккөзі - GitHub Actions қолданбасы. Соңғы main кодымен тексеруді талап ету қосылды. Бұрынғы PR, code owner мақұлдауы, force-push пен жоюға тыйым сақталды; bypass тізімі бос қалды.'),
    p('Ревьюердің Approve-ы тест әдейі бұзылмай тұрып алынды. Қызыл кезеңде мақұлдау сақталғанымен, міндетті test сәтсіз болғандықтан merge қолжетімсіз болды. Осылайша блоктау тек ревьюдің жоқтығынан емес, нақты тесттен болғаны расталды.'),
    p('Жергілікті тексеру, CI және GitHub ruleset нәтижелері бөлек JSON және мәтіндік журналдарда сақталған.',SMALL),
    PageBreak(),
    p('3. Қызыл test merge-ті бұғаттады',H),
    p('Create_DuplicateName_ReturnsConflict тестіндегі күтілетін Conflict уақытша OK мәніне ауыстырылды. API дұрыс 409 қайтарды; әдейі қате күту тестті құлатты. Қате коммит: '+failure['head_sha'][:7]+'.'),
    fig('merge-blocked.jpg',340),Spacer(1,3*mm),
    p('1-сурет. PR #17: 1 approval бар; ci-cd / test қызыл және Required деп белгіленген; Merge pull request түймесі қолжетімсіз. Сурет браузерден тікелей алынды.',SMALL),
    code('Create_DuplicateName_ReturnsConflict [FAIL]\nExpected: OK\nActual:   Conflict\nFailed: 1, Passed: 37, Total: 38\nProcess completed with exit code 1.'),Spacer(1,4*mm),
    p('Жоғарыдағы жолдар GitHub Actions журналынан алынған; уақыт белгілері мен қадам атауы ықшамдалған. Толық журнал evidence/lab05-ci/failure-ci-log.txt ішінде сақталған. Күтілген HTTP 200 мен нақты HTTP 409 айырмасы анық көрінеді.'),
    p(link('actions/runs/'+str(failure['id']),'Қызыл GitHub Actions run')+' · '+link('pull/17/commits/'+failure['head_sha'],'Әдейі қате тест коммиті')),
    p('GitHub REST күйі де mergeable_state=blocked болды. Серверге қате кодты біріктіру сұрауы жіберілген жоқ: интерфейс пен API блоктауды нақты көрсетті.',SMALL),
    PageBreak(),
    p('4. Runner және DB_PASSWORD',H),
    p('Ресми actions-runner-win-x64-2.338.0.zip архиві жүктеліп, оның SHA-256 сомасы GitHub берген мәнмен салыстырылды. Runner C:\\actions-runner каталогына, репозиторийден тыс орнатылды. Тіркеу токені журналға не Git-ке жазылған жоқ.'),
    fig('runner-idle.jpg',265),Spacer(1,3*mm),
    p('2-сурет. Settings → Actions → Runners: devops-labs-windows, Windows/X64/devops-labs белгілері және Idle күйі. API тексеруі status=online және busy=false мәндерін көрсетті.',SMALL),
    table([['Параметр','Нақты күйі'],['Іске қосу','run.cmd фондық процесте; Windows қызметі ретінде орнатылмаған'],
        ['Репозиторий құпия дерегі','DB_PASSWORD атауымен сақталған; мәні көрсетілмейді'],
        ['Құпиясөздің көзі','Жергілікті .env файлының қолданыстағы томға сәйкес мәні'],
        ['Deploy ортасы','PowerShell 7, API_PORT=8088, DB_PORT=15432']]),Spacer(1,4*mm),
    p('Құпия дерек GitHub CLI-ге stdin арқылы берілді. GitHub API тек secret атауы мен уақыт метадеректерін қайтарады; құпиясөз мәнін қайтармайды. Есепте оның мәні көрсетілмейді. Runner тіркелгі файлдары C:\\actions-runner ішінде ғана қалады.'),
    p('Қауіпсіздік шекарасы',SUB),
    p('Қоғамдық репозиторийдегі self-hosted runner жергілікті пайдаланушы құқықтарымен код орындайды. Сыртқы қатысушылардың workflow-лары үшін all_external_contributors мақұлдауы сақталды. PR тесттері hosted Ubuntu-да қалады. Бұл толық оқшаулау емес: сыртқы кодты тексермей мақұлдауға болмайды.'),
    p('Компьютер немесе runner процесі тоқтаса, ол Offline болады. Осы есеп дайындалған кезде агент Online/Idle күйінде келесі зертханалық жұмысқа қалдырылды.',SMALL),
    PageBreak(),
    p('5. Қалпына келтіру және қорытынды',H),
    p('Күтілетін код жеке коммитпен Conflict мәніне қайтарылды: '+restored['head_sha'][:7]+'. Бастапқы және қалпына келтірілген коммиттердің src, tests және workflow файлдары бірдей екені тексерілді. Қате күту түпкілікті нұсқада қалған жоқ.'),
    fig('restored-green.jpg',240),Spacer(1,3*mm),
    p('3-сурет. Тест қалпына келтірілгеннен кейінгі GitHub Actions run: Success. API мен толық логта test=success, image/deploy=skipped және 38 өткен тест көрсетілген.',SMALL),
    table([['Кезең','Коммит және нәтиже'],['Бастапқы CI',initial['head_sha'][:7]+' - 38/38, success'],
        ['Әдейі қате тест',failure['head_sha'][:7]+' - 37/38, failure; merge blocked'],
        ['Қалпына келтіру',restored['head_sha'][:7]+' - 38/38, success']]),Spacer(1,4*mm),
    p(link('actions/runs/'+str(initial['id']),'Бастапқы жасыл run')+' · '+link('actions/runs/'+str(restored['id']),'Қалпына келген жасыл run')+' · '+link('pull/17','Бес жауабы бар PR #17')),
    p('09-материалдың нәтижесі',SUB),
    p('Workflow жарияланды, 24 тексеру сәтті өтті, міндетті test пен қызыл кезде merge блокталуы дәлелденді, тест қалпына келтірілді, runner және secret дайындалды. Есепте талап етілген сілтемелер, қате жолы және шынайы суреттер берілген.'),
    p('PR әдейі ашық қалдырылды: 10-материалда оны біріктіріп, image → GHCR → жергілікті deploy → readiness smoke test және rollback орындалады. Есеп пен дәлелдер ci/pipeline тармағында жарияланады; олар main тармағына осы кезеңде біріктірілмейді.'),
    p('Шектеу: ревью үшін бір иенің екі аккаунты қолданылды. Оқытушыны қосу және алдыңғы есептердің қолмен жөндеу/сурет тармақтары өз чек-парағында қалады.',SMALL),
    p('Ресми анықтама: <link href="https://docs.github.com/en/actions/tutorials/build-and-test-code/net" color="#175E9A">GitHub Actions .NET</link>; <link href="https://docs.github.com/en/actions/reference/security/secure-use" color="#175E9A">runner қауіпсіздігі</link>. Есеп жинақтаушы скрипт арқылы сақталған дәлелдерден қайта құрастырылады; скрипт CI-ді іске қоспайды.',SMALL),
]
OUT.parent.mkdir(exist_ok=True)
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ | 09-материал | Үздіксіз интеграция',author='Есімханова Аружан Түсіпханқызы',
    subject='Қазақша есеп: CI, required test, blocked merge, self-hosted runner')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
