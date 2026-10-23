"""Validate retained material 11 command evidence; does not run failure requests."""
from pathlib import Path
import json

EV=Path(__file__).resolve().parents[1]/'evidence/lab06-failures'
load=lambda name:json.loads((EV/(name+'.json')).read_text(encoding='utf-8'))
checks=[]
def check(name,value):checks.append({'name':name,'passed':bool(value)})
def events(scenario):return [(e['Action'],e['Actor']['Attributes'].get('exitCode'),e['Actor']['Attributes'].get('signal')) for e in scenario['events']]
initial=load('initial-inspection');error=load('scenario-2-request-error');crash=load('scenario-3-auto-restart')
no=load('scenario-4-no-restart');stop=load('scenario-5-graceful-stop');final=load('final-local');marker=load('marker')
check('Local main image used',initial['image']=='devops-labs-demo-api:lab11-89a0e2b')
check('Initial API healthy',initial['state']['Health']['Status']=='healthy')
check('Initial restart policy unless-stopped',initial['restartPolicy']['Name']=='unless-stopped')
check('JSON log rotation configured',initial['logConfig']=={'Type':'json-file','Config':{'max-file':'3','max-size':'10m'}})
check('Memory and CPU limits configured',initial['memoryLimit']==268435456 and initial['memorySwapLimit']==268435456 and initial['nanoCpus']==1000000000)
check('Exec-form entrypoint',initial['entrypoint']==['dotnet','DemoApi.dll'])
check('Request error returns HTTP500 ProblemDetails',error['http']['status']==500 and error['http']['body']['status']==500 and 'application/problem+json' in error['http']['contentType'])
check('Error response does not expose internal exception','Chaos:' not in json.dumps(error['http']['body']) and 'InvalidOperationException' not in json.dumps(error['http']['body']))
check('Error log includes exception and stack',any(r.get('LogLevel')=='Error' and 'ChaosController.Error' in r.get('Exception','') for r in error['logs']))
check('Request error did not restart container',error['before']['id']==error['after']['id'] and error['before']['restartCount']==error['after']['restartCount'] and error['before']['state']['StartedAt']==error['after']['state']['StartedAt'])
check('No lifecycle events from request error',not any(a in ['die','start','kill','oom','stop'] for a,_,_ in events(error)))
check('API live after request error',error['live']['status']==200)
check('Crash accepted asynchronously',crash['http']['status']==202)
check('Auto-restart crash exits1',('die','1',None) in events(crash))
check('Crash event chain includes start and healthy',any(a=='start' for a,_,_ in events(crash)) and any(a=='health_status: healthy' for a,_,_ in events(crash)))
check('Same container automatic restart count increments once',crash['before']['id']==crash['after']['id'] and crash['after']['restartCount']==crash['before']['restartCount']+1)
check('Crash logs Critical',any(r.get('LogLevel')=='Critical' for r in crash['logs']))
check('Readiness recovered',crash['ready']['status']==200)
check('Temporary restart policy no applied',no['before']['restartPolicy']['Name']=='no')
check('No policy leaves API Exited1',no['after']['state']['Status']=='exited' and no['after']['state']['ExitCode']==1)
check('No automatic restart under no',no['after']['restartCount']==0 and not any(a=='start' for a,_,_ in events(no)))
check('No policy has actual die1 event',('die','1',None) in events(no))
check('Policy restored before graceful stop',stop['before']['restartPolicy']['Name']=='unless-stopped')
check('Graceful stop receives SIGTERM',('kill',None,'15') in events(stop))
check('Graceful stop exits0 with stop event',('die','0',None) in events(stop) and any(a=='stop' for a,_,_ in events(stop)))
check('Graceful stop no SIGKILL',not any(a=='kill' and signal=='9' for a,_,signal in events(stop)))
check('Manually stopped container stays stopped',stop['after']['state']['Status']=='exited' and stop['after']['state']['ExitCode']==0 and not any(a=='start' for a,_,_ in events(stop)))
check('Graceful shutdown log recorded',any('Application is shutting down' in r.get('Message','') for r in stop['logs']))
check('Explicit start restored API',final['inspection']['state']['Health']['Status']=='healthy' and final['live']['status']==200 and final['ready']['status']==200)
check('Marker persisted across crashes and recreation',all(s['marker']['project']['body']==marker['project'] and s['marker']['task']['body']==marker['task'] for s in [crash,load('restored-after-no'),final]))
check('Named DB volume retained',any(m['Type']=='volume' and m['Name']=='devops-labs_pgdata' for m in final['databaseVolumes']))
check('Compose original bytes restored',load('compose-restored')['exactBytesRestored'] and load('compose-restored')['originalSha256']==load('compose-restored')['finalSha256'])
check('T2 observer no stderr',(EV/'t2-stderr.txt').read_text().strip()=='')
check('T3 actual resource samples retained',load('resource-summary')['apiSamples']>5)
postman=load('postman-results')
check('Live Postman4requests10assertions',postman['requests']==4 and postman['assertions']==10 and postman['failed']==0 and postman['exitCode']==0)
result={'passed':sum(r['passed'] for r in checks),'failed':sum(not r['passed'] for r in checks),'checks':checks,
    'scope':'Actual command/HTTP/events/logs/resource consistency for material11. Docker Desktop tab inspection tracked separately.'}
(EV/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(result['passed'])+' passed; '+str(result['failed'])+' failed')
for row in checks:
    if not row['passed']:print('FAILED:',row['name'])
raise SystemExit(1 if result['failed'] else 0)
