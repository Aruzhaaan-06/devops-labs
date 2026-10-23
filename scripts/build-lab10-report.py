"""Build the Kazakh material 10 report from saved evidence; no network or deploy."""
from pathlib import Path
from html import escape
import json,textwrap
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,PageBreak,Table,TableStyle,Image
from reportlab.lib.utils import ImageReader

REPO=Path(__file__).resolve().parents[1]
EV=REPO/'evidence/lab05-cd'
OUT=REPO/'reports/lab05-cd-report.pdf'
PUBLIC='https://github.com/Aruzhaaan-06/devops-labs'
W=A4[0]-36*mm
NAVY=colors.HexColor('#17324D'); INK=colors.HexColor('#223447')
PALE=colors.HexColor('#F1F5F8'); MUTED=colors.HexColor('#596A7B')
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
    w,h=ImageReader(str(path)).getSize(); scale=min(W/w,height/h)
    return Image(str(path),width=w*scale,height=h*scale,hAlign='CENTER')
def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
    canvas.line(18*mm,16*mm,A4[0]-18*mm,16*mm)
    canvas.setFont('Arial',7);canvas.setFillColor(MUTED)
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 10')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()
load=lambda n:json.loads((EV/n).read_text(encoding='utf-8-sig'))
baseline=load('baseline-runtime.json'); message=load('message-runtime.json')
manual=load('manual-rollback-timing.json'); button=load('button-rollback-timing.json')
release=load('release-run.json'); checks=load('checks.json')
assert checks['failed']==0
assert message['info']['body']['version']=='sha-349a0b1'
story=[
    p('ВКТУ · DEVOPS · 10-МАТЕРИАЛ',SMALL),Spacer(1,10*mm),
    p('5-зертханалық жұмыс<br/>Жариялау және кері қайтару',TITLE),
    p('2-бөлім: 6-9-тармақтар және үш қосымша тапсырма',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
        ['Университет','ВКТУ'],['Күні','2026 жылғы 23 қазан'],['Репозиторий','Aruzhaaan-06/devops-labs, public']]),Spacer(1,6*mm),
    p('Мақсаты',SUB),
    p('Тексерілген кодты GHCR контейнер образына айналдырып, жергілікті Docker Desktop-та іске қосу; жаңа нұсқаны, дайындықты және деректердің сақталуын дәлелдеу; бұрынғы нұсқаға қайта құрастырмай оралу және v1.0.0 релизін шығару.'),
    p('Нақты нәтиже',SUB),
    p('main үшін test → image → deploy тізбегі орындалды. Жаңа GET / жауабында hello from CI/CD хабарламасы бар. InMemory тесттері 39/39, PostgreSQL CI тесттері 39/39; тірі API-де Postman 38 сұрау мен 103 тексеруді қатесіз орындады. Қолмен және Actions батырмасы арқылы кері қайтару тексерілді.'),
    p(link('pull/18','Код пен workflow өзгерісі: PR #18')+' · '+link('releases/tag/v1.0.0','Релиз v1.0.0')),
    p('Код, пәрмендер, шынайы API жауаптары және GitHub суреттері дәлел ретінде бастапқы тілінде сақталған. Түсіндірмелер мен қорытындылар қазақ тілінде жазылды.',SMALL),
    PageBreak(),
    p('1. Алғашқы толық пайплайн',H),
    p('09-материалдың PR #17-і міндетті test пен code owner мақұлдауынан кейін squash merge арқылы біріктірілді. main коммиті 8511c6c болды. test GitHub-hosted Ubuntu-да PostgreSQL қызметімен орындалды; image образды GHCR-ға жіберді; deploy self-hosted Windows runner-де дайын образды іске қосты.'),
    fig('baseline-pipeline.jpg',280),Spacer(1,3*mm),
    p('1-сурет. Бірінші толық run: test, image және deploy - Success. Сурет нақты GitHub Actions бетінен алынған.',SMALL),
    table([['Тексеру','Нәтиже'],['main және API нұсқасы','8511c6c → sha-8511c6c'],
        ['Образ','ghcr.io/aruzhaaan-06/devops-labs:sha-8511c6c'],
        ['Дайындық','/health/live = 200, /health/ready = 200'],
        ['Деректер','Жоба мен тапсырма жасалып, екі кері қайтаруға дейін сақталды']]),Spacer(1,4*mm),
    p(link('actions/runs/39926367307','Толық бастапқы run 39926367307')),
    p('Осы компьютерде 8080 портын бұрыннан басқа қызмет қолданады. Сондықтан хосттағы API_PORT=8088, ал контейнер ішіндегі порт 8080 күйінде қалды. DB_PORT=15432 және COMPOSE_SUBNET=10.254.54.0/24 бұрынғы жұмыстармен үйлестірілді.',SMALL),
    PageBreak(),
    p('2. Жаңа хабарлама және тексерулер',H),
    p('feat/info-message тармағында InfoResponse моделіне string Message қосылды. GET / бұрынғы service, version, host өрістерін сақтап, hello from CI/CD хабарламасын қайтарады. PR #18 жасыл test пен мақұлдаудан кейін біріктірілді; жаңа main - 349a0b1.'),
    code(json.dumps(message['info']['body'],ensure_ascii=False,indent=2)),Spacer(1,4*mm),
    table([['Тексеру','Нәтиже'],['Жергілікті InMemory','39/39: 7 unit және 32 integration тест'],
        ['PR және main PostgreSQL CI','39/39, failure жоқ'],['Postman, нақты Docker API','38 сұрау, 103 assertion, қате 0'],
        ['Жаңа интеграциялық тест','Service, Message, APP_VERSION және бос емес Host тексеріледі'],
        ['Коллекцияға қосылған сұрау','GET /: HTTP 200, Service, Message, Version - 4 тексеру']]),Spacer(1,4*mm),
    p('Postman localhost:8088 мекенжайындағы нақты PostgreSQL қолданатын контейнерге жіберілді; expectedVersion=sha-349a0b1 мәні берілді. Exit code - 0. Postman cloud-қа жариялау орындалған жоқ; CLI-дің тіркелгі сұраған ескертуі жергілікті тексерулерді тоқтатпады.'),
    p(link('actions/runs/39926948580','PR тексеруі')+' · '+link('actions/runs/39927177292/attempts/1','Жаңа main: бірінші іске қосу')),
    p('Қайта deploy жасаудың әсері',SUB),
    p('Сол main run-ының deploy job-ы қайта орындалды. image тегі мен Compose конфигурациясы бірдей болғанда API контейнерінің ID-і және StartedAt өзгермеді. Осы бақылау бірдей нұсқаны қайта орналастыру контейнерді қажетсіз қайта жасамағанын көрсетеді.'),
    code('API_IMAGE=ghcr.io/aruzhaaan-06/devops-labs\nAPI_TAG=sha-349a0b1\ndocker compose up -d --no-build --wait --wait-timeout 90'),
    p('SHA тегі код нұсқасын анықтайды, бірақ registry тегі техникалық тұрғыдан қайта тағайындалуы мүмкін. Нақты артефакт үшін image ID және registry manifest digest бөлек сақталды.',SMALL),
    PageBreak(),
    p('3. Қолмен кері қайтару',H),
    p('Алдыңғы қысқа SHA тегі docker image ls арқылы табылып, жергілікті кэште бар sha-8511c6c образы таңдалды. Код қайта құрастырылған жоқ. Тек осы Compose жобасының қызметтері жаңартылды; PostgreSQL-дің атаулы томы жойылған жоқ.'),
    code('$env:API_IMAGE = "ghcr.io/aruzhaaan-06/devops-labs"\n$env:API_TAG = "sha-8511c6c"\ndocker compose up -d --no-build --wait --wait-timeout 90\nInvoke-RestMethod http://localhost:8088/\nRemove-Item Env:API_IMAGE, Env:API_TAG'),Spacer(1,4*mm),
    table([['Өлшем','Нақты нәтиже'],['Уақыт','12,823 секунд'],['Басталуы','Бірінші Compose пәрменінің алдындағы сәт'],
        ['Аяқталуы','GET / ескі version мәнін бірінші растаған сәт'],['Ескі нұсқа','sha-8511c6c; message өрісі жоқ'],
        ['Деректер','Бақылау жобасы мен тапсырмасы бастапқы JSON мәндерімен бірдей'],
        ['Том','devops-labs_pgdata сақталды']]),Spacer(1,4*mm),
    code(json.dumps(manual['http']['body'],ensure_ascii=False,indent=2)),Spacer(1,4*mm),
    p('Дұрыс нұсқаға қайта оралу',SUB),
    p('GitHub Actions-та жаңа main run үшін Re-run all jobs орындалды. test, image және deploy қайтадан сәтті аяқталды; GET / қайтадан sha-349a0b1 және hello from CI/CD көрсетті. Бақылау жобасы мен тапсырмасы сақталды.'),
    p(link('actions/runs/39927177292/attempts/3','Re-run all jobs: үшінші әрекет')),
    p('Өлшеу PowerShell терезесіндегі шамалау арқылы емес, monotonic таймермен жасалды; UTC басталу/аяқталу сәттері manual-rollback-timing.json файлында сақталған.',SMALL),
    PageBreak(),
    p('4. Батырмамен кері қайтару және approval',H),
    p('workflow_dispatch оқиғасына міндетті tag енгізуі және бөлек rollback job қосылды. Бұл жолда test, image және deploy өткізіледі; бұрын жарияланған образ тартылады. sha-xxxxxxx немесе x.y.z пішімі тексеріледі, latest қабылданбайды. Енгізу shell мәтініне тікелей қойылмай, environment арқылы беріледі.'),
    table([['Өлшем','Нақты нәтиже'],['Run','39927957374, workflow_dispatch, success'],['Таңдалған тег','sha-8511c6c'],
        ['Уақыт','57,696 секунд'],['Өлшеу шекарасы','Dispatch сұрауы → approval/кезек → ескі GET / жауабын растау'],
        ['Нәтиже','Ескі version, message жоқ, жоба мен тапсырма сақталды']]),Spacer(1,4*mm),
    p('Бұл 57,696 секундқа approval, runner кезегі және бақылау аралығы кіреді; оны 12,823 секундтық тікелей Compose өлшемімен бірдей деп салыстыруға болмайды. Содан кейін deploy қайта орындалып, sha-349a0b1 қалпына келтірілді.'),
    fig('deploy-summary.jpg',240),Spacer(1,3*mm),
    p('2-сурет. Job summary тексерілген образ бен version мәнін көрсетеді; астында local ортасының approval жазбасы бар.',SMALL),
    p('local Environment: required reviewer - Aruzhaaan-06, protected branches ғана рұқсат етілген, әкімші айналып өте алмайды. Күту нақты API күйімен тіркелді. Мақұлдау осы оқу сценарийі үшін иенің тапсырмасымен ассистент арқылы орындалды; тәуелсіз адамның тексеруі ретінде көрсетілмейді.',SMALL),
    p(link('actions/runs/39927957374','Батырмалық кері қайтару run-ы')),
    PageBreak(),
    p('5. v1.0.0 релизі және Packages',H),
    p('Тексерілген 349a0b1 коммитіне v1.0.0 аннотацияланған Git тегі қойылып, origin-ге жіберілді. GitHub Release автоматты release notes арқылы жасалды. Тегтің test және image жұмыстары сәтті өтті; deploy және rollback skipped болды.'),
    fig('packages-tags.jpg',275),Spacer(1,3*mm),
    p('3-сурет. Packages бетінде latest, sha-349a0b1, 1.0.0 және алдыңғы sha-8511c6c тегтері бар. Сурет тег пайплайны аяқталғаннан кейін алынды.',SMALL),
    table([['Тексеру','Нәтиже'],['Тег run-ы',str(release['id'])+' - success'],['test / image','success / success'],
        ['deploy / rollback','skipped / skipped'],['API контейнері','Тег run-ының алдында және соңында ID мен StartedAt өзгермеді'],
        ['API нұсқасы','sha-349a0b1 және hello from CI/CD сақталды']]),Spacer(1,4*mm),
    p(link('actions/runs/'+str(release['id']),'Тег пайплайны')+' · '+link('releases/tag/v1.0.0','Жария релиз')),
    p('Registry-дегі 1.0.0 тегі мен қолданбаның APP_VERSION мәні екі бөлек ұғым: осы релиздегі API нұсқасы sha-349a0b1 болып қалады. Тег оқиғасы жұмыс істеп тұрған контейнерге орналастыру жүргізбеді.',SMALL),
    PageBreak(),
    p('6. Дәріс сұрақтарына жауап',H),
    p('1. PR кезінде образ неге жарияланбайды?',SUB),
    p('PR коды әлі main тармағына қабылданбаған. Бұл workflow PR үшін test job-ын ғана іске қосады; GHCR write құқығы тек image job-ына беріледі. Қабылданбаған код жергілікті runner-де орналастырылмайды.'),
    p('2. CI PostgreSQL-ді қайдан алады?',SUB),
    p('services.postgres уақытша postgres:18-alpine контейнерін іске қосады, pg_isready health check дайындықты күтеді. Storage=Postgres пен ConnectionStrings__Db тесттерді сол қызметке бағыттайды.'),
    p('3. Неге latest орнына sha тегі қолданылады?',SUB),
    p('sha тегі кодтың коммитін көрсетіп, алдыңғы нұсқаны таңдауға мүмкіндік береді; latest жылжиды. Registry тегін қайта тағайындауға болатындықтан, дәл артефактты тану үшін digest те сақталады.'),
    p('4. NAT артындағы self-hosted runner қалай байланысады?',SUB),
    p('Runner GitHub-қа өзі шығыс HTTPS қосылымын орнатып, тапсырма күтеді. Осы компьютерге сырттан ашық кіріс портын беру қажет емес.'),
    p('5. Қайта құрастырмай қалай тез ораламыз?',SUB),
    p('Бұрын жарияланған образды таңдап, API_IMAGE пен API_TAG орнатамыз. Compose up --no-build --wait орындаймыз, кейін GET / нұсқасын және readiness күйін тексереміз. Бұл жұмыста қолмен қайтару 12,823 секунд алды.'),
    p('6. image-ден deploy-ға мәндер қалай беріледі?',SUB),
    p('Step outputs → job outputs → needs.image.outputs тізбегі API_IMAGE пен API_TAG береді. Жай файл жеткіліксіз: jobs әртүрлі runner-лерде, ортақ емес дискілерде орындалады.'),
    p('7. Delivery мен Deployment айырмасы қандай?',SUB),
    p('Delivery тексерілген артефактты дайындайды; оны іске қосуға бөлек шешім қажет. Deployment сервисті де жаңартады. main push test → image → deploy жолын өтеді, бірақ осы қосымша нұсқада local approval күтеді. Тег тек образ жариялайды.'),
    p('8. Бір тегке deploy қайталанса не болады?',SUB),
    p('Образ бен Compose конфигурациясы өзгермесе, жұмыс істеп тұрған контейнер қайта жасалмайды. Бұл болжам контейнер ID және StartedAt мәндерін салыстыру арқылы нақты тексерілді.'),
    PageBreak(),
    p('7. Тапсыруға арналған қорытынды',H),
    table([['Талап','Орындалуы'],['6: алғашқы main deploy','PR #17 біріктірілді; test → image → deploy жасыл'],
        ['7: Message өзгерісі','PR #18, 39/39 тест, sha-349a0b1 және жаңа хабарлама'],
        ['8: кері қайтару','12,823 с; ескі жауап; Re-run all jobs арқылы қалпына келтіру'],
        ['9: v1.0.0','1.0.0 Packages тегі; тег deploy жасамады'],
        ['Қосымша 1','workflow_dispatch + tag + бөлек rollback; нақты run сәтті'],
        ['Қосымша 2','Job summary тексерілген Deployed image және version көрсетеді'],
        ['Қосымша 3','local, required reviewer, күту және approval дәлелі'],
        ['Жинақталған тексеру',str(checks['passed'])+' шарт сәтті, қате '+str(checks['failed'])]]),Spacer(1,4*mm),
    p('Тапсырылатын материалдар',SUB),
    p('Қазақша PDF, бастапқы код пен workflow, Postman коллекциясы, толық пайплайн және Packages суреттері, GET / жауаптары, тест нәтижелері, уақыт өлшемдері мен деректердің сақталуын дәлелдейтін JSON файлдары репозиторийде беріледі. 09-материалдағы қызыл test пен blocked merge дәлелдері өз тарихи каталогында сақталды.'),
    p(link('tree/main/evidence/lab05-cd','Осы бөлімнің дәлелдері')+' · '+link('tree/main/docs/lab05-cd.md','Орындау тәртібі')+' · '+link('tree/main/reports','Барлық қазақша есеп')),
    p('Жариялаудан кейінгі соңғы нұсқа',SUB),
    p('Бұл есеп функционалдық 349a0b1 кезеңінің өлшемдерін тіркейді. Есепті жариялайтын құжат коммиті main SHA-ын өзгертеді және CI/CD қайта орындайды. Соңғы main SHA, тірі API нұсқасы, health және файл хештері v1.0.0 релизіне lab10-final-verification.json ретінде тіркеледі. Бұл PDF ішіне өзінің болашақ коммит SHA-ын жазу қажеттілігін жояды.'),
    p('Шектеулер',SUB),
    p('Екі GitHub аккаунты бір иеге тиесілі; олармен жасалған техникалық ревью тәуелсіз топтас студенттің жұмысын дәлелдемейді. Оқытушының логині берілмеген. Бұрынғы жұмыстардағы қолмен жөндеу мен Visual Studio/Postman суреттерінің ашық тармақтары өз чек-парағында қалады. API осы компьютер мен runner жұмыс істеп тұрған кезде қолжетімді.',SMALL),
    p('Құпия дерек DB_PASSWORD secret-і арқылы беріледі; пароль мен runner credential файлдары есепке қосылған жоқ. Python скрипті тек сақталған дәлелдерден PDF жасайды, CI немесе deploy іске қоспайды.',SMALL),
]
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ | 10-материал | Жариялау және кері қайтару',author='Есімханова Аружан Түсіпханқызы',
    subject='Қазақша есеп: GHCR, CI/CD, rollback, v1.0.0, Environment local')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
