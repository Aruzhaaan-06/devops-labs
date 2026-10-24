"""Build the Kazakh material 13 report from saved evidence; no network or deploy."""
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
EV=REPO/'evidence/lab07-metrics'
OUT=REPO/'reports/lab07-metrics-report.pdf'
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
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 13')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()

load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
summary=load('summary');values=summary['values'];errors=load('error-requests')
load_result=load('load-results');pm=load('postman-results')
def figure(name,caption,max_height=120*mm):
    im=Image(str(EV/'screenshots'/name));ratio=min(W/im.imageWidth,max_height/im.imageHeight)
    im.drawWidth=im.imageWidth*ratio;im.drawHeight=im.imageHeight*ratio;im.hAlign='CENTER'
    return [im,Spacer(1,2*mm),p(caption,SMALL),Spacer(1,2*mm)]
def page(title):return [PageBreak(),p(title,H)]
def number(value,digits=4):return f'{float(value):.{digits}f}'.replace('.',',')
def first(name):return values[name][0]['value']
def expr(name):return load(name)['expression']

story=[p('ВКТУ · DEVOPS · 13-МАТЕРИАЛ',SMALL),Spacer(1,12*mm),
    p('7-зертханалық жұмыс<br/>Метрикалар және PromQL',TITLE),
    p('1-бөлім: мониторинг стегі, бастапқы метрикалар,<br/>жүктеме және сұраулар (1-4-тармақтар)',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],
        ['Университет','ВКТУ'],['Күні','2026 жылғы 24 қазан'],['Тапсырма','13-материал; 7-зертханалық жұмыс, 1-бөлім']]),Spacer(1,6*mm),
    p('Мақсаты',SUB),p('DemoApi сервисі мен контейнер ресурстарын Prometheus арқылы бақылау, Grafana дашбордын іске қосу, cAdvisor метрикаларын және Dozzle журналдарын оқу. Жүктеме кезінде сұрау жиілігін, p95 кідірісін, жадты және клиент қателерін PromQL арқылы өлшеу.'),
    p('Нақты нәтиже',SUB),p('Үш нысанның бәрі UP. Әдістемедегі бес және өзім құрастырған төрт PromQL сұрауы орындалды. Нақты HTTP400/409 жауаптары графикте көрінді. Жүктеме 1200 итерацияны қатесіз аяқтады; 1200 тапсырманың бәрі InProgress күйінде сақталды.'),
    p('Chrome браузерінен 13 шынайы экран суреті алынды; міндетті Target health және төрт жеке сұраудың графиктері осы есепке енгізілді. Postman: 5 сұрау, 15 тексеру, қате 0.'),
    p(link('pull/22','Мониторинг стегінің PR #22-і')+' · '+link('tree/main/monitoring','Конфигурация')+' · '+link('tree/main/evidence/lab07-metrics','Бастапқы дәлелдер')),
    p('Өлшемдер API-дің sha-e8be38f нұсқасында алынды. Негізгі сандық кесінді: 2026-10-24 16:40:13 UTC, жергілікті уақыт 21:40:13 (UTC+5). Скриншоттар бірнеше минут аралығында түсірілді; олардың сандары кесіндімен дәл бірдей болуы міндетті емес.',SMALL)]

story+=page('1. Мониторинг стегі және нысандар')
story += [table([['Құрал және порт','Нұсқа және қызметі'],['Prometheus · 9090','v3.14.0; метрикаларды жинау, сақтау және ережелерді есептеу'],
    ['Grafana · 3000','13.2.1; Prometheus дереккөзі, DevOps course / DemoApi дашборды'],
    ['cAdvisor · 8081','v0.60.5; контейнердің cgroup CPU/жад метрикалары'],['Dozzle · 8888','v11.0.1; тек devops-labs жобасының журналдары']]),Spacer(1,4*mm),
    code('docker compose -f monitoring/compose.yaml up -d\ndocker compose -f monitoring/compose.yaml exec -T prometheus promtool check config /etc/prometheus/prometheus.yml'),Spacer(1,4*mm)]
story+=figure('targets-up.png','1-сурет. Prometheus → Status → Target health: cadvisor, demo-api және prometheus - барлығы UP.',90*mm)
story += [p('prometheus.yml: scrape_interval және evaluation_interval - 5 секунд. demo-api → host.docker.internal:8088/metrics; cadvisor → cadvisor:8080/metrics; prometheus → localhost:9090/metrics. API-дің хосттағы порты 8088, контейнер ішіндегі порты 8080. host.docker.internal арқылы нақты жинау сәтті болды.'),
    p('Мониторинг жеке Compose жобасында іске қосылды. Docker автоматты адрес пулдары толғандықтан, бос 10.254.55.0/24 ішкі желісі берілді; MONITORING_SUBNET арқылы өзгертіледі. Қолданыстағы желілер мен өзге жобалар жойылған жоқ. Promtool конфигурация мен бес ереженің синтаксисін растады.'),
    p(link('blob/main/evidence/lab07-metrics/targets.json','Нысандардың JSON күйі')+' · '+link('blob/main/evidence/lab07-metrics/promtool.txt','Promtool нәтижесі'))]

story+=page('2. Бастапқы метрикалар және жүктеме')
story += [p('API метрикаларындағы controller="Tasks" лейблі TasksController класын, action="Create", "ChangeStatus", "List" лейблдері оның аттас әдістерін көрсетеді. Projects/Create - ProjectsController.Create. Қысқартылған нақты кесінді төменде; толық жолдар api-metrics.txt файлында сақталған.'),
    code('http_requests_received_total{controller="Tasks",action="Create",code="201",...}\nhttp_requests_received_total{controller="Tasks",action="ChangeStatus",code="200",...}\nhttp_requests_received_total{controller="Projects",action="Create",code="400",...}'),
    p('Жолдардағы көп нүкте басқа лейблдердің есепте ықшамдалғанын білдіреді; метрика файлы өзгертілген жоқ. Counter жинақталған HTTP жауаптарын санайды; ол бизнес оқиғасының жеке есептегіші емес.'),
    code('pwsh ./scripts/load.ps1 -BaseUrl http://localhost:8088 -DelayMs 300 -Iterations 1200\n...\niterations: 1200\ncompleted: 1200; failed: 0; project: 26'),
    p('Скрипт бір жоба құрады. Әр итерация тапсырма құрады, оны Todo → InProgress күйіне ауыстырады және Todo сүзгісімен тізім сұрайды; соңында 300 мс күтеді. Әр 20 итерацияда санауыш шығады. Iterations=0 болса, әдістемедегідей Ctrl+C-ге дейін жұмыс істейді. Қате болса, соңғы exit code нөлден өзгеше болады.'),
    p('Нақты іске қосу: жоба №26, 1200 итерация, қате 0. БД-дан 1200 InProgress тапсырмасы қайта оқылып тексерілді. Жүктеме аяқталған; деректер дәлел ретінде сақталды. Бұрынғы 10-12-материалдардың үш бақылау жобасы мен тапсырмасы өзгермеген.')]
story+=figure('cadvisor-api.png','2-сурет. cAdvisor → Docker Containers → devops-labs-api-1. Жад шегі 256 MiB; нақты метрикада 268435456 байт.',67*mm)
story += [p(link('blob/main/evidence/lab07-metrics/api-metrics.txt','API метрикалары')+' · '+link('blob/main/evidence/lab07-metrics/cadvisor-metrics.txt','cAdvisor метрикалары')+' · '+link('blob/main/evidence/lab07-metrics/load-results.json','Жүктеме нәтижесі'))]

story+=page('3. Дашборд және журналдар')
story+=figure('grafana-dashboard.png','3-сурет. DevOps course / DemoApi: UP, кодтар бойынша RPS, жалпы p95, жад/шек және API/БД CPU графиктері.',99*mm)
story += [p('Grafana дереккөзі provisioning арқылы http://prometheus:9090 адресіне қосылады; UID - prometheus. Дашборд JSON файлы Git ішінде. cAdvisor метрикаларындағы атау нақты devops-labs-api-1 атауына түзетілді. Жад сызығы 256 MiB шегінен төмен, CPU екі контейнер бойынша бөлек көрсетіледі.')]
story+=figure('dozzle-api.png','4-сурет. Dozzle: devops-labs-api-1 журналында тапсырма құру және Todo → InProgress ауысуы көрінеді.',99*mm)
story += [p('Метрика сұраулардың жиілігі мен кідірісін санмен көрсетеді; журнал нақты taskId/projectId және орындалған әрекетті түсіндіреді. Dozzle сүзгісі өзге жобалардың журналдарын интерфейске қоспайды. Журналдағы тіл дәлел ретінде өзгертілмеген.',SMALL)]

story+=page('4. Әдістемедегі бес PromQL сұрауы')
for name,title,explanation in [
    ('required-up','1. Нысандардың қолжетімділігі','Үш қатардың әрқайсысы 1: соңғы scrape сәтті. up=1 бизнес логика түгел дұрыс деген кепіл емес; ол /metrics адресінің қолжетімділігін көрсетеді.'),
    ('required-rps','2. Әрекеттер бойынша RPS','rate - соңғы минуттағы орташа өсім, өлшемі сұрау/с. Tasks/Create ≈3,0365; ChangeStatus ≈3,0547; List ≈3,0183. Контроллерсіз қатарлар health/metrics сияқты MVC-ден тыс маршруттарды да қамтуы мүмкін.'),
    ('required-p95','3. Жалпы p95 кідірісі','Негізгі кесіндіде '+number(first('required-p95'),6)+' с, яғни шамамен 7,796 мс. le лейблі histogram шекараларын сақтайды; нәтиже қоржындар арасындағы интерполяцияға тәуелді.'),
    ('required-memory','4. API жады','Working set = '+number(first('required-memory'),3)+' MiB. 1024-ке екі рет бөлу байтты MiB-ке ауыстырады; бұл Docker-дегі бүкіл контейнердің жады.'),
    ('required-cpu','5. Контейнер CPU жүктемесі','rate(counter) пайдаланылған ядролар үлесін береді. Кесіндіде API ≈0,02268 ядро, БД ≈0,01203 ядро. API үшін 1,0 ядро - Compose-тағы бір ядролық квотаға жуық жүктеме.')]:
    story += [p(title,SUB),code(expr(name).replace(',',',\n  ')),p(explanation)]
story += [p('Бес сұрау Prometheus → Query → Graph ішінде де орындалды; олардың жеке экран суреттері screenshots/required-*.png файлдарында. Негізгі бір уақытқа есептелген instant және 3 минуттық range JSON нәтижелері бөлек сақталған. Графиктер 5 минуттық аралықты көрсетеді.',SMALL)]

own=[
 ('own-created','5. Жеке сұрау: құрылған тапсырмалар','5-сурет. Соңғы минутта HTTP201 жауабымен құрылған тапсырмалар саны.',
  'Сұрау Tasks/Create/201 қатарын таңдап, increase арқылы соңғы минуттағы өсімді есептейді. sum барлық сәйкес қатарларды біріктіреді. Негізгі кесінді: '+number(first('own-created'),4)+' тапсырма/мин.',
  'Бөлшек сан - қате емес: increase өлшем терезесінің шеттерін экстраполяциялайды. Бұл барлық уақыттағы тапсырма саны да, БД-дағы нақты 1200 жолдың саны да емес. Жүктеме шамамен минутына 182 тапсырма құрды.'),
 ('own-memory','6. Жеке сұрау: жадтың шекке қатынасы','6-сурет. API working set жадының белгіленген шекке пайыздық қатынасы.',
  'Кесінді: '+number(first('own-memory'),4)+'%. Алым - working set, бөлім - 268435456 байт шек. Екі жақта да name бойынша бірдей топтау қолданылды; басқа лейблдер нәтижені қажетсіз ұзартпайды.',
  'Шегі нөлден үлкен контейнер ғана есепке алынады: >0 сүзгісі нөлге бөлуді болдырмайды. Жад 80% ескерту шегінен төмен. Working set - қолданылған жадтан белсенді емес файл кэші шегерілген көрсеткіш; ол процесс жады метрикасымен дәл бірдей болмауы мүмкін.'),
 ('own-p95','7. Жеке сұрау: әрекеттер бойынша p95','7-сурет. Әр controller/action тобы үшін p95 кідірісінің графигі.',
  'rate әр histogram қоржынының минуттық өсімін есептейді. sum by(le,controller,action) қоржын шекарасын және әрекетті сақтайды. histogram_quantile(0.95,...) әр әрекетке жеке 95-процентиль береді.',
  'Кесінді: Tasks/Create - 13,680 мс; ChangeStatus - 3,970 мс; List - 1,078 мс. Бұрын орындалған, бірақ соңғы минутта сұрауы болмаған Projects/Get, Tasks/Get және Chaos/Slow үшін NaN сақталды: осы терезеде p95 анықталмайды. Ол нөлге ауыстырылған жоқ.'),
 ('own-4xx','8. Жеке сұрау: клиент қателерінің жиілігі','8-сурет. Projects/Create/400 және Tasks/ChangeStatus/409 қатарларының жиілігі.',
  'Бос жоба атауы HTTP400 берді. Жаңа Todo тапсырмасын бірден Done күйіне ауыстыру HTTP409 берді. Сұраулар бастапқы scrape-тен кейін қайталанды, сондықтан counter өсімі rate арқылы көрінді. Екі кодтың кесіндідегі жиілігі де ≈0,03637 сұрау/с.',
  'controller/action/code бойынша топтау қай әрекеттің және қай кодтың жиілегенін көрсетеді. Бірдей уақытта бірдей санмен жасалған 400/409 сызықтары графикте қабаттасады; екеуі де аңызда және JSON ішінде бар. 4xx клиенттің жарамсыз сұрауы кері қайтарылғанын білдіреді; оны сервердің 5xx қатесімен араластырмау керек.')]
for name,title,caption,explanation,interpretation in own:
    story+=page(title)
    story += [code(expr(name).replace(',',',\n  ')),Spacer(1,4*mm)]
    story+=figure(name+'.png',caption,140*mm)
    story += [p('Түсіндіру',SUB),p(explanation),p(interpretation),p(link('blob/main/evidence/lab07-metrics/'+name+'.json','Instant және range нәтижесі')+' · '+link('blob/main/evidence/lab07-metrics/screenshots/'+name+'.png','Түпнұсқа экран суреті'))]
    if name=='own-4xx':story += [code('POST /api/projects  {"name":""} -> 400\nPOST /api/tasks  {"projectId":'+str(errors['project']['body']['id'])+',"title":"lab13-Todo-to-Done"} -> 201\nPATCH /api/tasks/'+str(errors['task']['body']['id'])+'/status  {"status":"Done"} -> 409')]

story+=page('9. Ережелер, тексеру және қорытынды')
story += [table([['Ереже','Шарты'],['ApiDown','up=0; 30 с сақталса, critical'],['ApiHighErrorRate','Соңғы минутта 5xx үлесі >5%; 30 с'],
    ['ApiSlowRequests','Жалпы p95 >1 с; 30 с'],['ContainerHighMemory','API working set / шек >80%; 15 с'],['ContainerRestarted','Соңғы 5 минутта max by(name)(start_time) өзгерген']]),Spacer(1,4*mm),
    p('Бұл бөлімде ережелердің мазмұны оқылып, синтаксисі және жүктелуі тексерілді. Ақау тудырып, барлық алертті іске қосу - келесі 14-материалдың міндеті; ол осы есепте орындалды деп көрсетілмейді.'),
    p('Тексеру',SUB),p('Нақты Prometheus API: 3/3 UP; 9 instant және 9 range сұрауы. Белсенді әрекеттердің p95 мәндері анықталған, NaN белсенді емес әрекеттер үшін сақталған. Нақты 400/409 жауаптары, API және cAdvisor бастапқы метрикалары, жүктеме журналы мен 13 шынайы скриншот Git-те сақталған. Postman CLI: 5 сұрау, 15 тексеру, exit0; cloud-қа жіберілген жоқ.'),
    p('Қауіпсіздік және қолдану шегі',SUB),p('Төрт UI тек 127.0.0.1 адресіне жарияланған. Grafana admin/admin - әдістемедегі жергілікті бастапқы кіру. cAdvisor privileged және host mount қолданады; Dozzle Docker socket-ін оқиды. Socket-ті :ro тіркеу Docker API-ге толық қауіпсіздік шекарасы бола алмайды. Стендті интернетке ашуға болмайды; Dozzle actions/shell қосылған жоқ. Құпия DB_PASSWORD файлдарға қосылмайды.'),
    p('Жариялау және қайталау',SUB),p(link('pull/22','PR #22')+' · '+link('blob/main/docs/lab07-metrics.md','Қайта орындау нұсқаулығы')+' · '+link('blob/main/postman/lab07-metrics.postman_collection.json','Postman коллекциясы')+' · '+link('releases/tag/v1.0.0','Соңғы deploy-ды тексеру файлы бар релиз')),
    p('Кейінгі main CI/CD дәл осы өлшем нұсқасының SHA-сына тең болмайды: есеп пен құжаттаманың өзі де жаңа commit жасайды. Соңғы main/runtime сәйкестігі lab13-final-verification.json релиз файлы арқылы беріледі. Бұрынғы 11 PDF өзгертілмейді. Техникалық Approve үшін бір иенің екі аккаунты қолданылады; бұл тәуелсіз жұптық ревью емес. Оқытушының GitHub атауы әлі белгісіз.',SMALL),
    p('Қорытынды',SUB),p('Метрика, ресурс және журнал бір стендте байланыстырылды. Жүктеменің сұрау жиілігі мен кідірісі өлшенді, API жады шекпен салыстырылды, 400/409 клиент қателері әрекеттер бойынша табылды. 13-материалдың 1-4-тармақтары орындалды; алерт тәжірибелері мен инцидентті талдау келесі жұмыстарға қалды.'),
    p('<link href="https://prometheus.io/docs/prometheus/3.12/querying/functions/" color="#175E9A">Prometheus: rate, increase, histogram_quantile</link> · <link href="https://github.com/google/cadvisor" color="#175E9A">cAdvisor ресми репозиторийі</link> · <link href="https://dozzle.dev/guide/getting-started" color="#175E9A">Dozzle ресми нұсқаулығы</link>',SMALL)]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ - 7-зертханалық жұмыс, 1-бөлім - Метрикалар және PromQL',author='Есімханова Аружан Түсіпханқызы',
    subject='13-материал | 25-ИСТК-2о | Қазақ тіліндегі есеп')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
