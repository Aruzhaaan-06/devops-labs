"""Run material 11's four failure scenarios on the named local coursework stack.

Requires an already-built local image, a clean compose.yaml and PostgreSQL data.
Records T1 commands, live T2 events and T3 resource samples separately. Temporarily
changes only api.restart; restores the exact Compose bytes in finally. Never calls
down, removes volumes, or targets containers from other projects.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
import argparse,json,os,subprocess,threading,time,uuid,hashlib

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--image',default='devops-labs-demo-api')
    parser.add_argument('--tag',required=True)
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[1]
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    compose=repo/'compose.yaml';original=compose.read_bytes()
    api_name='devops-labs-api-1';db_name='devops-labs-db-1'
    env=dict(os.environ,API_IMAGE=args.image,API_TAG=args.tag)
    base='http://localhost:8088'
    stop_stats=threading.Event();stats_thread=None;events_process=None
    event_file=None;event_error=None
    transcript=(out/'t1-commands.txt').open('w',encoding='utf-8',buffering=1)
    def utc():return datetime.now(timezone.utc).isoformat()
    def write(name,value):(out/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def run(*argv,record=True):
        result=subprocess.run(list(argv),cwd=repo,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        if record:
            transcript.write('\n'+utc()+' $ '+subprocess.list2cmdline(argv)+'\n'+result.stdout+result.stderr+'\nexit='+str(result.returncode)+'\n')
        if result.returncode:raise RuntimeError('Command failed: '+subprocess.list2cmdline(argv)+'\n'+result.stderr)
        return result.stdout
    def http(method,path,data=None):
        started=utc()
        req=Request(base+path,method=method,headers={'Content-Type':'application/json'},
            data=json.dumps(data,ensure_ascii=False).encode() if data is not None else (b'' if method=='POST' else None))
        try:r=urlopen(req,timeout=10)
        except HTTPError as e:r=e
        raw=r.read().decode('utf-8')
        try:body=json.loads(raw)
        except json.JSONDecodeError:body=raw
        result={'utc':started,'method':method,'path':path,'status':r.status,'contentType':r.headers.get('Content-Type'),'body':body}
        transcript.write(utc()+' HTTP '+method+' '+path+'\n'+json.dumps(result,ensure_ascii=False)+'\n')
        return result
    def inspect():
        fields={'id':'{{json .Id}}','state':'{{json .State}}','restartCount':'{{json .RestartCount}}',
            'image':'{{json .Config.Image}}','imageId':'{{json .Image}}','restartPolicy':'{{json .HostConfig.RestartPolicy}}',
            'logConfig':'{{json .HostConfig.LogConfig}}','memoryLimit':'{{json .HostConfig.Memory}}',
            'memorySwapLimit':'{{json .HostConfig.MemorySwap}}','nanoCpus':'{{json .HostConfig.NanoCpus}}',
            'entrypoint':'{{json .Config.Entrypoint}}'}
        return {'utc':utc(),**{k:json.loads(run('docker','inspect','--format',fmt,api_name,record=False)) for k,fmt in fields.items()}}
    def wait_for(predicate,seconds=75):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            value=inspect()
            if predicate(value):return value
            time.sleep(.4)
        raise TimeoutError('Container did not reach required state')
    def healthy():return wait_for(lambda s:s['state']['Running'] and s['state'].get('Health',{}).get('Status')=='healthy')
    def preserve_marker(marker):
        project=http('GET','/api/projects/'+str(marker['project']['id']))
        task=http('GET','/api/tasks/'+str(marker['task']['id']))
        assert project['body']==marker['project'] and task['body']==marker['task']
        return {'project':project,'task':task}
    def logs(name,since):
        result=subprocess.run(['docker','logs','--since',since,api_name],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
        assert result.returncode==0
        text=result.stdout+result.stderr
        (out/(name+'-logs.txt')).write_text(text,encoding='utf-8')
        return [json.loads(line) for line in text.splitlines() if line.strip().startswith('{')]
    def sample_stats():
        with (out/'t3-stats.jsonl').open('w',encoding='utf-8',buffering=1) as stream:
            while not stop_stats.is_set():
                result=subprocess.run(['docker','stats','--no-stream','--format','{{json .}}',api_name,db_name],
                    cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
                rows=[json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
                stream.write(json.dumps({'utc':utc(),'exitCode':result.returncode,'containers':rows,'stderr':result.stderr.strip()},ensure_ascii=False)+'\n')
                stop_stats.wait(1)
    def start_phase(name):
        result={'name':name,'startUtc':utc(),'startNs':time.time_ns(),'before':inspect()}
        print('Starting',name,flush=True)
        return result
    def finish_phase(value):
        value['endNs']=time.time_ns();value['endUtc']=utc()
        write(value['name'],value)
        return value
    try:
        assert run('git','diff','--','compose.yaml').strip()==''
        assert original.decode('utf-8').count('    restart: unless-stopped')==3
        actual_project=run('docker','inspect','--format','{{index .Config.Labels "com.docker.compose.project"}}',api_name).strip()
        assert actual_project=='devops-labs'
        before=healthy()
        assert before['image']==args.image+':'+args.tag and before['restartPolicy']['Name']=='unless-stopped'
        run('docker','compose','ps')
        run('docker','compose','logs','api','--tail','20')
        run('docker','inspect',api_name,'--format','{{json .HostConfig.LogConfig}}')
        run('docker','inspect',api_name,'--format','{{.HostConfig.RestartPolicy.Name}}')
        write('initial-inspection',before)
        marker_project=http('POST','/api/projects',{'name':'lab11-retained-'+uuid.uuid4().hex})
        assert marker_project['status']==201
        marker_task=http('POST','/api/tasks',{'projectId':marker_project['body']['id'],'title':'Lab11: persists across process failures'})
        assert marker_task['status']==201
        marker={'project':marker_project['body'],'task':marker_task['body']};write('marker',marker)
        event_file=(out/'t2-events.jsonl').open('w',encoding='utf-8')
        event_error=(out/'t2-stderr.txt').open('w',encoding='utf-8')
        event_args=['docker','events','--since',str(int(time.time())),'--format','{{json .}}','--filter','container='+api_name]
        for action in ['start','kill','die','oom','stop','health_status']:event_args+=['--filter','event='+action]
        write('observation-streams',{'T1':'verify-lab11.py command and HTTP transcript','T2':event_args,
            'T3':['docker','stats','--no-stream','--format','{{json .}}',api_name,db_name],
            'T3Mode':'repeated samples in parallel; resolves current container names across Compose recreation'})
        events_process=subprocess.Popen(event_args,cwd=repo,stdout=event_file,stderr=event_error)
        stats_thread=threading.Thread(target=sample_stats,daemon=True);stats_thread.start()
        time.sleep(1)
        assert events_process.poll() is None
        error=start_phase('scenario-2-request-error')
        error['http']=http('GET','/api/chaos/error')
        assert error['http']['status']==500 and 'Exception' not in json.dumps(error['http']['body']) and 'Chaos:' not in json.dumps(error['http']['body'])
        time.sleep(2)
        error['after']=healthy();error['live']=http('GET','/health/live')
        error['logs']=logs(error['name'],error['startUtc'])
        assert any(row.get('LogLevel')=='Error' and 'InvalidOperationException' in row.get('Exception','') for row in error['logs'])
        assert all(error['before'][k]==error['after'][k] for k in ['id','restartCount'])
        assert error['before']['state']['StartedAt']==error['after']['state']['StartedAt']
        finish_phase(error)
        # Ensure Docker's successful-start monitoring interval has elapsed before crash.
        started=datetime.fromisoformat(before['state']['StartedAt'].replace('Z','+00:00'))
        remaining=11-(datetime.now(timezone.utc)-started).total_seconds()
        if remaining>0:time.sleep(remaining)
        crash=start_phase('scenario-3-auto-restart')
        crash['http']=http('POST','/api/chaos/crash');assert crash['http']['status']==202
        crash['after']=wait_for(lambda s:s['restartCount']==crash['before']['restartCount']+1 and s['state'].get('Health',{}).get('Status')=='healthy')
        crash['ready']=http('GET','/health/ready');crash['marker']=preserve_marker(marker)
        crash['logs']=logs(crash['name'],crash['startUtc'])
        assert any(row.get('LogLevel')=='Critical' for row in crash['logs'])
        finish_phase(crash)
        changed=original.decode('utf-8').replace('    restart: unless-stopped','    restart: "no"',1).encode('utf-8')
        compose.write_bytes(changed)
        run('docker','compose','up','-d','--no-build','--wait','--wait-timeout','90')
        no_before=healthy();assert no_before['restartPolicy']['Name']=='no'
        time.sleep(11)
        no_restart=start_phase('scenario-4-no-restart')
        no_restart['http']=http('POST','/api/chaos/crash');assert no_restart['http']['status']==202
        exited=wait_for(lambda s:s['state']['Status']=='exited')
        time.sleep(5)
        no_restart['after']=inspect();no_restart['psAll']=run('docker','compose','ps','-a')
        no_restart['logs']=logs(no_restart['name'],no_restart['startUtc'])
        assert no_restart['after']['state']['Status']=='exited' and no_restart['after']['state']['ExitCode']==1
        assert no_restart['after']['restartCount']==0
        finish_phase(no_restart)
        compose.write_bytes(original)
        run('docker','compose','up','-d','--no-build','--wait','--wait-timeout','90')
        restored=healthy();assert restored['restartPolicy']['Name']=='unless-stopped'
        write('restored-after-no',{'inspection':restored,'marker':preserve_marker(marker)})
        stop=start_phase('scenario-5-graceful-stop')
        run('docker','compose','stop','api')
        time.sleep(5)
        stop['after']=inspect();stop['logs']=logs(stop['name'],stop['startUtc'])
        assert stop['after']['state']['Status']=='exited' and stop['after']['state']['ExitCode']==0
        assert stop['after']['restartCount']==stop['before']['restartCount']
        assert any('Application is shutting down' in row.get('Message','') for row in stop['logs'])
        finish_phase(stop)
        run('docker','compose','start','api');final=healthy()
        write('final-local',{'inspection':final,'info':http('GET','/'),'live':http('GET','/health/live'),
            'ready':http('GET','/health/ready'),'marker':preserve_marker(marker),
            'databaseVolumes':json.loads(run('docker','inspect','--format','{{json .Mounts}}',db_name,record=False))})
        print('All four failure scenarios passed; final API healthy, data preserved.',flush=True)
    finally:
        compose.write_bytes(original)
        # On failure, restore availability as well as the exact tracked configuration.
        try:run('docker','compose','up','-d','--no-build','--wait','--wait-timeout','90')
        finally:
            stop_stats.set()
            if stats_thread:stats_thread.join(timeout=25)
            if events_process:
                events_process.terminate();events_process.wait(timeout=10)
            if event_file:event_file.close()
            if event_error:event_error.close()
            transcript.close()
            write('compose-restored',{'originalSha256':hashlib.sha256(original).hexdigest(),
                'finalSha256':hashlib.sha256(compose.read_bytes()).hexdigest(),'exactBytesRestored':compose.read_bytes()==original})
    events=[json.loads(line) for line in (out/'t2-events.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    for phase in [error,crash,no_restart,stop]:
        phase['events']=[e for e in events if phase['startNs']<=e['timeNano']<=phase['endNs']]
        write(phase['name'],phase)
    assert not any(e['Action'] in ['die','start','kill','oom','stop'] for e in error['events'])
    assert any(e['Action']=='die' and e['Actor']['Attributes']['exitCode']=='1' for e in crash['events'])
    assert any(e['Action']=='start' for e in crash['events'])
    assert any(e['Action']=='die' and e['Actor']['Attributes']['exitCode']=='1' for e in no_restart['events'])
    assert not any(e['Action']=='start' for e in no_restart['events'])
    assert any(e['Action']=='kill' and e['Actor']['Attributes']['signal']=='15' for e in stop['events'])
    assert any(e['Action']=='die' and e['Actor']['Attributes']['exitCode']=='0' for e in stop['events'])
    assert any(e['Action']=='stop' for e in stop['events'])
    assert not any(e['Action']=='start' for e in stop['events'])
    print('T2 event chains confirmed; T1/T2/T3 retained at',out,flush=True)

if __name__=='__main__':main()
