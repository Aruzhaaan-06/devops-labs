"""Validate recorded monitoring evidence; no requests, load or container mutation."""
from pathlib import Path
import json,hashlib,math
REPO=Path(__file__).resolve().parents[1];EV=REPO/'evidence/lab07-metrics'
load=lambda name:json.loads((EV/(name+'.json')).read_text(encoding='utf-8'))
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
targets=load('targets')['body']['data']['activeTargets']
check('Exactly demo-api cadvisor prometheus UP',len(targets)==3 and {t['labels']['job'] for t in targets}=={'demo-api','cadvisor','prometheus'} and all(t['health']=='up' for t in targets))
check('API scrape uses actual port8088',next(t for t in targets if t['labels']['job']=='demo-api')['scrapeUrl']=='http://host.docker.internal:8088/metrics')
summary=load('summary');check('Nine query responses',summary['queries']==9 and len(summary['values'])==9)
for name in summary['values']:
    q=load(name)
    check(name+' real nonempty vector and range',q['instant']['status']==200 and q['instant']['body']['status']=='success' and q['instant']['body']['data']['result'] and q['range']['body']['status']=='success' and q['range']['body']['data']['result'])
v=summary['values']
check('Created tasks increased',float(v['own-created'][0]['value'])>0)
check('Memory within limit',0<float(v['own-memory'][0]['value'])<100)
check('Known active actions have finite p95',all(any(s['labels'].get('controller')=='Tasks' and s['labels'].get('action')==action and math.isfinite(float(s['value'])) for s in v['own-p95']) for action in ['Create','ChangeStatus','List']))
check('Idle action p95 honestly retained NaN',any(s['value']=='NaN' for s in v['own-p95']))
check('400and409 rates positive',{s['labels']['code'] for s in v['own-4xx'] if float(s['value'])>0}>={'400','409'})
e=load('error-requests');check('Real400and409 responses',e['badProject']['status']==400 and e['conflict']['status']==409)
check('API labels match controllers',all('controller="'+s+'"' in (EV/'api-metrics.txt').read_text(encoding='utf-8') for s in ['Projects','Tasks']))
cadvisor=(EV/'cadvisor-metrics.txt').read_text(encoding='utf-8')
limits=[float(line.split('}',1)[1].split()[0]) for line in cadvisor.splitlines() if line.startswith('container_spec_memory_limit_bytes{')]
check('Real cAdvisor working set and limit',all(s in cadvisor for s in ['container_memory_working_set_bytes','name="devops-labs-api-1"']) and limits==[268435456.0])
check('Five alert rules loaded',sum(len(g['rules']) for g in load('rules')['body']['data']['groups'])==5)
check('Promtool passed',(EV/'promtool.txt').read_text(encoding='utf-8').count('SUCCESS')==3)
l=load('load-results');check('1200 iterations stored then stopped',l['iterations']==l['tasksInDatabase']==1200 and l['failed']==0 and l['allInProgress'] and l['stopped'])
check('Postman5requests15assertions zero failures',all(load('postman-results')[k]==v for k,v in {'requests':5,'assertions':15,'failed':0,'exitCode':0,'cloudPublished':False}.items()))
check('Three previous data markers retained',len(load('retained-markers'))==3 and all(m['preserved'] for m in load('retained-markers')))
shots=load('screenshots');check('13 actual screenshot hashes',len(shots)==13 and all(hashlib.sha256((EV/'screenshots'/s['file']).read_bytes()).hexdigest()==s['sha256'] for s in shots))
from report_history import historical_pdf_matches
report=load('report-validation');check('Historical Kazakh PDF10pages24links preserved in Git',report['pages']==10 and report['links']==24 and report['language']=='kk' and historical_pdf_matches(REPO,'lab07-metrics-report.pdf',report['sha256']))
d=load('deliverables');check('Historical 12reports94pages prior11 preserved in Git',d['totalReports']==12 and d['totalPages']==94 and len(d['historicalPdfSha256'])==11 and all(historical_pdf_matches(REPO,n,h) for n,h in d['historicalPdfSha256'].items()))
result={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'scope':'Saved real monitoring run, not a current live health monitor'}
(EV/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result['passed'],'passed;',result['failed'],'failed')
for row in checks:
    if not row['passed']:print('FAILED',row['name'])
raise SystemExit(1 if result['failed'] else 0)
