"""Validate recorded lab7 part2 evidence, without repeating dangerous failures."""
from pathlib import Path
from datetime import datetime
import json,hashlib
REPO=Path(__file__).resolve().parents[1];EV=REPO/'evidence/lab07-alerts'
load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)})
def epoch(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
phases=load('phases');byname={p['name']:p for p in phases};rows=load('scenario-table')
timeline=[json.loads(s) for s in (EV/'alerts-timeline.jsonl').read_text(encoding='utf-8').splitlines()]
check('Five completed scenarios',set(byname)=={'a-errors','b-slow','c-crash','d-memory','e-down'} and all('endEpoch' in p for p in phases))
check('Six actual firings',len(rows)==6 and all(r['firingObservedUtc'] for r in rows))
check('Pending retained for timed rules',all(r['pendingObservedUtc'] and epoch(r['firingObservedUtc'])>epoch(r['pendingObservedUtc']) for r in rows if r['forSeconds']>0))
check('No invented pending for restart rule',all(r['pendingObservedUtc'] is None and r['forSeconds']==0 for r in rows if r['alert']=='ContainerRestarted'))
check('Each timed firing exceeds configured for',all(r['secondsActiveToFiringEvaluation']>=r['forSeconds'] for r in rows))
check('Timeline retains original failed memory attempt',any(o['phase']=='d-initial-premature-oom' for o in timeline))
check('Observer error free',load('observer-errors')==[])
a=byname['a-errors'];b=byname['b-slow'];c=byname['c-crash'];d=byname['d-memory'];e=byname['e-down']
check('a sixty real500',len(a['requests'])==60 and all(r['status']==500 for r in a['requests']))
check('a no process restart',a['before']['id']==a['after']['id'] and a['before']['restartCount']==a['after']['restartCount'])
check('b forty real slow200',len(b['requests'])==40 and all(r['status']==200 and r['seconds']>=1.4 for r in b['requests']))
check('c accepted then same-container restart',c['requests'][0]['status']==202 and c['before']['id']==c['after']['id'] and c['after']['restartCount']==c['before']['restartCount']+1)
check('c ApiDown never firing in retained interval',all(r['state']=='inactive' for o in timeline if c['startEpoch']<=o['epoch']<=c['endEpoch'] for g in o['groups'] for r in g['rules'] if r['name']=='ApiDown'))
before_d=[o for o in timeline if o['epoch']<d['startEpoch']]
check('d begins after prior restart alert inactive',next(r['state'] for g in before_d[-1]['groups'] for r in g['rules'] if r['name']=='ContainerRestarted')=='inactive')
check('d measured high memory before OOM',d['memorySamples'][-1]['dockerMemoryPercent']>=84 and len(d['requests'])>=2)
memory=next(r for r in rows if r['alert']=='ContainerHighMemory');restart=next(r for r in rows if r['scenario']=='d-memory' and r['alert']=='ContainerRestarted')
check('d warning firing precedes restart firing',epoch(memory['firingObservedUtc'])<epoch(restart['firingObservedUtc']))
check('d restarts same API once',d['before']['id']==d['after']['id'] and d['after']['restartCount']==d['before']['restartCount']+1 and d['after']['health']=='healthy')
events=[json.loads(s) for s in (EV/'docker-events.jsonl').read_text(encoding='utf-8').splitlines()]
old_events=[json.loads(s) for s in (EV/'initial-attempt-docker-events.jsonl').read_text(encoding='utf-8').splitlines()]
check('Actual new OOM and137',any(x['Action']=='oom' for x in events) and any(x['Action']=='die' and x['Actor']['Attributes'].get('exitCode')=='137' for x in events))
check('Actual original crash1 and prematureOOM137',any(x['Action']=='die' and x['Actor']['Attributes'].get('exitCode')=='1' for x in old_events) and any(x['Action']=='die' and x['Actor']['Attributes'].get('exitCode')=='137' for x in old_events))
check('e intentional stop and start healthy',epoch(e['startCompletedUtc'])>epoch(e['stopCompletedUtc']) and e['after']['health']=='healthy')
check('Final healthy live ready and load stopped',load('final')['inspection']['health']=='healthy' and load('final')['live']['status']==load('final')['ready']['status']==200 and load('final')['loadStopped'])
targets=load('final')['targets']['body']['data']['activeTargets'];check('Final3UP',len(targets)==3 and all(t['health']=='up' for t in targets))
bc=load('business-counter');check('Business counter increments successful persistence only',bc['afterSuccess']==bc['before']+1 and bc['afterRejected']==bc['afterSuccess'] and bc['bad']['status']==400 and bc['missing']['status']==404)
dash=load('grafana-provisioned');check('Loaded7panels and UID retained',dash['metadata']['name']=='demo-api' and len(dash['spec']['panels'])==7 and any(p['title']=='Tasks created per minute' for p in dash['spec']['panels']))
check('Provisioned expressions match Git file',load('dashboard-provisioning')['fileMatchesPanelExpressions'])
check('Filesystem polling fix verified',load('polling-reload')['updateIntervalSeconds']==20 and load('polling-reload')['fileDescriptionPropagatedWithoutSecondRestart'])
check('InMemory40andfocused1passed',sorted(int(t['passed']) for t in load('local-tests'))==[1,40] and all(int(t['failed'])==0 for t in load('local-tests')))
check('Postman10requests17assertions nofailures',all(load('postman-results')[k]==v for k,v in {'requests':10,'assertions':17,'failed':0,'exitCode':0,'cloudPublished':False}.items()))
check('Historical markers and1200tasks retained',len(load('retained-data')['markers'])==3 and all(m['preserved'] for m in load('retained-data')['markers']) and load('retained-data')['lab13Tasks']==1200)
check('Permanent Compose alert config workflow unchanged',all(load('unchanged-config').values()))
check('Expected Error and Critical actual logs',all(term in (EV/'a-errors-logs.txt').read_text(encoding='utf-8') for term in ['Error','InvalidOperationException']) and 'Critical' in (EV/'c-crash-logs.txt').read_text(encoding='utf-8'))
result={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,
    'scope':'Saved real observations, not a current monitor. UI export/visual observation unavailable and not claimed.'}
(EV/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result['passed'],'passed;',result['failed'],'failed')
for r in checks:
    if not r['passed']:print('FAILED',r['name'])
raise SystemExit(1 if result['failed'] else 0)
