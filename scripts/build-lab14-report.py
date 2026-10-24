"""Build the Kazakh material 14 report from saved evidence; no network or deploy."""
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

REPO=Path(__file__).resolve().parents[1]
EV=REPO/'evidence/lab07-alerts'
OUT=REPO/'reports/lab07-alerts-report.pdf'
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
        lines.extend(textwrap.wrap(line,100,break_long_words=True,break_on_hyphens=False,replace_whitespace=False) or [' '])
    t=Table([[p(escape(line).replace(' ','&nbsp;'),CODE)] for line in lines],colWidths=[W])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('LEFTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t
def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
    canvas.line(18*mm,16*mm,A4[0]-18*mm,16*mm)
    canvas.setFont('Arial',7);canvas.setFillColor(MUTED)
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 14')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()

from datetime import datetime,timezone
load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
phases=load('phases');rows=load('scenario-table');pm=load('postman-results');counter=load('business-counter')
byname={s['name']:s for s in phases};poll=load('polling-reload');data=load('retained-data')
def page(title):return [PageBreak(),p(title,H)]
def tm(value):return datetime.fromisoformat(value.replace('Z','+00:00')).strftime('%H:%M:%S.%f')[:-3] if value else '-'
def num(value,digits=3):return f'{float(value):.{digits}f}'.replace('.',',')
def figure(path,caption,height=87*mm):
    im=Image(str(path));ratio=min(W/im.imageWidth,height/im.imageHeight);im.drawWidth=im.imageWidth*ratio;im.drawHeight=im.imageHeight*ratio
    return [im,Spacer(1,2*mm),p(caption,SMALL)]
story=[p('ВКТУ · DEVOPS · 14-МАТЕРИАЛ',SMALL),Spacer(1,12*mm),
    p('7-зертханалық жұмыс<br/>Дашбордтар және алерттер',TITLE),
    p('2-бөлім: 5-7-тармақтар және бизнес-метрика қосымшасы',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],['Университет','ВКТУ'],
        ['Күні','2026 жылғы 24 қазан'],['Тапсырма','14-материал; 7-зертханалық жұмыс, 2-бөлім']]),Spacer(1,5*mm),
    p('Мақсаты',SUB),p('Дашбордты Git-тегі конфигурация ретінде дамыту, нақты ақаулар арқылы алерттердің pending және firing күйлерін өлшеу. HTTP сұрауларының метрикасын сәтті сақталған тапсырмалардың бизнес-санауышымен салыстыру.'),
    p('Нәтиже',SUB),p('«Tasks created per minute» және бизнес-метрика панельдері қосылды; UID demo-api сақталды. a-e бес сценарий орындалды: 500 қателері, баяу жауап, процесс ақауы, жадтың таусылуы және API қолжетімсіздігі. Алты қажетті firing ауысуы бастапқы алерт күйлерінің журналымен расталды.'),
    p('Жад тәжірибесінің бірінші әрекетінде OOM ескертуден ерте болды; бұл нәтиже жасырылмай сақталды. Қайталанған d сценарийінде алдымен ContainerHighMemory firing, кейін OOM (exit code 137) және ContainerRestarted алынды. API қалпына келді, PostgreSQL деректері сақталды.'),
    p(link('pull/23','PR #23')+' · '+link('tree/main/evidence/lab07-alerts','Бастапқы дәлелдер')+' · '+link('blob/main/docs/lab07-alerts.md','Қайта орындау нұсқаулығы')),
    p('Тәжірибе нұсқасы - lab14-7d78755. Кестелердегі уақыт UTC: жергілікті уақытқа 5 сағат қосылады. Есеп тек нақты алынған нәтижелерді сипаттайды; соңғы main deploy бөлек тексеру файлына жазылады.',SMALL)]

story+=page('1. Дашбордты код ретінде сақтау')
story += [p('Файл: monitoring/grafana/dashboards/demo-api.json. Дашборд UID - demo-api, бума - DevOps course. Бастапқы бес панель сақталды; id=6 және id=7 жаңа панельдері қосылды.'),
    p('Tasks created per minute',SUB),code('sum(increase(http_requests_received_total{\n  job="demo-api", controller="Tasks",\n  action="Create", code="201"}[1m]))'),
    p('Соңғы минутта HTTP 201 жауабын берген Tasks/Create сұраулары есептеледі. increase өлшем терезесінің шеттерін экстраполяциялайды, сондықтан нәтиже бөлшек болуы мүмкін. Панельдің өлшемі - тапсырма/мин.'),
    p('Business tasks created per minute',SUB),code('sum(increase(demo_tasks_created_total{job="demo-api"}[1m]))'),
    p('Екінші панель HTTP жауаптарын емес, TaskService арқылы сәтті сақталған тапсырмаларды санайды. Екі панельдің дереккөзі - Prometheus, UID prometheus. Екі сұрау да Git ішінде болғандықтан, Grafana қайта жасалғанда да қалпына келеді.'),
    p('Docker Desktop-тағы нақты түзету',SUB),p('Файл контейнер ішінде жаңарды, бірақ Grafana-дағы панель саны 5 болып қалды. Себебі bind mount арқылы файл өзгерісі туралы watch оқиғасы жетпеді. Provisioning ішіне updateIntervalSeconds:20 қосылып, тек Grafana қайта іске қосылды.'),
    code('providers:\n  - name: default\n    folder: DevOps course\n    type: file\n    updateIntervalSeconds: 20\n    options:\n      path: /var/lib/grafana/dashboards'),
    p('Нәтиже: 7 панель жүктелді. Кейін description өзгертіліп, '+num(poll['observedFileEditDelaySeconds'])+' секундтан соң екінші restart жасамай API арқылы тексерілді. Файлдағы панель ID/title/PromQL жүктелген спецификациямен дәл сәйкес.'),
    p('Орындау тәсілінің шегі',SUB),p('Work браузерді басқаруға рұқсат бермеді. Сондықтан панель Classic JSON файлына тікелей енгізіліп, нақты Grafana API арқылы тексерілді. UI ішіндегі Add/Export/Copy to clipboard қадамдары орындалды деп көрсетілмейді; интерфейс суреттері ойдан жасалған жоқ.'),
    p(link('blob/main/monitoring/grafana/dashboards/demo-api.json','Дашборд JSON')+' · '+link('blob/main/evidence/lab07-alerts/polling-reload.json','Нақты polling тексеруі')+' · '+link('blob/main/evidence/lab07-alerts/grafana-provisioned.json','Grafana жауабы'))]

story+=page('2. Барлық сценарийдің уақыт кестесі')
story += [p('Күйлер Prometheus /api/v1/rules?type=alert адресінен шамамен әр секунд сайын оқылды. Кестеде алғашқы pending және firing бақылаулары берілген. Ереженің lastEvaluation және activeAt уақыттары толық JSON ішінде сақталған. Бақылау дәлдігі - шамамен бір poll аралығы; subsecond цифрлары дәл абсолют шекараға кепіл болмайды.',SMALL),
    table([['Сценарий / алерт','Басталуы UTC','pending байқалды','firing байқалды','Басталудан firing-ке, с']]+
        [[r['scenario']+'\n'+r['alert'],tm(r['startUtc']),tm(r['pendingObservedUtc']),tm(r['firingObservedUtc']),num(r['secondsStartToFiringObservation'])] for r in rows],
        [W*.30,W*.17,W*.17,W*.17,W*.19]),Spacer(1,4*mm),
    p('ContainerRestarted ережесінде for жоқ: бірінші true evaluation кезінде бірден firing болады. Сондықтан c және d/restart жолдарындағы pending ұяшығы «-»; жасанды уақыт қойылған жоқ.'),
    p('Сценарийлердің оқшаулануы',SUB),p('a аяқталған соң ApiHighErrorRate inactive болғаны, b аяқталған соң ApiSlowRequests inactive болғаны күтілді. c алдында бастапқы deploy-дан қалған ContainerRestarted сөнді. c мен d арасында толық бес минуттық терезе бітіп, ереже inactive-ке қайтқанша күтілді. Жадтың ерте OOM әрекетінен кейін де жаңа таза терезе күтілді.'),
    p('a-c - бірінші іске қосудың өзгертілмеген сәтті тәжірибелері; d-e - бөлек жалғастыруда орындалды. Екі журнал бір хронологияда сақталды. Алғашқы сәтсіз d өлшемі d-initial-premature-oom деп жеке белгіленді; кестеге сәтті d сценарийінің уақыттары енгізілді.'),
    p(link('blob/main/evidence/lab07-alerts/scenario-table.json','Уақыттар, activeAt және lastEvaluation')+' · '+link('blob/main/evidence/lab07-alerts/alerts-timeline.jsonl','Толық бастапқы күй журналы'))]

story+=page('3. a-b: қателер және баяу жауаптар')
a=byname['a-errors'];b=byname['b-slow']
story += [p('a. ApiHighErrorRate',SUB),code('1..60 | ForEach-Object {\n  curl.exe -s -o NUL http://localhost:8088/api/chaos/error\n  Start-Sleep 1\n}'),
    p(str(len(a['requests']))+' нақты сұраудың бәрі HTTP 500 берді. Процесс жұмысын жалғастырды: before/after ID және RestartCount бірдей. Ереже 5xx үлесі 5%-дан асқанда pending болды; for=30s орындалған соң firing-ке өтті. RPS панелінде 500 қатары мәселені көрсетеді.'),
    p('Сақталған API журналында Error, InvalidOperationException және «Chaos: искусственная ошибка» бар. Осы іске қосуда UI автоматты түрде қаралмады; docker logs шығысы бастапқы тілінде сақталды.'),
    p('b. ApiSlowRequests',SUB),code('1..40 | ForEach-Object {\n  curl.exe -s -o NUL "http://localhost:8088/api/chaos/slow?ms=1500"\n}'),
    p(str(len(b['requests']))+' сұрау HTTP 200 берді; ең аз өлшенген жауап '+num(min(x['seconds'] for x in b['requests']))+' с. Жауап дұрыс болғанымен, жалпы p95 >1 с шарты for=30s бойы сақталып, алерт firing болды. Latency p95 панелі бұрын ps/logs көрсете алмаған пайдаланушы күтуін анықтайды.'),
    p('Маңызды айырма',SUB),p('ApiHighErrorRate - сервер қателерінің үлесін, ApiSlowRequests - уақыт гистограммасының 95-процентилін бақылайды. Баяу сұрау міндетті түрде 500 бермейді және application Error жазбасын жасамайды. p95 үшін баяу сұраулардың үлесі жеткілікті болуы керек; бір жалғыз баяу сұрау жалпы p95-ті өзгерте бермейді.'),
    p('Қалпына келу',SUB),p('Қате және баяу сұрау циклдері тоқтаған соң жаман үлгілер минуттық терезеден бірден шықпайды. Сондықтан алерттер де бірден сөнбейді. Екі ереже inactive болғаннан кейін ғана келесі тәжірибеге көшілді.'),
    p(link('blob/main/evidence/lab07-alerts/a-errors.json','a: HTTP жауаптары және firing кесіндісі')+' · '+link('blob/main/evidence/lab07-alerts/a-errors-logs.txt','a: Error журналы')+' · '+link('blob/main/evidence/lab07-alerts/b-slow.json','b: өлшенген кідірістер'))]

story+=page('4. c: процестің авариялық аяқталуы')
c=byname['c-crash']
story += [code('curl.exe -X POST http://localhost:8088/api/chaos/crash'),
    table([['Белгі','Нәтиже'],['HTTP жауабы',str(c['requests'][0]['status'])+' Accepted; одан кейін процесс аяқталады'],['Docker оқиғалары','die(exitCode=1) → start → healthy'],
        ['Контейнер ID','Сақталды'],['RestartCount',str(c['before']['restartCount'])+' → '+str(c['after']['restartCount'])],['ContainerRestarted','firing; for жоқ'],['ApiDown','Күй журналында inactive; firing жоқ']]),Spacer(1,5*mm),
    p('Журнал мен метрика',SUB),p('Application журналы Critical деңгейінде авариялық аяқталуды, кейін жаңа процестің startup хабарларын көрсетеді. cAdvisor container_start_time_seconds мәнінің өзгеруін жазады; ереже max by(name) арқылы қатарларды біріктіріп, соңғы бес минуттағы changes мәнін есептейді.'),
    code('changes((max by (name) (\n  container_start_time_seconds{name="devops-labs-api-1"}\n))[5m:5s]) > 0'),
    p('Неге бірден pending жоқ?',SUB),p('Restart - болған оқиға. for параметрі берілмеген, сондықтан ереже оны бірінші evaluation кезінде firing деп белгілейді. Бес минуттық терезе оқиғаны біршама уақыт көрінетін етеді. Жаңа startup мәні терезеден ескі мән толық шыққанша өзгеріс ретінде сақталады.'),
    p('d-ге дейін күту',SUB),p('Бұл firing кезеңі келесі OOM-мен шатаспау үшін ереже inactive-ке оралғанша күтілді. Қауіпсіздікті әлсірету, for уақытын қысқарту немесе алертті қолмен өшіру қолданылған жоқ.'),
    p(link('blob/main/evidence/lab07-alerts/c-crash.json','c: before/after және уақыттар')+' · '+link('blob/main/evidence/lab07-alerts/c-crash-logs.txt','c: Critical/startup журналы')+' · '+link('blob/main/evidence/lab07-alerts/initial-attempt-docker-events.jsonl','c және алғашқы OOM оқиғалары'))]

story+=page('5. d: жад ескертуі және OOM')
d=byname['d-memory'];alloc=[int(x['url'].split('mb=')[1]) for x in d['requests']]
story += [p('Алғашқы әрекет неге қайталанды?',SUB),p('Әдістемедегі 80+100 MiB бөлінгенде, жүктемеден қалыптасқан бастапқы жад қосылып, процесс ContainerHighMemory үшін for=15s өтпей OOM арқылы аяқталды. Docker-де oom және die (exit code 137) бар, ал ескерту firing болмады. Бұл сәтсіз әрекет жеке дәлел ретінде толық сақталды.'),
    p('Қайталанған тәжірибе',SUB),p('Алдыңғы ContainerRestarted inactive болғаннан кейін 80 MiB, кейін 20 MiB қадамдар бөлінді. Әр қадамнан кейін docker stats өлшенді; жад кемінде 84%-ға жеткенде бөлу тоқтатылды. Ескерту нақты firing болғанша күтіліп, содан кейін қосымша 60 MiB арқылы OOM жасалды.'),
    table([['Өлшем','Нақты нәтиже'],['Бөлінген порциялар, MiB',' + '.join(map(str,alloc))],
        ['OOM алдындағы соңғы stats',num(d['memorySamples'][-1]['dockerMemoryPercent'],2)+'%'],
        ['ContainerHighMemory','pending → firing, for=15s'],['Оқиға тізбегі','oom → die (exit code 137) → start → healthy'],
        ['RestartCount',str(d['before']['restartCount'])+' → '+str(d['after']['restartCount'])],['Контейнер және БД','API ID сақталды; PostgreSQL тоқтатылған жоқ']]),Spacer(1,5*mm),
    p('Панель мен журнал',SUB),p('Working set / limit панелі жадтың сатылы өсуін, 256 MiB шегін және restart-тен кейін төмендеуін көрсетеді. OOM кезінде application соңғы Error жазбасын қалдыруға үлгермеуі мүмкін; себептің шешуші дәлелі - Docker oom/die (exit code 137). Кейін startup журналы жаңа процестің басталғанын растайды.'),
    p('Бұл сценарийде ешбір шек өзгертілген жоқ: API 256 MiB, RAM+swap 256 MiB, ескерту 80% / 15 с. Өзгергені - ақауға дейінгі жадты ескеретін бөлу порциялары. Бастапқы әрекетті сәтті ескерту тәжірибесі ретінде көрсетуге болмайды.'),
    p(link('blob/main/evidence/lab07-alerts/d-memory.json','d: өлшемдер, порциялар және firing')+' · '+link('blob/main/evidence/lab07-alerts/docker-events.jsonl','Сәтті d-e Docker оқиғалары')+' · '+link('blob/main/evidence/lab07-alerts/initial-attempt-phases.json','Алғашқы аяқталмаған d әрекеті'))]

story+=page('6. e: қолжетімсіздік және қалпына келу')
e=byname['e-down']
story += [code('docker compose stop api\n# ApiDown pending, кейін firing болғанша күту\ndocker compose start api'),
    p('Бұл жолы API әдейі тоқтатылып, /metrics қолжетімсіз күйінде 30 с-тан ұзақ ұсталды. Prometheus up=0 арқылы ApiDown pending және firing күйлерін тіркеді. API up панелі 0 көрсетеді; тоқтау кезінде жаңа application сұрау логтары болмайды.'),
    table([['Кезең','UTC уақыты немесе нәтиже'],['stop аяқталды',tm(e['stopCompletedUtc'])],['start аяқталды',tm(e['startCompletedUtc'])],
        ['Соңғы Docker health',e['after']['health']],['/health/live','200'],['/health/ready','200'],['ApiDown','API қайта басталғаннан кейін inactive']]),Spacer(1,5*mm),
    p('Деректердің сақталуы',SUB),p('10-12-материалдардың үш бақылау жобасы мен тапсырмасы бастапқы объектілерімен дәл салыстырылды. 13-материалдың 1200 InProgress тапсырмасы сақталды. Осы жұмыстың бизнес-санауыш тексеру объектілері және екі жүктеме жобасының тапсырмалары да PostgreSQL-де қалды.'),
    p('Жүктеме мен диагностика',SUB),p('Екі іске қосуда фондық load.ps1 қолданылды. Crash/stop/OOM кезінде байланыс үзілуі күтіледі; бұл жолдар load-console ішінде сақталған және сәтті сұрау ретінде саналмайды. Тәжірибе біткенде тек осы скрипт іске қосқан жүктеме процесі тоқтатылды. Өзге жобаның PostgreSQL контейнері өзгертілген жоқ.'),
    p('Нәтижені түсіндіру',SUB),p('unless-stopped қолмен stop жасалған контейнерді өздігінен қайта көтермейді. Оның healthy күйге қайтуы - нақты start пәрменінің нәтижесі. Ал c және d кезінде процестің авариялық аяқталуы restart саясаты арқылы қалпына келді.'),
    p(link('blob/main/evidence/lab07-alerts/e-down.json','e: күй және уақыттар')+' · '+link('blob/main/evidence/lab07-alerts/final.json','Тәжірибеден кейінгі API/targets')+' · '+link('blob/main/evidence/lab07-alerts/retained-data.json','Сақталған бақылау деректері'))]

story+=page('7. Тапсырудағы үш сұраққа жауап')
story += [p('1. Ақау басталғаннан firing-ке дейін неге уақыт өтеді?',SUB),
    p('Prometheus алдымен келесі scrape кезінде жаңа метриканы алуы керек: стендте аралығы 5 с. rate/increase және p95 минуттық терезеге сүйенеді, сондықтан қателер не баяу сұраулар жеткілікті үлеске жетуі тиіс. Кейін келесі evaluation күтіледі: оның аралығы да 5 с. Шарт true болғанда for=30s немесе for=15s таймері басталады.'),
    p('Бұл әрқашан «5+60+5+30» деген тұрақты қосынды емес. Минуттық терезе алдын ала толы болуы мүмкін; шекті үлес 60 с аяқталмай-ақ жиналады. for кезінде шарт жоғалса, таймер тасталады. Бақылаудың бір секундтық poll аралығы да көрген уақытқа қосымша айырма береді. Кестеде осы нақты тәжірибенің уақыттары келтірілген.'),
    p('2. c сценарийінде ApiDown неге firing болмады?',SUB),
    p('Процесс die (exit code 1) арқылы аяқталды, бірақ unless-stopped оны тез қайта бастады. ApiDown шарты up=0 күйін 30 с бойы үздіксіз талап етеді. Үзіліс бұдан қысқа болғандықтан, ұзақ қолжетімсіздік расталмады. Осы тәжірибенің күй журналында c кезінде ApiDown үнемі inactive болды; өте қысқа үзілісті scrape мүлде байқамауы да мүмкін. Restart фактісін ContainerRestarted ережесі for-сіз ұстап алды.'),
    p('3. 6-зертханалық жұмыстың 9-тармағындағы қай мәселе енді көрінеді?',SUB),
    p('Баяу, бірақ HTTP 200 қайтаратын сұрау. Бұрын контейнер healthy, процесс тірі, application Error жоқ болып, пайдаланушының ұзақ күтуі ps пен error log арқылы көрінбеді. Енді http_request_duration_seconds гистограммасы мен Latency p95 панелі кешігуді көрсетеді; p95 > 1 с / 30 с шарты ApiSlowRequests алертін іске қосады. controller/action бойынша p95 сұрауы Chaos/Slow әрекетін бөлек табуға мүмкіндік береді.'),
    p('Код, контейнер ресурсы және пайдаланушы симптомы әртүрлі дерек береді: HTTP 500 - сұрау қатесі, die1 - процесс аяқталуы, OOM (exit code 137) - жад шегінен асып өлу, up=0 - метриканы ала алмау. Диагноз үшін оларды бір оқиға деп араластыруға болмайды.')]

story+=page('8. Қосымша: бизнес-санауыш')
story += [code('private static readonly Counter TasksCreated = Metrics.CreateCounter(\n  "demo_tasks_created_total",\n  "Successfully persisted tasks created by TaskService.");\n\nvar task = await tasks.CreateAsync(projectId, title, description, dueDate, ct);\nTasksCreated.Inc();'),
    p('TaskService ішіндегі Inc репозиторий тапсырманы сәтті сақтағаннан кейін ғана орындалады. Егер жоба жоқ болса, сервис оған жетпей null қайтарады. Request validation қатесі контроллерге дейін кері қайтарылады. Сәтсіз persistence кезінде де Inc орындалмайды. Жаңа тәуелділік қосылмады: prometheus-net бұрыннан бар.'),
    table([['Нақты тексеру','Санауыш'],['Бастапқы мән',str(counter['before'])],['Бір 201 сәтті құрудан кейін',str(counter['afterSuccess'])],['400 және 404 жауаптарынан кейін',str(counter['afterRejected'])],['Процесс қайта басталса','Жаңа процестің санауышы нөлден басталады; БД тапсырмалары сақталады']]),Spacer(1,4*mm),
    p('HTTP 201 санауышымен қашан айырма болады?',SUB),p('Қалыпты HTTP жолында екі өсім жақын болуы тиіс. Бизнес-санауыш тапсырма сақталған сәтте өседі, HTTP метрикасы жауап аяқталған кезде жазылады. Сақтаудан кейін жауапты жазу/сериализациялау сәтсіз болса немесе клиент байланысын үзсе, бизнес оқиғасы болды, бірақ сәтті 201 жауап клиентке жетпеуі мүмкін. Кейін HTTP-ден тыс background job осы сервисті шақырса да бизнес-санауыш өседі.'),
    p('Бұл ерекше ақау осы жұмыста әдейі жасалған жоқ; ол семантикалық айырманы түсіндіреді. Екі counter да process lifetime-ға тиесілі; олар БД-дағы барлық тарихи тапсырманың санын білдірмейді. Өсімді rate/increase арқылы оқу restart reset-ін ескереді. TaskId/email сияқты жоғары кардиналды лейблдер қосылмады.'),
    p('Тест және Postman',SUB),p('Жаңа интеграциялық тест нақты /metrics мәнінің өзгерісін тексерді: бір сәтті сақтауда +1, 400/404 кезінде өзгеріс жоқ. Толық InMemory 40/40. Жүктеме тоқтаған соң нақты Postman '+str(pm['requests'])+' сұрау / '+str(pm['assertions'])+' тексеру, қате 0, exit code 0. Коллекция бұлтқа жарияланған жоқ.'),
    p(link('blob/main/src/DemoApi/Services/TaskService.cs','TaskService коды')+' · '+link('blob/main/tests/DemoApi.Tests/Integration/TasksApiTests.cs','Санауыш тесті')+' · '+link('blob/main/evidence/lab07-alerts/business-range.json','Бизнес өсімінің нақты қатары')+' · '+link('blob/main/evidence/lab07-alerts/http-range.json','HTTP 201 өсімінің нақты қатары'))]

story+=page('9. Жинақталған дәлелдер және шектеулер')
story += [p('Бірінші бөлімнен сақталған Target health',SUB)]
story+=figure(REPO/'evidence/lab07-metrics/screenshots/targets-up.png','1-сурет. 13-материалдағы бастапқы шынайы Chrome суреті: 3 UP. Бұл 14-материалдың жаңа скриншоты деп көрсетілмейді.',80*mm)
story += [p('13-материалдағы төрт жеке PromQL сұрауы, графиктері және түсіндірмелері сол бөлімнің PDF-інде және evidence/lab07-metrics каталогында сақталды. Осы бөлімнің соңғы targets JSON-ы қалпына келген 3 UP күйін жаңадан растайды.'),
    p('Қайта орындау',SUB),code('docker compose -f monitoring/compose.yaml up -d\npython scripts/verify-lab14.py --tag lab14-<functional-sha> --output <new-directory>\n# Жүктеме тоқтап, API қалпына келгеннен кейін:\npostman collection run postman/lab07-alerts.postman_collection.json --no-report-events'),
    p('Скрипт тек devops-labs-api-1 және нақты lab14 жергілікті тегін қабылдайды. API 256 MiB және swap 256 MiB шегін тексереді. Ол әдейі crash/OOM/stop жасайды; deploy-мен қатар іске қосуға болмайды. finally API-ді қайта іске қосып, өзі ашқан бақылау/жүктеме процестерін жабады.'),
    p('Жариялау және адал есеп беру',SUB),p('PR #23 міндетті PostgreSQL test арқылы тексеріледі, содан кейін main CI/CD іске қосылады. Техникалық ревью бір иенің екі аккаунтымен жасалады; бұл тәуелсіз жұптық ревью емес. Local approval ассистент тарапынан пайдаланушының тапсырмасы бойынша орындалады. Соңғы main/runtime, файл хештері және деректердің сақталуы lab14-final-verification.json релиз asset-інде тіркеледі.'),
    p('Браузер рұқсаты болмағандықтан UI экспорт және a-e кезінде Grafana/Dozzle-ны автоматты визуалды қарау орындалмады. Олардың орнына жүктелген Grafana спецификациясы, Prometheus жауаптары және контейнер журналдары берілді. Алғашқы OOM, жүктеменің күтілетін transport қателері және сәтті жалғастыру бір-бірінен нақты ажыратылды.',SMALL),
    p(link('pull/23','PR #23')+' · '+link('blob/main/evidence/lab07-alerts/postman-results.json','Postman нәтижесі')+' · '+link('releases/tag/v1.0.0','Релиз және соңғы тексеру')),
    p('<link href="https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/" color="#175E9A">Prometheus alerting rules</link> · <link href="https://grafana.com/docs/grafana/latest/administration/provisioning/" color="#175E9A">Grafana provisioning / polling</link>',SMALL)]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ - 7-зертханалық жұмыс, 2-бөлім - Дашбордтар және алерттер',author='Есімханова Аружан Түсіпханқызы',
    subject='14-материал | 25-ИСТК-2о | Қазақ тіліндегі есеп')
doc.build(story,onFirstPage=footer,onLaterPages=footer);print(OUT)
