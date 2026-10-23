"""Build the Kazakh material 11 report from saved evidence; no network or deploy."""
from pathlib import Path
from html import escape
import json,textwrap
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,PageBreak,Table,TableStyle

REPO=Path(__file__).resolve().parents[1]
EV=REPO/'evidence/lab06-failures'
OUT=REPO/'reports/lab06-failures-report.pdf'
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
def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
    canvas.line(18*mm,16*mm,A4[0]-18*mm,16*mm)
    canvas.setFont('Arial',7);canvas.setFillColor(MUTED)
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 11')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()
load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
initial=load('initial-inspection');error=load('scenario-2-request-error');crash=load('scenario-3-auto-restart')
no=load('scenario-4-no-restart');stop=load('scenario-5-graceful-stop');final=load('final-local')
checks=load('checks');resources=load('resource-summary');ui=load('docker-desktop-inspection')
assert checks['failed']==0
def event_line(value):
    parts=[]
    for event in value['events']:
        attrs=event['Actor']['Attributes'];text=event['Action']
        if 'exitCode' in attrs:text+=' (exit='+attrs['exitCode']+')'
        if 'signal' in attrs:text+=' (signal='+attrs['signal']+')'
        parts.append(text)
    return ' → '.join(parts) or 'Тіршілік циклінің оқиғасы тіркелмеді'
story=[
    p('ВКТУ · DEVOPS · 11-МАТЕРИАЛ',SMALL),Spacer(1,10*mm),
    p('6-зертханалық жұмыс<br/>Контейнер ақауларын талдау',TITLE),
    p('1-бөлім: 1-5-тармақтар, бақылау нүктесі 6',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
        ['Университет','ВКТУ'],['Күні','2026 жылғы 23 қазан'],['Тапсырма','11-материал, 6-зертханалық жұмыстың 1-бөлімі']]),Spacer(1,6*mm),
    p('Мақсаты',SUB),
    p('HTTP сұрауының қатесін процестің тоқтауынан ажырату; Docker оқиғалары, exit code, JSON логтары және RestartCount арқылы төрт сценарийді дәлелдеу. restart: no мен unless-stopped саясатын салыстырып, штаттық тоқтаудың себебін түсіндіру.'),
    p('Нақты орындалған жұмыс',SUB),
    p('Ағымдағы main коды 89a0e2b негізінде жергілікті Docker образы құрастырылды. HTTP 500, автоматты қайта іске қосу, қайта іске қосуды өшіру және штаттық тоқтату нақты орындалды. Үш параллель CLI арнасы сақталды. 35 дәлел тексеруі сәтті өтті; Postman 4 сұрау мен 10 тексеруді қатесіз орындады.'),
    p(link('tree/main/evidence/lab06-failures','Дәлелдер')+' · '+link('tree/main/scripts/verify-lab11.py','Қайта орындау скрипті')+' · '+link('tree/main/docs/lab06-failures.md','Орындау тәртібі')),
    p('API мекенжайы - http://localhost:8088, контейнер ішіндегі порт - 8080. Бұл компьютерде 8080 портын басқа қызмет қолданады. 12-материалдың OOM, БД ақауы және unhealthy тәжірибелері осы есепке кірмейді.',SMALL),
    PageBreak(),
    p('1. Дайындау және контейнерді қарау',H),
    p('CI образының орнына әдістеме талабына сай жергілікті main құрастыруы қолданылды: devops-labs-demo-api:lab11-89a0e2b. compose.yaml тек api.restart параметрін уақытша ауыстыру үшін өзгертілді; файлдың бастапқы байттары соңында толық қайтарылды. Атаулы PostgreSQL томы жойылған жоқ.'),
    code('git switch main\ngit pull --ff-only\n$env:API_IMAGE = "devops-labs-demo-api"\n$env:API_TAG = "lab11-89a0e2b"\ndocker compose up -d --build --wait --wait-timeout 120\n$api = "http://localhost:8088"\ndocker compose ps\ndocker compose logs api --tail 20'),Spacer(1,4*mm),
    table([['Параметр','Нақты мән'],['API контейнері','devops-labs-api-1; running, healthy'],['Restart policy','unless-stopped'],
        ['Лог драйвері','json-file; max-size=10m; max-file=3'],['Ресурс шектері','Memory=268435456 байт (256 MiB); swap-пен жалпы шек 256 MiB; CPU=1'],
        ['ENTRYPOINT','["dotnet", "DemoApi.dll"] - exec пішімі'],['Бастапқы RestartCount',initial['restartCount']]]),Spacer(1,4*mm),
    p('T1, T2, T3 бақылау арналары',SUB),
    p('T1 пәрмендер мен HTTP жауаптарын жазады; T2 docker events ағынын нақты API атымен сүзеді; T3 API мен БД ресурстарын қатар өлшейді. Үш бөлек көрінетін терминал терезесінің суреті жасалмады: үш CLI арнасы параллель процестер мен файлдар арқылы тіркелді. T3 контейнер қайта жасалғанда жаңа ID-ді атауы бойынша табуы үшін --no-stream өлшемін қайталайды.'),
    code('docker events --filter container=devops-labs-api-1 --filter event=start\n  --filter event=kill --filter event=die --filter event=oom\n  --filter event=stop --filter event=health_status\ndocker stats --no-stream devops-labs-api-1 devops-labs-db-1'),
    p('T2 пәрмені терминалда бір жолмен енгізіледі; exec_* оқиғалары сүзілді. T3: '+str(resources['sampleBatches'])+' топтама, API бойынша '+str(resources['apiSamples'])+' өлшем. Контейнерді қайта жасау кезінде бір stats пәрмені EOF/exit1 берді; қате сақталды, келесі өлшемдер жалғасты.',SMALL),
    PageBreak(),
    p('2. Тапсыру кестесі: сценарийлер 2-5',H),
    table([['Сценарий','T2 оқиғалары','Exit code','Қайта іске қосу','Логтағы дерек'],
        ['2. Сұрау қатесі','die/start/kill/stop/oom жоқ','Процесс аяқталған жоқ','Жоқ; ID, StartedAt және RestartCount өзгермеді','Error; exception және стек'],
        ['3. Процестің құлауы','die(exit=1) → start → health_status: healthy','1; die оқиғасынан алынды','Иә; сол контейнердің RestartCount мәні 0 → 1','Critical; кейін PostgreSQL және іске қосылу логтары'],
        ['4. restart: no','die(exit=1); start жоқ','1; State мәні','Жоқ; 5 с бақылаудан кейін Exited (1), RestartCount=0','Critical; жаңа іске қосылу логы жоқ'],
        ['5. Штаттық тоқтату','kill(signal=15) → stop → die(exit=0)','0; State мәні','Жоқ; қолмен start жасалғанға дейін stopped','Information: Application is shutting down...']],
        [W*.17,W*.24,W*.14,W*.23,W*.22]),Spacer(1,5*mm),
    p('Кесте нақты сақталған оқиғаларға сүйенеді. Штаттық тоқтауда T2 файлы stop оқиғасын die-дан бұрын жеткізді; бұл рет әдейі өзгертілмеді. Негізгі белгілер - SIGTERM=15, exit=0, stop және автоматты start болмауы.'),
    p('Exit code пен HTTP коды екі бөлек өлшем',SUB),
    p('HTTP 500 бір сұраудың нәтижесін білдіреді. Ол контейнер процесінің exit code-ы емес. 2-сценарийде процесс тірі болғандықтан, оның аяқталу коды жоқ. 3-сценарийде қайта іске қосылған контейнердің ағымдағы State.ExitCode мәні 0 болуы мүмкін; бұрынғы 1 коды die оқиғасында сақталады.'),
    p('Дәлел сілтемелері',SUB),
    p(link('blob/main/evidence/lab06-failures/scenario-2-request-error.json','2: сұрау қатесі')+' · '+link('blob/main/evidence/lab06-failures/scenario-3-auto-restart.json','3: автоматты қайта іске қосу')),
    p(link('blob/main/evidence/lab06-failures/scenario-4-no-restart.json','4: no саясаты')+' · '+link('blob/main/evidence/lab06-failures/scenario-5-graceful-stop.json','5: штаттық тоқтату')),
    p('Әр JSON файлында UTC аралығы, контейнердің before/after күйі, HTTP жауабы, лог жазбалары және сол уақыт аралығындағы нақты оқиғалар бар. Бөлек толық T2 ағыны Compose қайта жасаған кездегі қосымша оқиғаларды да сақтайды.',SMALL),
    PageBreak(),
    p('3. Сұрау қатесі және процестің құлауы',H),
    p('2-сценарий: HTTP 500, процесс тірі',SUB),
    code('curl.exe -s -w " [%{http_code}]`n" "$api/api/chaos/error"\ndocker compose logs api --tail 3 --no-log-prefix'),Spacer(1,3*mm),
    code(json.dumps(error['http']['body'],ensure_ascii=False,indent=2)),Spacer(1,3*mm),
    p('Жауап application/problem+json пішімінде, status=500. Ішкі Chaos хабарламасы мен exception stack trace клиентке шыққан жоқ. Олар сервер логында Error деңгейімен сақталған:'),
    code('LogLevel: Error\nCategory: Microsoft.AspNetCore.Diagnostics.ExceptionHandlerMiddleware\nException: System.InvalidOperationException: Chaos: искусственная ошибка\n  at DemoApi.Controllers.ChaosController.Error()'),Spacer(1,3*mm),
    p('Толық стек бөлек лог файлында берілген; бұл қысқа үзінді негізгі белгілерін ғана көрсетеді. API контейнерінің ID-і, StartedAt және RestartCount өзгермеді; /health/live 200 қайтарды.'),
    p('3-сценарий: exit 1 және авторестарт',SUB),
    code('curl.exe -X POST "$api/api/chaos/crash"\ndocker inspect devops-labs-api-1 --format "{{.RestartCount}}"\ndocker compose logs api --since 2m --no-log-prefix'),Spacer(1,3*mm),
    p('POST /api/chaos/crash алдымен 202 қайтарады; шамамен 200 мс кейін қолданба Environment.Exit(1) шақырады. Critical логы жазылып, процесс тоқтайды. unless-stopped саясаты сол контейнерді қайта іске қосады. T2 тізбегі:'),
    code(event_line(crash)),Spacer(1,3*mm),
    p('RestartCount 0-ден 1-ге өсті, контейнер ID-і өзгермеді, StartedAt жаңарды. Readiness 200-ге оралды; бақылау жобасы мен тапсырмасы PostgreSQL-де сақталды. Бұл Compose арқылы контейнерді жаңадан жасаудан бөлек жағдай.'),
    PageBreak(),
    p('4. no саясаты және штаттық тоқтату',H),
    p('4-сценарий: автоматты қайта іске қосуды өшіру',SUB),
    p('compose.yaml ішінде тек api қызметінің restart мәні уақытша "no" деп өзгертілді. DB мен Adminer саясаттары сол қалпында қалды. Compose up --no-build --wait контейнерді жаңа конфигурациямен қайта жасады; содан кейін crash сұрауы жіберілді.'),
    code('restart: "no"\ndocker compose up -d --no-build --wait --wait-timeout 90\ncurl.exe -X POST "$api/api/chaos/crash"\nStart-Sleep 5\ndocker compose ps -a'),Spacer(1,3*mm),
    table([['Өлшем','Нәтиже'],['State.Status','exited'],['State.ExitCode','1'],['RestartCount','0'],
        ['Оқиға',event_line(no)],['Лог','Critical: Chaos: аварийное завершение процесса']]),Spacer(1,4*mm),
    p('Параметр unless-stopped мәніне қайтарылып, API қайта іске қосылды. Бақылау деректері сақталды. Compose файлының бастапқы және соңғы SHA-256 мәндері бірдей; уақытша no параметрі Git-ке енгізілген жоқ.'),
    p('5-сценарий: SIGTERM арқылы штаттық тоқтату',SUB),
    code('docker compose stop api\ndocker compose logs api --tail 5 --no-log-prefix\ndocker compose start api'),Spacer(1,3*mm),
    p('Оқиғалар: '+event_line(stop)+'. Лог: Application is shutting down...; State.ExitCode=0. SIGKILL=9 тіркелген жоқ. Контейнер қолмен start жасалғанға дейін 5 секундтық бақылауда stopped күйінде қалды.'),
    p('docker compose start api командасынан кейін API healthy болды, live/ready 200 қайтарды. Кері қайтару немесе down/up қолданылған жоқ; дәлел ретінде бастапқы ақау логтары мен оқиғалары сақталды.'),
    PageBreak(),
    p('5. Тапсырудағы екі сұраққа жауап',H),
    p('1. 2-сценарий 3-сценарийден пайдаланушы және Docker үшін несімен ерекшеленеді?',SUB),
    table([['Өлшем','2: сұрау қатесі','3: процесс тоқтайды'],['Пайдаланушыға әсері','Бір сұрау HTTP 500 қайтарады; басқа сұраулар орындала береді','Crash сұрауы 202 алуы мүмкін; қайта іске қосылу кезінде жаңа сұраулар үзіледі не қосылу қатесін алады'],
        ['Docker күйі','Процесс running/healthy; қайта іске қосу жоқ','Процесс exit 1 береді; policy рұқсат етсе, Docker қайта іске қосады'],
        ['Негізгі дәлел','Error және exception stack; lifecycle оқиғасы жоқ','Critical, die(exit=1), start, RestartCount өсімі']],
        [W*.22,W*.39,W*.39]),Spacer(1,5*mm),
    p('Осылайша, HTTP 500 саны мен контейнердің құлау саны бірдей емес. Тек docker compose ps-ке қарап 2-сценарийді анықтау мүмкін емес: контейнер healthy көрінеді. Сұрау логтары мен HTTP нәтижесі қажет.'),
    p('2. docker compose stop api орындалғанда unless-stopped неге қайта іске қоспайды?',SUB),
    p('Бұл - әкімшінің әдейі тоқтатуы. unless-stopped саясаты мұндай контейнерді автоматты көтермейді; әйтпесе оны қолмен өшіру мүмкін болмас еді. Контейнерді қайта қосу үшін docker compose start api сияқты нақты пәрмен қажет. Docker daemon қайта іске қосылса да unless-stopped қолмен тоқтатылған контейнерді көтермейді; always саясатының осы жағдайда айырмасы бар.'),
    p('Процестің өзі қателікпен аяқталғанда қолмен тоқтату белгісі қойылмайды: 3-сценарийде сондықтан авторестарт болды. 5-сценарийде SIGTERM-ді ASP.NET өңдеп, қолданбаны exit 0 арқылы аяқтады; бұл error crash емес.'),
    p('Ресми анықтамалар',SUB),
    p('<link href="https://docs.docker.com/engine/containers/start-containers-automatically/" color="#175E9A">Docker restart policies</link> · <link href="https://docs.docker.com/reference/cli/docker/container/stop/" color="#175E9A">Docker stop және сигналдар</link> · <link href="https://docs.docker.com/reference/cli/docker/system/events/" color="#175E9A">Docker events</link>'),
    p('Бұлар механизмді түсіндіретін ресми дереккөздер; кестедегі нақты нәтижелер репозиторийдегі өлшенген JSON/лог файлдарынан алынған.',SMALL),
    PageBreak(),
    p('6. Қорытынды және тапсыру құрамы',H),
    table([['Талап','Күйі'],['1: бастапқы қарау','ps, logs, LogConfig, restart policy, ресурстар және ENTRYPOINT сақталды'],
        ['2-5: төрт сценарий','HTTP, events, exit code, logs және restart нақты тексерілді'],
        ['Тапсыру кестесі','Осы есептің 3-бетінде бес бағанмен берілген'],['Сұрақтар 1 және 2','Осы есептің 6-бетінде жауап берілген'],
        ['Дәлел тексерулері',str(checks['passed'])+' сәтті, қате 0'],['Postman','4 сұрау, 10 assertion, қате 0; нақты localhost API'],
        ['Compose және деректер','Бастапқы файл толық қайтарылды; атаулы том, жоба және тапсырма сақталды']]),Spacer(1,4*mm),
    p('Docker Desktop арқылы қарау',SUB),p(escape(ui['reportText'])),
    p('Тапсыру файлдары',SUB),
    p('Бұл қазақша PDF, жұмыс нұсқаулығы, қайта орындау скрипті, бөлек Postman коллекциясы және evidence/lab06-failures ішіндегі T1/T2/T3 файлдары жария репозиторийге қосылады. Бастапқы код пен тұрақты Compose конфигурациясына мінез-құлық өзгерісі енгізілген жоқ.'),
    p('Есеп жарияланатын PR PostgreSQL қатысатын міндетті CI-ден өтеді. Біріктірілген main үшін CI/CD қайта орындалып, соңғы API version мен main SHA сәйкестігі қосымша lab11-final-verification.json файлында беріледі. Есептегі lab11-89a0e2b - жергілікті тәжірибе нұсқасы, соңғы deploy SHA-ы емес.'),
    p(link('tree/main/reports','Қазақша есептер мен ортақ мұрағат')+' · '+link('tree/main/evidence/lab06-failures/checks.json','35 тексеру')),
    p('Қауіпсіздік және шектеулер',SUB),
    p('Тәжірибелер тек localhost-тағы оқу Compose жобасында жасалды. DB_PASSWORD пен GitHub токендері есепке қосылған жоқ. Chaos crash сұрауы негізгі Postman коллекциясына енгізілмеді; оны тек айқын таңдалған тексеру скрипті орындайды. Құпия деректер көрінуі мүмкін толық inspect Config.Env жарияланбады.',SMALL),
    p('Екі GitHub аккаунты бір иеге тиесілі; техникалық Approve тәуелсіз студенттің ревьюі емес. Оқытушы логині берілмеген; бұрынғы жұмыстардың қолмен жөндеу/сурет тармақтары өз чек-парағында қалады. Осы есеп 12-15-материалдардың орындалғанын мәлімдемейді.',SMALL),
]
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ | 11-материал | Контейнер ақауларын талдау',author='Есімханова Аружан Түсіпханқызы',
    subject='Қазақша есеп: лаба 6, 1-бөлім; HTTP500, crash, restart no, graceful stop')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
