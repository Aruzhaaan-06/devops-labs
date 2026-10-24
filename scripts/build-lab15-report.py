"""Build the Kazakh material 15 report from saved evidence; no network or deploy."""
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
EV=REPO/'evidence/lab08-incident'
OUT=REPO/'reports/lab08-incident-report.pdf'
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
    canvas.drawString(18*mm,11*mm,'ВКТУ | Есімханова Аружан Түсіпханқызы | 25-ИСТК-2о | 15')
    canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page));canvas.restoreState()

from datetime import datetime,timezone
from reportlab.graphics.shapes import Drawing,Line,String
from reportlab.graphics.charts.lineplots import LinePlot
import math

load=lambda name:json.loads((EV/(name+'.json')).read_text(encoding='utf-8'))
metrics=load('incident-metrics');diagnosis=load('diagnosis');recovered=load('revert-recovered')
links=load('github-links');guard=load('latency-guard');retained=load('retained-data');pm=load('postman-results')
def num(value,digits=3):return f'{float(value):.{digits}f}'.replace('.',',')
def utc(value):return datetime.fromisoformat(value.replace('Z','+00:00')).strftime('%H:%M:%S.%f')[:-3]
def epoch(value):return datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()
def page(title):return [PageBreak(),p(title,H)]
def issue(key,label):return link('issues/'+str(links['actions'][key]['number']),label)

def metric_plot():
    source=load('p95-global-range');start=source['startEpoch'];end=source['endEpoch']
    drawing=Drawing(W,225);plot=LinePlot();plot.x=36;plot.y=32;plot.width=W-48;plot.height=160;plot.joinedLines=1
    series=[];palette=[]
    for filename,color,task_only in [('p95-global-range',colors.HexColor('#185A9D'),False),('p95-actions-range',colors.HexColor('#C34F38'),True)]:
        for result in load(filename)['response']['body']['data']['result']:
            if task_only and (result['metric'].get('controller')!='Tasks' or result['metric'].get('action')!='List'):continue
            points=[]
            for t,value in result['values']:
                value=float(value)
                if math.isfinite(value):points.append((float(t)-start,value))
                elif points:
                    if len(points)>1:series.append(points);palette.append(color)
                    points=[]
            if len(points)>1:series.append(points);palette.append(color)
    assert series
    plot.data=series
    for i,color in enumerate(palette):plot.lines[i].strokeColor=color;plot.lines[i].strokeWidth=1.25
    plot.xValueAxis.valueMin=0;plot.xValueAxis.valueMax=end-start
    plot.xValueAxis.valueSteps=list(range(0,int(end-start)+1,120))
    plot.xValueAxis.labelTextFormat=lambda value:datetime.fromtimestamp(start+value,timezone.utc).strftime('%H:%M')
    plot.yValueAxis.valueMin=0;plot.yValueAxis.valueMax=2.5;plot.yValueAxis.valueStep=.5
    for axis in [plot.xValueAxis,plot.yValueAxis]:axis.labels.fontName='Arial';axis.labels.fontSize=7
    plot.yValueAxis.visibleGrid=1;plot.yValueAxis.gridStrokeColor=colors.HexColor('#DDE5EC')
    drawing.add(plot)
    for key,color in [('T1','#C17B19'),('T2','#23805A')]:
        x=plot.x+(epoch(metrics[key])-start)/(end-start)*plot.width
        drawing.add(Line(x,plot.y,x,plot.y+plot.height,strokeColor=colors.HexColor(color),strokeDashArray=[3,2]))
        drawing.add(String(x+3,plot.y+plot.height+5,key,fontName='Arial-Bold',fontSize=8,fillColor=colors.HexColor(color)))
    drawing.add(String(36,212,'p95, с',fontName='Arial-Bold',fontSize=9))
    drawing.add(String(36,12,'UTC | көк: барлық сұрау | қызыл: Tasks/List | үзік сызық: T1 және T2',fontName='Arial',fontSize=8))
    return drawing

story=[p('ВКТУ · DEVOPS · 15-МАТЕРИАЛ',SMALL),Spacer(1,12*mm),
    p('8-зертханалық жұмыс<br/>Тапсырмалар сервисіндегі инцидент',TITLE),
    p('Қорытынды жұмыс: анықтау, кері қайтару және түзету',H),
    table([['Мәлімет','Мәні'],['Орындаған','Есімханова Аружан Түсіпханқызы'],['Тобы','25-ИСТК-2о'],['Университет','ВКТУ'],['Күні','2026 жылғы 24 қазан'],['Материал','15; қорытынды 8-зертханалық жұмыс']]),Spacer(1,5*mm),
    p('Мақсаты',SUB),p('Шығарылымды пайплайн арқылы жариялау, деградацияны мониторингтен анықтау, бұрынғы нұсқаға кері қайтару, Revert PR арқылы түзету және қайталанудың алдын алу шараларын тіркеу.'),
    p('Нақты нәтиже',SUB),p('Функционалдық тестілерден өткен 1500 мс кідіріс әдейі шығарылды. ApiSlowRequests алерті іске қосылып, себеп Tasks/List әрекетінен табылды. Бұрынғы sha-cf768be нұсқасына rollback жасалды. GitHub жасаған Revert PR №28 түзетілген нұсқаны қайта жариялады. Бақылау деректері сақталды.'),
    p('Орындау шекарасы',SUB),p('Тәжірибе localhost оқу стендінде орындалды. Браузерді басқару бұғатталғандықтан UI скриншоттары жасалды деп көрсетілмейді: нақты Prometheus жауаптары, график және журналдар берілді. Оқытушы алдындағы онлайн қорғау бұл есеппен алмастырылмайды.'),
    p(link('issues/27','Инцидент №27')+' · '+link('pull/26','Нашар шығарылым PR №26')+' · '+link('pull/28','Revert PR №28')+' · '+link('releases/tag/v1.1.0','v1.1.0 релизі')),
    p('Уақыттар UTC бойынша жазылған; жергілікті уақыт UTC+5. Негізгі өлшемдер түзетілген sha-21b953a кезеңіне қатысты. Есеп пен deploy тексеруі қосылған соңғы main сәйкестігі lab15-final-verification.json арқылы бөлек расталады.',SMALL)]

story+=page('1. Бастапқы күй және жұмыс реті')
story += [table([['Қадам','Нақты орындау'],['1. Нашар шығарылым','Issue №25, feat/25-audit, PR №26; CI және merge'],['2. Анықтау','Қолмен сұрау жібермей ApiSlowRequests firing күту'],['3. Кері қайтару','Сақталған sha-cf768be тегіне workflow rollback'],['4. Инцидент','T0/T1/T2, метрикалар және себеп - issue №27'],['5. Түзету','GitHub жасаған Revert PR №28 және жаңа deploy'],['6. Постмортем','Алты бөлім, әр әрекетке жеке issue №29-31'],['7. Релиз','Жаңа v1.1.0 тегі, жасалған release notes және постмортемге сілтеме']]),Spacer(1,5*mm),
    p('Стенд',SUB),p('ASP.NET Core / .NET 10 API, PostgreSQL, Docker Desktop, PowerShell 7, GitHub Actions және self-hosted Windows runner. Prometheus, Grafana, cAdvisor және Dozzle бұрынғы monitoring жобасында жұмыс істеді. API хостта 8088, контейнер ішінде 8080 портын қолданады; әдістемедегі 8080 хост адресі осы стендте 8088 болып бейімделді.'),
    p('Бастапқы тексеру',SUB),p('main=cf768be; GET / нұсқасы sha-cf768be. Readiness 200, үш monitoring нысанасы UP, ApiSlowRequests inactive. Runner online/idle болды. Бұрынғы sha-тег rollback нысанасы ретінде алдын ала сақталды; main қорғауы мен міндетті test өшірілген жоқ.'),
    p('Жүктеме',SUB),p('Бастапқы load.ps1 жаңа №37 жобасында тапсырма құрып, InProgress күйіне ауыстырып, тізімді оқыды. Қайталану шегі 20 000, кідірісі 300 мс; басқарушы процесс түзетілген нұсқа расталған соң өзінің жүктемесін ғана тоқтатты.'),
    p(link('blob/main/evidence/lab08-incident/baseline.json','Бастапқы күй')+' · '+link('blob/main/scripts/observe-lab15.py','Нақты алертті бақылаушы'))]

story+=page('2. Функционалдық тест өткен нашар шығарылым')
story += [p('Issue №25 бойынша TaskService.ListAsync әдісі ғана өзгертілді. Сұраудың нәтижесі бұрынғыдай қалады, бірақ әр оқу 1500 мс күтеді. Сондықтан бұл мысал функционалдық дұрыстық пен жауап уақытының бөлек қасиеттер екенін көрсетеді.'),
    code('public async Task<IReadOnlyList<TaskItem>> ListAsync(\n    int? projectId, TaskItemStatus? status, CancellationToken ct)\n{\n    await Task.Delay(1500, ct); // "аудит"\n    return await tasks.ListAsync(projectId, status, ct);\n}'),
    table([['Белгі','Нәтиже'],['Ветка','feat/25-audit'],['PR','№26; Closes #25'],['PR PostgreSQL CI','40 өтті, 0 қате'],['Merge нәтижесі','4e49041b629a30791b27654a793722dc8a4c82bf'],['main PostgreSQL CI','40 өтті, 0 қате'],['Жарияланған нұсқа','sha-4e49041'],['T0: GitHub merged_at',utc(metrics['T0'])+' UTC']]),Spacer(1,5*mm),
    p('Неге тестілер жасыл?',SUB),p('Тестілер HTTP күйін, жауап мазмұнын, валидацияны және деректерді тексереді. Сұраудың 1,5 секунд күтуі сол нәтижелерді өзгертпейді. Бұрынғы deploy smoke тек /health/ready-ді оқыды; ол Tasks/List кідірісін тексермеді.'),
    p('Ревьюдің шегі',SUB),p('Екі GitHub тіркелгісі бір иеге тиесілі. Сондықтан Approve - қорғалған репозиторийдегі техникалық сценарий, тәуелсіз топтас студенттің ревьюі емес. Әдейі енгізілген кідіріс оқу инциденті екені PR ішінде ашық жазылды.'),
    p(link('pull/26','PR және diff')+' · '+link('blob/main/evidence/lab08-incident/ci-summary.json','Төрт CI іске қосуының нәтижесі'))]

story+=page('3. Алерт арқылы анықтау және себепті табу')
story += [p('Автоматты бақылаушы Prometheus ережелерін шамамен әр секунд сайын оқыды. ApiSlowRequests firing болғанға дейін қолмен API диагностикасы жасалмады. Жүктеме мен пайплайнның штаттық health тексерулері жұмысын жалғастырды.'),
    table([['Өлшем','Нақты мән'],['T1: бірінші firing бақылауы',utc(metrics['T1'])+' UTC'],['Ереже','Жалпы p95 > 1 с, for=30s'],['Себеп болған әрекет','controller=Tasks, action=List'],['Tasks/List p95',num(diagnosis['culprit']['value'][1],4)+' с'],['Алерттен кейінгі бір HTTP жауабы','200; '+num(diagnosis['postAlertProbe']['seconds'])+' с'],['Нұсқа және код','sha-4e49041; TaskService.cs, 15-жол']]),Spacer(1,4*mm),
    code('histogram_quantile(0.95,\n  sum by (le, controller, action) (\n    rate(http_request_duration_seconds_bucket{job="demo-api"}[1m])\n  )\n)'),
    p('Диагностика жолы',SUB),p('PromQL әрекетті Tasks/List деп бөлді. Тек содан кейін GET / арқылы version оқылып, оның commit-і GitHub-та ашылды. TasksController.List сұрауды TaskService.ListAsync әдісіне береді; сол әдістің 15-жолындағы Task.Delay(1500, ct) кідірістің себебі болды.'),
    p('Екі түрлі уақыт өлшемі',SUB),p('Histogram p95 bucket шекаралары бойынша жуықталады. Сондықтан '+num(diagnosis['culprit']['value'][1],4)+' с мәнін дәл 1500 мс stopwatch өлшемімен теңестіруге болмайды. Екеуі де сұраудың белгіленген 1 секунд шегінен асқанын растайды.'),
    p(link('blob/main/evidence/lab08-incident/first-firing.json','Бірінші firing')+' · '+link('blob/main/evidence/lab08-incident/diagnosis.json','PromQL, version және нақты HTTP өлшемі'))]

story+=page('4. Нақты метрикалар графигі және хронология')
story += [metric_plot(),p('1-сурет. Prometheus query_range бастапқы деректерінен құрылған график. Бұл Grafana UI скриншоты емес. Қадам - 5 секунд; NaN аралықтары нөлмен алмастырылмады. T1 - анықтау, T2 - rollback пен алерттің сөнгенін бірге растау.',SMALL),
    table([['Оқиға','UTC','Мағынасы'],['T0',utc(metrics['T0']),'PR merge; кейін CI, image және deploy бар'],['T1',utc(metrics['T1']),'Бақылаушы ApiSlowRequests firing көрді'],['T2',utc(metrics['T2']),'Ескі нұсқа расталды; ApiSlowRequests inactive']],[W*.13,W*.24,W*.63]),Spacer(1,4*mm),
    p('Анықтау: T1 - T0 = <b>'+num(metrics['detectionSeconds'])+' с</b>. Бұл санға пайплайн мен deploy да кіреді. Оны тек Prometheus scrape/evaluation кідірісі деп атау қате.'),
    p('Қалпына келу: T2 - T1 = <b>'+num(metrics['recoverySeconds'])+' с</b>. Диагностика, workflow dispatch, approval, runner кезегі, контейнерді ауыстыру және қалыпты күйді растау осы аралықта орындалды.'),
    p('Бақылау шегі',SUB),p('T0 GitHub серверінің секундтық merged_at уақытына сүйенеді. T1 және T2 - сақталған бақылау уақыттары. Миллисекундтың жазылуы абсолют шекара дәлдігін білдірмейді; бақылаушының шамамен 1 секундтық аралығы және API сұрау уақыты бар.'),
    p(link('blob/main/evidence/lab08-incident/p95-actions-range.json','Әр әрекеттің бастапқы қатары')+' · '+link('blob/main/evidence/lab08-incident/incident-metrics.json','Уақыттардың анықтамалары'))]

story+=page('5. Алдымен сервисті қалпына келтіру')
story += [p('Себеп анықталғаннан кейін түзетуді күтпей, дайын бұрынғы образға rollback жасалды. Нысана - sha-cf768be. Қозғалмалы latest тегі қолданылған жоқ; дерекқор томы жойылған жоқ.'),
    code('gh workflow run ci-cd.yml --ref main -f tag=sha-cf768be\n# Таңдалған run үшін local environment approval\n# rollback: pull existing image -> compose up -> readiness -> version'),
    table([['Тексеру','Нәтиже'],['Workflow','workflow_dispatch; rollback job - success'],['Қайтарылған нұсқа','sha-cf768be'],['T2',utc(metrics['T2'])+' UTC'],['ApiSlowRequests','inactive'],['Деректер','PostgreSQL бақылау объектілері сақталды'],['Жүктеме','Rollback кезінде жалғасты; байланыс қателері журналда қалды']]),Spacer(1,5*mm),
    p('Алерт неге бірден сөнбеуі мүмкін?',SUB),p('p95 соңғы минуттағы histogram өсіміне сүйенеді. Жаңа процесс, scrape және ережені есептеу уақыттары қатарға әсер етеді; ескі баяу үлгілердің салмағы бірден жоғалмайды. T2 тек нұсқа мен inactive күйі нақты расталғанда тіркелді.'),
    p('Шешімнің шегі',SUB),p('Local approval пайдаланушының тапсырмасы бойынша ассистентпен орындалды. Қорғау өшірілмеді және bypass қолданылмады. Бұл тәуелсіз адамның approval-ы деп көрсетілмейді. Rollback - жедел қалпына келтіру; main ішіндегі нашар commit келесі Revert PR арқылы ғана түзетіледі.'),
    p(link('blob/main/evidence/lab08-incident/T2.json','Түпкі T2 және нұсқа')+' · '+link('issues/27','Инциденттегі rollback run сілтемесі'))]

story+=page('6. GitHub Revert PR арқылы тұрақты түзету')
story += [p('GitHub серверінің revertPullRequest операциясы PR №26 өзгерісін кері қайтаратын жаңа PR №28 жасады. Бұл - GitHub Revert батырмасының серверлік баламасы; файлды қолмен бұрынғы күйге ұқсатып жазу емес. Браузер қолжетімсіз болғандықтан операция ресми API арқылы орындалды.'),
    table([['Қадам','Нәтиже'],['Revert PR','№28; сипаттамада Refs #27'],['PR test','PostgreSQL 40/40'],['Ревью','CODEOWNER екінші тіркелгімен; бір иесі бар екені көрсетілген'],['Merge және main','21b953a4b34b5f336aca46f2928ede6966fb47d2'],['main test -> image -> deploy','Барлығы success'],['Нақты version','sha-21b953a'],['Қалпына келген Tasks/List p95',num(recovered['tasksListP95Seconds']*1000)+' мс']]),Spacer(1,4*mm),
    p('Кодты салыстыру',SUB),p('Revert-тен кейін src және tests каталогтары бастапқы cf768be нұсқасымен дәл салыстырылды: айырма жоқ. Бизнес-санауыш сақталды; HTTP-контракт өзгермеді. Compose, Dockerfile, scrape және alert ережелері де өзгертілген жоқ.'),
    p('Қайта қосылу алерті',SUB),p('ContainerRestarted соңғы 5 минуттағы process start өзгерісін көрсетеді. Басқарылатын deploy-дан кейін ол уақытша firing болуы қалыпты. Соңғы тексеруде осы терезе толық өткенше күтіліп, бес ереженің бәрі inactive болғаны расталады; уақыт қысқартылмайды.'),
    p(link('pull/28','GitHub жасаған Revert PR')+' · '+link('blob/main/evidence/lab08-incident/revert-operation.json','Нақты сервер операциясы')+' · '+link('blob/main/evidence/lab08-incident/source-proof.json','Бастапқы және түзетілген код'))]

story+=page('7. Постмортем: не болды және неге болды')
story += [p('Не болды?',SUB),p('«Аудит» атауымен тізімді оқу жолына 1500 мс жасанды күту енгізілді. Сұрау HTTP 200 қайтарды, функционалдық тестілер өтті. Деградацияны ApiSlowRequests алерті анықтады.'),
    p('Әсері',SUB),p('Оқу жүктемесіндегі Tasks/List клиенттері ұзақ күтті; нақты бір жауап '+num(diagnosis['postAlertProbe']['seconds'])+' с алды. Қалпына келтірудің T1-ден есептелген уақыты '+num(metrics['recoverySeconds'])+' с. Бұл барлық клиентке әсердің дәл ұзақтығы емес: T0 - merge, ал әсер deploy-дан кейін басталған. Қайта қосылу кезіндегі 5 transport қатесі сақталды; тапсырмалар жойылған жоқ.'),
    p('Түпкі себеп',SUB),p('Әрбір оқу сұрауының тікелей жолындағы await Task.Delay(1500, ct). Аудитті орындау тәсіліне response-time бюджеті қойылмаған. Controller/action метрикалары мен root version себепті нақты commit-пен байланыстырды.'),
    p('Неге ертерек табылмады?',SUB),p('Функционалдық тестілер жауаптың дұрыстығын тексерді. Readiness дерекқорға қолжетімділікті тексерді. Екеуінде де Tasks/List жауап уақытының шегі болмады. Сондықтан жасыл пайплайн жеткілікті latency кепілдігі бола алмады.'),
    p('Не жақсы жұмыс істеді?',SUB),p('Алерт, controller/action белгілері, нұсқаны commit-пен байланыстыру, сақталған sha-тег, қорғалған PR үрдісі және дайын rollback workflow. Алдымен сервис қалпына келтіріліп, содан кейін main Revert PR арқылы түзетілді.'),
    p('Әрі қарайғы әрекеттер',SUB),p('Тез deploy smoke енгізу, жеке performance baseline дайындау және оқиғаға әрекет ету нұсқаулығын сақтау. Әр әрекетке жеке issue ашылды; орындалған және ашық қалған жұмыс ажыратылады.'),
    p('<link href="'+load('postmortem')['url']+'" color="#175E9A">Инциденттегі бастапқы постмортем түсініктемесі</link>')]

story+=page('8. Қайталанудың алдын алу және әрекеттер')
story += [table([['Issue','Әрекет және күй'],['№29','Deploy ішінде Tasks/List latency smoke; осы жұмыстың қорытынды PR-ына енгізілді'],['№30','PostgreSQL бар performance baseline; кеңейтілген follow-up ашық қалады'],['№31','Диагностика, rollback және қорғау жоспары; нұсқаулыққа енгізілді']]),Spacer(1,5*mm),
    p('Жаңа deploy шегі',SUB),p('scripts/smoke-tasks-latency.ps1 үш рет деректерді өзгертпейтін GET жібереді. Әр жауап HTTP 200 болып, 1000 мс-тан аз уақытта аяқталуы тиіс; бір сұраудың timeout мәні 5 секунд. Белгісіз projectId және Todo сүзгісі үлкен жауап көлемінің ықпалын азайтады.'),
    code('./scripts/smoke-tasks-latency.ps1 `\n  -BaseUrl "http://127.0.0.1:$env:API_PORT"'),
    table([['Нұсқа','Өлшем','Қорытынды'],['Нашар',num(guard['badMilliseconds'])+' мс','exit 1; 1000 мс шегі орындалмады']]+[['Түзетілген, үлгі '+str(s['sample']),num(s['milliseconds'])+' мс','HTTP 200; шектен төмен'] for s in guard['good']['samples']],[W*.36,W*.23,W*.41]),Spacer(1,4*mm),
    p('Нені қамтамасыз етеді?',SUB),p('Осы 1500 мс регрессиясы енді deploy job ішінде байқалмай жасыл өте алмайды. Тексеру readiness-тен кейін, Job summary-ден бұрын іске қосылады. Ол статистикалық жүктеме тесті де, автоматты rollback та емес. Шек бұзылса, оператор инцидент нұсқаулығымен кері қайтарады. Кеңейтілген жүктеме жұмысы №30 issue-де бөлек сақталды.'),
    p(issue('latency','№29: latency gate')+' · '+issue('benchmark','№30: performance baseline')+' · '+issue('runbook','№31: runbook'))]

story+=page('9. Деректер, бақылау және тексеру нәтижелері')
story += [table([['Тексеру','Нақты нәтиже'],['Нашар PR және main CI','Екі іске қосуда да PostgreSQL 40/40'],['Revert PR және main CI','Екі іске қосуда да PostgreSQL 40/40'],['Read-only Postman',str(pm['requests'])+' сұрау; '+str(pm['assertions'])+' тексеру; 0 қате'],['Ережелер','Бес ереже healthy/inactive болғанша күтілді'],['Бұрынғы деректер','10-12 бақылау объектілері; 13-тегі 1200 InProgress; 14-тегі 2231/531 тапсырма сақталды'],['Инцидент жүктемесі','№37 жоба; 1771 InProgress тапсырма; 5 transport қатесі'],['Жүктеме/бақылаушы','Өз процестері тоқтатылды; Prometheus бақылаушысының қатесі жоқ']]),Spacer(1,5*mm),
    p('Дәлелдерді тексеру',SUB),p('checks.json уақытының реті, firing фактісі, себеп болған әрекет, version/commit байланысы, rollback, GitHub Revert операциясы, кодтың дәл қалпына келуі, деректердің сақталуы және latency шегінің екі нұсқадағы нәтижесін тексереді. Бұл - сақталған өлшемдердің тексеруі; ақау сценарийі қайта орындалмайды.'),
    p('Қайта тексеру',SUB),code('postman collection run postman/lab08-incident.postman_collection.json `\n  --env-var expectedVersion=sha-<current-main> --no-report-events\npython scripts/check-lab15-evidence.py'),
    p('Маңызды шектеу',SUB),p('API/CLI жауаптары мен осы есептің графигі нақты деректерден алынды. Бірақ олар интерфейстің шынайы скриншоты деп көрсетілмейді. Браузер бұғаттауы салдарынан әдістемедегі alert/Grafana скриншоттары толықтырылмаған. Бұл тармақтың бағасын оқытушы анықтайды.'),
    p(link('tree/main/evidence/lab08-incident','Барлық бастапқы дәлелдер')+' · '+link('blob/main/postman/lab08-incident.postman_collection.json','Қайта қолданылатын коллекция'))]

story+=page('10. Қорғауға дайындық: алты сұрақ')
story += [p('1. PATCH /api/tasks/{id}/status қай жолмен өтеді?',SUB),p('TasksController.ChangeStatus алдымен TaskService.GetAsync арқылы тапсырманы алады. Ол жоқ болса 404 береді. StatusRules.CanTransition жалған болса 409 Problem жауабын контроллер жасайды. Рұқсат етілсе TaskService.ChangeStatusAsync репозиторийдің SetStatusAsync әдісін шақырады; PostgreSQL UPDATE орындалып, нәтиже 200 болып қайтады.'),
    p('2. Контейнер exit 137 арқылы аяқталды. Не істейміз?',SUB),p('Алдымен Docker events, inspect және журналды уақытпен салыстырамыз. Exit 137 жалғыз өзі OOM дәлелі емес: SIGKILL де сол кодты бере алады. oom оқиғасын, сол іске қосудың OOMKilled белгісін, working set/limit және restart уақытын тексереміз. Автоматты restart-тен кейін соңғы State ескі оқиғаны жаппауы мүмкін; сақталған events маңызды.'),
    p('3. Неге sha-тег, ал latest емес?',SUB),p('sha-тег шығарылымды нақты commit-пен байланыстырып, бұрын тексерілген нұсқаны таңдау мүмкіндігін береді. latest жаңа push сайын басқа образға ауыса алады. Образ байттарын дәл бекіту үшін digest қолданылады; бұл жұмыста нұсқа, commit және образ сәйкестігі бөлек тексеріледі.'),
    p('4. Readiness пен liveness айырмасы қандай?',SUB),p('Liveness процестің жауап беруін, readiness PostgreSQL-мен жұмысқа дайын екенін тексереді. Осы Dockerfile HEALTHCHECK ішінде /health/live шақырылады. Сондықтан БД қолжетімсіз болса контейнер healthy болып қалуы мүмкін, ал /health/ready 503 береді. Deploy smoke readiness-ті қосымша тексереді.'),
    p('5. БД құпиясөзі қайда? Өзгертсек не болады?',SUB),p('GitHub-та DB_PASSWORD Actions secret ретінде, жергілікті машинада Git-ке кірмейтін .env ішінде сақталады. Құпиясөз есепке немесе журналға шығарылмайды. PostgreSQL томы бұрын жасалса, env мәнін ғана ауыстыру БД пайдаланушысының құпиясөзін өзгертпейді; сәйкессіздік қосылу қатесін тудырады. Өзгеріс БД мен конфигурацияда келісілген түрде орындалуы тиіс.'),
    p('6. cAdvisor /metrics-тен нені бөлек көреді?',SUB),p('cAdvisor контейнердің CPU, working set, memory limit және start уақытын көреді. Қолданбаның /metrics адресі HTTP сұрау кодтарын, latency histogram және demo_tasks_created_total бизнес-санауышын береді. Екі қабат бірін-бірі толықтырады; контейнердің тірі болуы қолданушы сұрауының жылдамдығын дәлелдемейді.')]

story+=page('11. Тапсыру талаптары және он минуттық қорғау')
story += [table([['Критерий','Ұпай','Осы жұмыстың күйі'],['Жасыл test -> image -> deploy, main қорғауы','20','Қорғаныс сақталды; соңғы release/main бөлек manifest арқылы тексеріледі'],['Алертпен табу, әрекет/жол/deploy','20','Нақты firing, Tasks/List, 15-жол және sha-4e49041'],['Rollback және қалпына келу уақыты','20',num(metrics['recoverySeconds'])+' с; нақты version және inactive'],['Revert PR және deploy','15','GitHub жасаған PR №28; пайплайнмен жарияланды'],['Инцидент, суреттер, постмортем, әрекеттер','15','Хронология/постмортем/issue бар; UI скриншоттары толықтырылмаған'],['Оқытушының екі сұрағына жауап','10','Алты дайын жауап берілді; онлайн қорғау өтпеді']],[W*.46,W*.09,W*.45]),Spacer(1,4*mm),
    p('Өздігінен баға қойылмайды',SUB),p('Әдістемеде өту шегі 70 ұпай деп берілген. Бұл есеп автоматты түрде сол бағаны кепілдемейді: UI дәлелдерін, орындалған тармақтарды және онлайн жауаптарды оқытушы бағалайды.'),
    p('Қорғау жоспары',SUB),p('0-2 минут: репозиторий, main қорғауы, жасыл пайплайн және v1.1.0. 2-4 минут: алерт, controller/action, нұсқа және код жолы. 4-6 минут: rollback, T0/T1/T2 және деректердің сақталуы. 6-8 минут: Revert PR, постмортем, latency gate және ашық follow-up. 8-10 минут: оқытушының екі сұрағына жауап.'),
    p('Студент орындайтын қадамдар',SUB),p('Курс форумында слотқа жазылу, Teams/Zoom/Meet арқылы экран көрсетіп қорғау және есепті СДО-ға жүктеу. Оқытушының GitHub атауы әлі берілмеген. Бұрынғы жұмыстардағы қолмен отладка/скриншот тармақтары мен шарттары алынбаған 04-материал жалпы чек-листе сақталады.'),
    p(link('releases/tag/v1.1.0','Релиз: есеп, ортақ мұрағат және final verification')+' · '+link('blob/main/docs/lab08-incident.md','Қадамдық runbook және шектеулер'))]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=22*mm,
    title='ВКТУ - 8-зертханалық жұмыс - Тапсырмалар сервисіндегі инцидент',author='Есімханова Аружан Түсіпханқызы',
    subject='15-материал | 25-ИСТК-2о | Қазақ тіліндегі есеп')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('Kazakh incident report built')
