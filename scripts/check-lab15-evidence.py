"""Check recorded material15 observations; never redeploy or repeat the incident."""
from pathlib import Path
from datetime import datetime
import hashlib,json,math,re

ROOT=Path(__file__).resolve().parents[1];EV=ROOT/'evidence/lab08-incident'
load=lambda n:json.loads((EV/(n+'.json')).read_text(encoding='utf-8'))
stamp=lambda s:datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
checks=[]
def check(name,result):checks.append({'name':name,'passed':bool(result)})

m=load('incident-metrics');d=load('diagnosis');first=load('first-firing');source=load('source-proof');guard=load('latency-guard');retained=load('retained-data')
check('T0 T1 T2 ordered',stamp(m['T0'])<stamp(m['T1'])<stamp(m['T2']))
check('Detection arithmetic',abs(stamp(m['T1'])-stamp(m['T0'])-m['detectionSeconds'])<.002)
check('Recovery arithmetic',abs(stamp(m['T2'])-stamp(m['T1'])-m['recoverySeconds'])<.002)
slow=next(r for g in first['groups'] for r in g['rules'] if r['name']=='ApiSlowRequests')
check('Actual slow firing at T1',slow['state']=='firing' and first['observedUtc']==m['T1'])
check('Configured30s for satisfied',slow['duration']==30 and stamp(slow['lastEvaluation'])-stamp(slow['alerts'][0]['activeAt'])>=30)
timeline=[json.loads(s) for s in (EV/'alerts-timeline.jsonl').read_text(encoding='utf-8').splitlines()]
check('Observer retained first firing',any(o['observedUtc']==first['observedUtc'] for o in timeline))
check('Initial slow state inactive',next(r['state'] for g in timeline[0]['groups'] for r in g['rules'] if r['name']=='ApiSlowRequests')=='inactive')
check('No observer errors and owned load stopped',load('observer-final')['errors']==[] and load('observer-final')['loadStopped'])
check('Manual version probe after alarm',stamp(d['version']['utc'])>=stamp(m['T1']))
check('Manual latency probe after alarm',stamp(d['postAlertProbe']['utc'])>=stamp(m['T1']) and d['probeWasAfterAlert'])
check('PromQL culprit Tasks List',d['culprit']['metric']['controller']=='Tasks' and d['culprit']['metric']['action']=='List' and float(d['culprit']['value'][1])>1)
check('Bad exact version identified',d['version']['body']['version']=='sha-'+source['badMain'][:7])
check('Exact slow source line identified','Task.Delay(1500, ct)' in d['sourceLine'] and d['line']==15)
check('Functional200 yet slow',d['postAlertProbe']['status']==200 and d['postAlertProbe']['seconds']>=1.4)
check('Four PostgreSQL CI runs40passed',len(load('ci-summary'))==4 and all(r['conclusion']=='success' and r['postgresPassed']==40 and r['postgresFailed']==0 for r in load('ci-summary')))
check('Rollback workflow success',load('github-links')['rollbackRun']['conclusion']=='success')
check('Rollback selected previous SHA',load('rollback-dispatch')['tag']=='sha-'+source['baseline'][:7])
check('T2 confirms old version and inactive',load('T2')['version']['version']=='sha-'+source['baseline'][:7] and load('T2')['rule']['state']=='inactive')
revert=load('revert-operation')['data']['revertPullRequest']
check('Genuine GitHub generated Revert PR',revert['pullRequest']['number']==26 and revert['revertPullRequest']['number']==28)
check('Bad and revert PRs merged',load('github-links')['badPR']['merged'] and load('github-links')['revertPR']['merged'])
check('Bad delay present fixed delay absent','await Task.Delay(1500, ct)' in source['badSource'] and 'await Task.Delay(1500, ct)' not in source['fixedSource'])
check('Application restored exactly',source['sourceRestoredExactly'] and load('revert-recovered')['applicationSourceRestoredExactly'])
check('Fixed observed p95 finite below1',math.isfinite(load('revert-recovered')['tasksListP95Seconds']) and 0<=load('revert-recovered')['tasksListP95Seconds']<1)
check('Old permanent configs unchanged',all(source['permanentConfigUnchanged'].values()))
check('Bad latency gate fails honestly',guard['badExitCode']==1 and guard['badMilliseconds']>=1000 and 'exceeds 1000' in (EV/'bad-latency-guard.txt').read_text(encoding='utf-8'))
check('Fixed latency gate3samples pass',guard['goodExitCode']==0 and len(guard['good']['samples'])==3 and all(s['status']==200 and s['milliseconds']<1000 for s in guard['good']['samples']))
raw=(ROOT/'scripts/smoke-tasks-latency.ps1').read_bytes().replace(b'\r\n',b'\n')
check('Gate code matches tested code',hashlib.sha256(raw).hexdigest()==guard['scriptSha256'])
check('Postman6requests13assertions nofailures',all(load('postman-results')[k]==v for k,v in {'requests':6,'assertions':13,'failed':0,'exitCode':0,'readOnly':True,'allFiveRulesInactive':True}.items()))
check('Historical data retained',all(m['preserved'] for m in retained['markers']) and retained['lab13InProgressTasks']==1200 and retained['lab14BusinessTasksRetained'])
tasks=load('load-tasks');digest=hashlib.sha256(json.dumps(tasks,sort_keys=True,separators=(',',':')).encode()).hexdigest()
check('Load task set retained',len(tasks)==retained['incidentLoad']['storedTasks']==1771 and digest==retained['incidentLoad']['taskSetSha256'])
check('Five transport errors preserved',len(re.findall(r'^error:',(EV/'load-console.txt').read_text(encoding='utf-8'),re.M))==retained['incidentLoad']['consoleErrors']==5)
check('One issue per action',len(load('github-links')['actions'])==3 and len({i['number'] for i in load('github-links')['actions'].values()})==3)
check('Postmortem actual comment retained','issuecomment-' in load('postmortem')['url'] and len(load('postmortem')['body'])>1000)
check('UI limits explicitly declared',load('ui-status')['alertScreenshotTaken'] is False and load('ui-status')['grafanaScreenshotTaken'] is False)
result={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,
    'scope':'Recorded actual evidence, not a current monitor or teacher grading. UI screenshot and defense limitations are not counted as completed rubric points.'}
(EV/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result['passed'],'passed;',result['failed'],'failed')
if result['failed']:raise SystemExit(1)
