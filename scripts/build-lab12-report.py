"""Build the Kazakh material 12 report from saved evidence; no network or deploy."""
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
EV=REPO/'evidence/lab06-resources'
OUT=REPO/'reports/lab06-resources-report.pdf'
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
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 12')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()
load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
initial=load('initial');oom=load('scenario-6-oom');db=load('scenario-7-db-unavailable')
bad=load('scenario-8-unhealthy');slow=load('scenario-9-slow-response');checks=load('checks');stats=load('resource-summary')
assert checks['failed']==0
story=[
    p('ВКТУ · DEVOPS · 12-МАТЕРИАЛ',SMALL),Spacer(1,10*mm),
    p('6-зертханалық жұмыс<br/>Ресурстар және дайындық',TITLE),
    p('2-бөлім: 6-9-тармақтар және diag.ps1 қосымшасы',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
        ['Университет','ВКТУ'],['Күні','2026 жылғы 24 қазан'],['Тапсырма','12-материал; 6-зертханалық жұмыс, 2-бөлім']]),Spacer(1,6*mm),
    p('Мақсаты',SUB),
    p('Жад шегіне жеткен процестің OOM арқылы тоқтауын, БД қолжетімсіздігін, unhealthy күйін және баяу HTTP жауабын нақты ажырату. Оқиғалар, exit code, health, ресурстар мен логтарды бірге талдап, тек оқуға арналған диагностика скриптін PR арқылы жариялау.'),
    p('Нәтиже',SUB),
    p('OOM → die(exit137) → start тізбегі алынды. БД тоқтағанда live=200, ready=503, деректер сұрауы=500, бірақ API healthy және restart жоқ. Қате healthcheck unhealthy берді, автоматты restart болмады. Баяу жауап '+str(slow['delayed']['seconds']).replace('.',',')+' с ішінде 200 қайтарды.'),
    p('38 дәлел тексеруі сәтті. Нақты Postman: 5 сұрау, 11 assertion, қате 0. diag.ps1 қалыпты контейнерде және жоқ атауда тексерілді; контейнер күйін өзгертпейді. Бастапқы Compose пен бақылау деректері сақталды.'),
    p(link('tree/main/docs/lab06-resources.md','Орындау тәртібі')+' · '+link('tree/main/evidence/lab06-resources','Дәлелдер')+' · '+link('blob/main/scripts/diag.ps1','diag.ps1')),
    p('Код пен нақты пәрмен шығыстары бастапқы тілінде берілді; түсіндірмелер қазақ тілінде. 13-15-материалдар осы есепте орындалды деп көрсетілмейді.',SMALL),
    PageBreak(),
    p('1. Толық кесте: сценарийлер 2-8',H),
    p('2-5-сценарийлер - 2026 жылғы 23 қазандағы 11-материалдың сақталған нақты тәжірибелері. Олар бүгін қайта орындалды деп көрсетілмейді; бастапқы JSON SHA-256 мәндері тексерілді. 6-8-сценарийлер 24 қазанда main 2dd5a9f жергілікті құрастыруында орындалды.'),
    table([['Сценарий','T2 оқиғалары','Exit code','Қайта іске қосу','Лог және нәтиже'],
        ['2. Сұрау қатесі','Lifecycle оқиғасы жоқ','Процесс аяқталмады','Жоқ; ID/StartedAt бірдей','Error, exception/стек; HTTP500'],
        ['3. Процесс құлайды','die(1) → start → healthy','1','Иә; RestartCount 0 → 1','Critical, кейін startup'],
        ['4. restart: no','die(1), start жоқ','1','Жоқ; Exited(1)','Critical; жаңа startup жоқ'],
        ['5. Штаттық stop','kill(15) → stop → die(0)','0','Жоқ; қолмен start керек','Application is shutting down...'],
        ['6. OOM','oom → die(137) → start → healthy','137','Иә; сол ID, RestartCount 0 → 1','Жеке OOM application логы жоқ; кейін startup; шешуші дәлел - Docker оқиғасы'],
        ['7. БД жоқ','API lifecycle оқиғасы жоқ','Процесс аяқталмады','Жоқ; healthy күйінде','Error/Npgsql; live200, ready503, tasks500'],
        ['8. Қате healthcheck','health_status: unhealthy','Процесс аяқталмады','Жоқ; RestartCount=0','Health.Log: curl exit22/HTTP404; API live/ready200']],
        [W*.16,W*.24,W*.13,W*.20,W*.27]),Spacer(1,4*mm),
    p('5-сценарийде stop хабарламасы die-дан бұрын жеткізілді; нақты рет өзгертілмеді. HTTP500 мен healthcheck пәрменінің exit22 мәні API процесінің exit code-ы емес. Қайта іске қосылған ағымдағы State.ExitCode=0 бұрынғы die137 оқиғасын жоққа шығармайды.'),
    p(link('tree/main/evidence/lab06-failures','2-5: бастапқы дәлелдер')+' · '+link('blob/main/evidence/lab06-resources/part1-references.json','Тарихи файлдардың хештері')+' · '+link('blob/main/evidence/lab06-resources/t2-events.jsonl','6-9: толық T2 ағыны')),
    p('Оқу API мекенжайы - localhost:8088, контейнер ішінде 8080. T1 пәрмен/HTTP журналы, T2 оқиға ағыны және T3 қайталанған stats өлшемдері қатар орындалды. Үш бөлек көрінетін терминалдың скриншоты жасалған жоқ.',SMALL),
    PageBreak(),
    p('2. Жадтың жетіспеуі: OOM',H),
    p('Контейнер шегі - 268435456 байт, яғни 256 MiB. RAM+swap жиынтық шегі де 256 MiB, қосымша swap жоқ. Chaos leak Marshal.AllocHGlobal арқылы native жад бөледі және оны нақты толтырады; бөлінген жад босатылмайды.'),
    code('docker compose up -d --build --wait\n1..4 | ForEach-Object {\n  curl.exe -s -m 10 -X POST "$api/api/chaos/leak?mb=80"\n}\ndocker inspect devops-labs-api-1 --format "{{.State.OOMKilled}} {{.RestartCount}}"'),Spacer(1,3*mm),
    table([['Өлшем','Нақты нәтиже'],['1-сұрау','HTTP200, leakedMb=80'],['2-сұрау','HTTP200, leakedMb=160'],
        ['3-сұрау','Байланыс үзілді; жауап мәртебесі алынбады'],['T2','oom → die(exitCode=137) → start → health_status: healthy'],
        ['Авторестарт','Контейнер ID сақталды; RestartCount 0 → 1'],['Қайта іске қосылған күй','OOMKilled=false, ExitCode=0, healthy']]),Spacer(1,4*mm),
    p('Тексеру OOM расталғанда тоқтады; төртінші сұрауды жаңадан іске қосылған процеске жібермеді. Бақылау жобасы мен тапсырмасы PostgreSQL-де сақталды. OOM кезінде қолданба соңғы Error жазбасын қалдыруға үлгермеуі мүмкін; логта жаңа процестің startup жазбалары бар.'),
    p('Ресурс өлшемдерінің шегі',SUB),
    p('T3 '+str(stats['batches'])+' топтама және API бойынша '+str(stats['apiSamples'])+' үлгі сақтады. Өлшенген ең жоғары жад үлесі - '+str(stats['maxMemoryPercent']).replace('.',',')+'%. Бұл міндетті түрде шын ең жоғарғы нүкте емес: өлшемдер аралығында процесс шекке жетіп тоқтай алады. Қайта жасалу кезіндегі бір EOF/exit1 өлшемі сақталды, кейін бақылау жалғасты.'),
    p('Қайта іске қосылғаннан кейін memory.peak және memory.events жаңа cgroup күйін көрсетті: oom_kill=0. Оларды бұрынғы OOM болмады деген қорытындыға қолдануға болмайды. Тарихтың нақты дәлелі - үздіксіз сақталған oom және die137 оқиғалары.'),
    p(link('blob/main/evidence/lab06-resources/scenario-6-oom.json','OOM жауаптары, cgroup және before/after')+' · '+link('blob/main/evidence/lab06-resources/diag-after-oom.txt','OOM-нан кейінгі diag шығысы')),
    PageBreak(),
    p('3. БД ақауы және unhealthy',H),
    p('7-сценарий: тәуелділік қолжетімсіз',SUB),
    code('docker compose stop db\ncurl.exe -s -w " %{http_code}" "$api/health/live"\ncurl.exe -s -w " %{http_code}" "$api/health/ready"\ncurl.exe -s -o NUL -w "%{http_code}" "$api/api/tasks"\ndocker compose ps\ndocker compose start db'),Spacer(1,3*mm),
    table([['Белгі','Нәтиже'],['/health/live','200 Healthy: тек процесс тексеріледі'],['/health/ready','503 Unhealthy: PostgreSQL қолжетімсіз'],
        ['/api/tasks','500; логта Npgsql және Name or service not known'],['Docker','API running/healthy; ID, StartedAt, RestartCount өзгермеді']]),Spacer(1,4*mm),
    p('DB start-тен кейін ready 200-ге оралды, деректерге сұраулар қайта орындалды. API-ді қайта іске қосу қажет болмады. БД ақауын API restart-ымен түзету мүмкін емес.'),
    p('8-сценарий: қате healthcheck',SUB),
    code('healthcheck:\n  test: ["CMD", "curl", "-fsS", "http://localhost:8080/no-such-endpoint"]\n  interval: 5s\n  retries: 2\ndocker compose up -d --no-build\nStart-Sleep 40'),Spacer(1,3*mm),
    p('40 секундтан кейін Docker unhealthy көрсетті. Health.Log ішінде HTTP404 және curl exit22 жазылды. Процесс тірі: /health/live және /health/ready - 200. Контейнер ID, StartedAt және RestartCount=0 өзгермеді; T2-де тек health_status: unhealthy бар.'),
    p('Docker health мәртебесін өзі авторестартқа айналдырмайды. Бастапқы Compose байттары қайтарылып, up --no-build --wait орындалды; контейнер қайтадан healthy болды. Уақытша healthcheck Git-ке қосылмады.'),
    p(link('blob/main/evidence/lab06-resources/scenario-7-db-unavailable.json','БД ақауы')+' · '+link('blob/main/evidence/lab06-resources/scenario-8-unhealthy.json','Health.Log және restart болмауы')),
    PageBreak(),
    p('4. Баяу жауап және diag.ps1',H),
    p('9-сценарий: қате жоқ, бірақ жауап баяу',SUB),
    table([['Сұрау','Уақыт және нәтиже'],['GET /api/tasks',str(slow['normal']['seconds']).replace('.',',')+' с; HTTP200'],
        ['GET /api/chaos/slow?ms=3000',str(slow['delayed']['seconds']).replace('.',',')+' с; HTTP200, delayedMs=3000'],
        ['Docker күйі','healthy; restart және lifecycle ақауы жоқ']]),Spacer(1,4*mm),
    p('Бұл екі нақты сұраудың өлшемі, жүктеме benchmark-і немесе p95/p99 бағасы емес. Пайдаланушы үшін ұзақ күту бар, ал ps пен қате логтары мәселені көрсетпейді. Мониторингте HTTP latency histogram, p95/p99 және қажет болса tracing қолданылады; келесі зертханалық осыны дамытады.'),
    p('Қосымша: тек оқитын диагностика',SUB),
    code('pwsh -NoProfile -File scripts/diag.ps1 devops-labs-api-1\n\nStatus: running; Health: healthy\nExitCode: 0; OOMKilled: False\nRestartCount: 1; RestartPolicy: unless-stopped\nMemory limit bytes: 268435456\nMemory/CPU now: 35.37MiB / 256MiB\nDie/OOM events: oom; die(exitCode=137)'),Spacer(1,3*mm),
    p('Жоғарыда OOM-нан кейінгі нақты шығыстың ықшамдалған үзіндісі берілді; толық журналда бастапқы Docker timestamps және JSON оқиғалары сақталған. Скрипт status/health, RestartCount, memory limit, stats --no-stream, соңғы 20 лог жолын және 15 минуттағы die/oom оқиғаларын шығарады.'),
    p('Скрипт PowerShell 7-де орындалады, Config.Env оқымайды, контейнерді өзгертпейді. Бастапқы ID/StartedAt/RestartCount мәндері кейінгі мәндермен бірдей болды. Жоқ контейнер атауы Docker inspect қатесі мен нөлден өзгеше exit code берді. Логтағы password/token үлгілері бүркемеленеді.'),
    p('Docker оқиғаларының буфері шектеулі; --since 15m сол уақыттың бәрі сақталды деген кепіл емес. Ұзақ мерзімді тарих үшін T2 сияқты бөлек сақталған ағын немесе мониторинг керек.'),
    p(link('blob/main/scripts/diag.ps1','diag.ps1 коды')+' · '+link('blob/main/evidence/lab06-resources/diag-tests.json','Оң және теріс тексеру')+' · '+link('blob/main/evidence/lab06-resources/postman-results.json','Postman 5/11')),
    PageBreak(),
    p('5. Тапсырудағы бес сұраққа жауап',H),
    p('1. 2-сценарий мен 3-сценарийдің айырмасы қандай?',SUB),
    p('2-де бір HTTP сұрауы 500 алады, ал процесс пен қалған сұраулар жұмысын жалғастырады; Docker-де die/start жоқ, RestartCount өзгермейді. 3-де crash сұрауы алдымен 202 алуы мүмкін, кейін процесс exit1 арқылы аяқталады; қайта іске қосылу кезінде клиенттің қосылымы үзілуі мүмкін. Docker die/start жариялап, RestartCount өсіреді.'),
    p('2. docker compose stop api кезінде unless-stopped неге авторестарт жасамайды?',SUB),
    p('Қолмен stop - әкімшінің әдейі тоқтату ниеті. Саясат оны құрметтеп, контейнерді нақты start пәрменіне дейін көтермейді; daemon қайта іске қосылса да unless-stopped қолмен тоқтатылған контейнерді іске қоспайды. Бұл болмаса, сервисті әдейі өшіру мүмкін болмас еді.'),
    p('3. OOM-нан кейін OOMKilled=false неге болады, шын деректі қайдан табамыз?',SUB),
    p('State ағымдағы іске қосылуды сипаттайды; restart-тен кейін OOMKilled пен ExitCode қайта жазылады. RestartCount бұрын тоқтағанын көрсетеді, бірақ себебін ашпайды. Себеп үшін сақталған Docker oom/die137 оқиғалары, логтар мен мониторинг қажет. Осы тәжірибеде cgroup санауыштары да restart-тен кейін жаңа күйге қайтты.'),
    p('4. HEALTHCHECK неге ready емес, live тексереді?',SUB),
    p('Live процестің жауап бере алатынын, ready оның тәуелділіктермен бірге трафик қабылдауға дайын екенін көрсетеді. БД-ны live-қа қосып, оркестратор арқылы restart жасасақ, қысқа БД ақауы барлық API данасының қатар restart болуына әкелуі мүмкін. Тәуелділік жоқ кезде API тірі қалып, ready503 беруі тиіс. Docker-дің өзі unhealthy үшін restart жасамайтынын да ажырату қажет.'),
    p('5. Қай ақаулар docker compose ps арқылы көрінбейді?',SUB),
    p('Бір сұраудың HTTP500 қатесі, live healthcheck кезінде БД қолжетімсіздігі және жай баяу жауаптар healthy күйінің артында қалады. OOM немесе crash-тен кейін ps қайтадан Up көрсетуі мүмкін, сондықтан тарих үшін events/logs/RestartCount қажет. Ал әдейі бұзылған healthcheck unhealthy ретінде ps-те көрінеді; бұл процесс міндетті түрде тоқтады дегенді білдірмейді.'),
    PageBreak(),
    p('6. Дәрістегі өзіндік тексеру',H),
    p('1. Exit137-нің екі себебін қалай ажыратамыз?',SUB),
    p('137 - SIGKILL. OOM болса, оның алдында oom оқиғасы бар. Stop grace period аяқталса, kill signal15-тен кейін signal9 келеді; қолданба уақытында тоқтамаған. Жалғыз exit137 себебін толық ашпайды.'),
    p('2. БД-ны liveness-ке қосу неліктен қауіпті?',SUB),
    p('Оркестратор БД ақауы үшін барлық API-ді қайта іске қосып, каскадты істен шығуды күшейтуі мүмкін. Сондықтан live - процесс, ready - тәуелділік.'),
    p('3. always және unless-stopped айырмасы қандай?',SUB),
    p('Қолмен stop-тен кейін екеуі де бірден қайта көтермейді. Daemon қайта қосылғанда always қолмен тоқтатылған контейнерді көтере алады, unless-stopped оны stopped күйінде қалдырады.'),
    p('4. OOMKilled неге false болып қалады?',SUB),
    p('Бұл - жаңа іске қосылудың күйі. Бұрынғы OOM үшін die/oom оқиғасын және сақталған уақыт тізбегін қараймыз; тек inspect-ке сенбейміз.'),
    p('5. Native leak пен .NET массивінің айырмасы қандай?',SUB),
    p('Native AllocHGlobal жады GC үйіндісінің шегіне бағынбай өседі; cgroup шегінде ядро процесті өлтіруі мүмкін. Managed бөлу GC шегінде OutOfMemoryException беруі ықтимал. Әр OOM нақты орта мен бөлу жолына тәуелді; жалпы бір exit code-қа кепіл жоқ.'),
    p('6. Әр deploy exit137 берсе, алдымен нені тексереміз?',SUB),
    p('ENTRYPOINT exec пішімінде ме, PID1 SIGTERM алады ма; stop grace period пен қолданбаның shutdown timeout мәндері жеткілікті ме. Сонымен қатар oom оқиғасы бар-жоғын тексеріп, жад шегін ажыратамыз.'),
    p('7. Healthy сервис баяу болса, алдымен неге қараймыз?',SUB),
    p('Жауап ұзақтығының p95/p99 мәндері, сұрау жиілігі, CPU throttling/жад және БД сұрау уақыты қаралады. Осы бөлімде тек 0,114 және 3,027 секундтық жеке өлшем алынды, percentile есептелген жоқ.'),
    p('8. ps қай ақауларды жасырады?',SUB),
    p('Жекелеген HTTP500, тәуелділік істемеген кездегі live200 және ұзақ жауап. Қайта іске қосылып үлгерген контейнердің бұрынғы crash/OOM себебі де ps-те толық көрінбейді.'),
    PageBreak(),
    p('7. Қорытынды және тексеру шекаралары',H),
    table([['Талап','Орындалуы'],['6: жад жетіспеуі','3-сұрауда OOM; die137; авторестарт; деректер сақталды'],
        ['7: тәуелділік жоқ','live200 / ready503 / tasks500; API restart жоқ; БД қайта қосылды'],
        ['8: unhealthy','40 с, health probe404/exit22; процесс тірі; авторестарт жоқ'],
        ['9: баяу жауап','3000 мс сұрауы 3,027295 с; HTTP200, healthy'],
        ['Кесте және сұрақтар','2-8 толық кестесі; бес жауап; қосымша сегіз өзіндік жауап'],
        ['diag.ps1','PR-ға қосылады; қалыпты және жоқ контейнер тексерілді; read-only'],
        ['Дәлел тексерулері',str(checks['passed'])+' сәтті; қате 0'],['Postman','5 сұрау, 11 assertion, қате 0; нақты PostgreSQL API'],
        ['Қалпына келтіру','Compose бастапқы байттары қайтарылды; live/ready200; том сақталды']]),Spacer(1,4*mm),
    p('Жариялау және қайта орындау',SUB),
    p('Есеп, diag.ps1, қауіпсіз GET коллекциясы, тексеру скрипттері және дәлелдер PR арқылы жарияланады. Міндетті PostgreSQL CI-ден кейін main үшін test → image → deploy орындалады. Соңғы main SHA, тірі API және PDF/ZIP хештері lab12-final-verification.json ретінде v1.0.0 релизіне тіркеледі. Есептегі lab12-2dd5a9f - жергілікті тәжірибе нұсқасы.'),
    p('Қайта орындау: scripts/verify-lab12.py тек оқу стендінде нақты OOM/DB stop жасайды және уақытша healthcheck өзгертеді. scripts/check-lab12-evidence.py тек сақталған файлдарды тексереді. scripts/build-lab12-report.py PDF жасайды; Python reportlab және Windows Arial/Consolas қажет.'),
    p('Құпия дерек пен шектеулер',SUB),
    p('API 256 MiB шегімен localhost-та сыналды. DB_PASSWORD, GitHub токендері және Config.Env жарияланбады. Docker Desktop қойындылары алдыңғы бөлімде пайдаланушының растауымен қаралған; осы бөлімде CLI шығыстары қолданылды. Екі аккаунт бір иеге тиесілі, техникалық ревью тәуелсіз студенттің ревьюі емес. Оқытушы логині мен бұрынғы қолмен тексеру тармақтары өз чек-парағында қалады.',SMALL),
    p('<link href="https://docs.docker.com/engine/containers/resource_constraints/" color="#175E9A">Docker resource limits</link> · <link href="https://docs.docker.com/reference/dockerfile/#healthcheck" color="#175E9A">HEALTHCHECK</link> · <link href="https://docs.docker.com/reference/cli/docker/system/events/" color="#175E9A">Events және буфер шегі</link>',SMALL),
]
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ | 12-материал | Ресурстар және дайындық',author='Есімханова Аружан Түсіпханқызы',
    subject='Қазақша есеп: лаба6 part2, OOM137, readiness, unhealthy, slow, diag.ps1')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
