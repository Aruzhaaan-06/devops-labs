"""Run lab 6 part 2 on the fixed local coursework stack; retain original evidence.

Deliberately OOMs only the 256 MiB API, stops only its DB, and temporarily replaces
only api.healthcheck. Restores exact Compose bytes and both services in finally.
Do not run alongside another deployment of this Compose project.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import argparse,hashlib,json,os,subprocess,threading,time,uuid

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--tag',required=True)
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[1];out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    compose=repo/'compose.yaml';original=compose.read_bytes()
    env=dict(os.environ,API_IMAGE='devops-labs-demo-api',API_TAG=args.tag)
    api='devops-labs-api-1';db='devops-labs-db-1';base='http://localhost:8088'
    stop_stats=threading.Event();observer=None;worker=None;stream=None;errors=None;validated=False
    transcript=(out/'t1-commands.txt').open('w',encoding='utf-8',buffering=1)
    def utc():return datetime.now(timezone.utc).isoformat()
    def save(name,value):(out/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def run(*argv,record=True,timeout=150):
        p=subprocess.run(argv,cwd=repo,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
        if record:transcript.write(utc()+' $ '+subprocess.list2cmdline(argv)+'\n'+p.stdout+p.stderr+'\nexit='+str(p.returncode)+'\n')
        if p.returncode:raise RuntimeError(subprocess.list2cmdline(argv)+' failed\n'+p.stderr)
        return p.stdout
    def http(method,path,data=None):
        start=time.perf_counter();value={'utc':utc(),'method':method,'path':path}
        req=Request(base+path,method=method,headers={'Content-Type':'application/json'},
            data=json.dumps(data).encode() if data is not None else (b'' if method=='POST' else None))
        try:
            try:r=urlopen(req,timeout=25)
            except HTTPError as error:r=error
            raw=r.read().decode('utf-8')
            try:body=json.loads(raw)
            except json.JSONDecodeError:body=raw
            value.update(status=r.status,body=body)
        except (OSError,TimeoutError) as error:
            value.update(status=None,transportError=type(error).__name__+': '+str(error))
        value['seconds']=round(time.perf_counter()-start,6)
        transcript.write(json.dumps(value,ensure_ascii=False)+'\n');return value
    def inspect():
        fmt='{"id":{{json .Id}},"state":{{json .State}},"restartCount":{{json .RestartCount}},"image":{{json .Config.Image}},"imageId":{{json .Image}},"memoryLimit":{{json .HostConfig.Memory}},"memorySwapLimit":{{json .HostConfig.MemorySwap}},"restartPolicy":{{json .HostConfig.RestartPolicy.Name}},"healthcheck":{{json .Config.Healthcheck}}}'
        return {'utc':utc(),**json.loads(run('docker','inspect','--format',fmt,api,record=False))}
    def wait_for(predicate,timeout=100):
        end=time.monotonic()+timeout
        while time.monotonic()<end:
            value=inspect()
            if predicate(value):return value
            time.sleep(.5)
        raise TimeoutError('Expected container state not reached')
    def healthy():return wait_for(lambda s:s['state']['Running'] and s['state'].get('Health',{}).get('Status')=='healthy')
    def marker_check(marker):
        result={'project':http('GET','/api/projects/'+str(marker['project']['id'])),
            'task':http('GET','/api/tasks/'+str(marker['task']['id']))}
        assert result['project']['body']==marker['project'] and result['task']['body']==marker['task']
        return result
    def phase(name):
        print('Starting',name,flush=True)
        return {'name':name,'startUtc':utc(),'startNs':time.time_ns(),'before':inspect()}
    def finish(value):
        value['after']=inspect();value['endUtc']=utc();value['endNs']=time.time_ns()
        p=subprocess.run(['docker','logs','--since',value['startUtc'],api],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
        assert p.returncode==0
        raw=p.stdout+p.stderr;(out/(value['name']+'-logs.txt')).write_text(raw,encoding='utf-8')
        value['logs']=[json.loads(line) for line in raw.splitlines() if line.startswith('{')]
        save(value['name'],value)
    def stats():
        with (out/'t3-stats.jsonl').open('w',encoding='utf-8',buffering=1) as f:
            while not stop_stats.is_set():
                p=subprocess.run(['docker','stats','--no-stream','--format','{{json .}}',api,db],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20)
                f.write(json.dumps({'utc':utc(),'exitCode':p.returncode,'stderr':p.stderr.strip(),
                    'containers':[json.loads(line) for line in p.stdout.splitlines() if line.startswith('{')]},ensure_ascii=False)+'\n')
                stop_stats.wait(.5)
    def cgroup():
        values={}
        for name in ['memory.peak','memory.events','memory.max','memory.swap.max']:
            p=subprocess.run(['docker','exec',api,'cat','/sys/fs/cgroup/'+name],cwd=repo,capture_output=True,text=True,timeout=10)
            values[name]={'exitCode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
        return values
    try:
        assert run('git','diff','HEAD','--','compose.yaml').strip()==''
        assert run('docker','inspect','--format','{{index .Config.Labels "com.docker.compose.project"}}',api).strip()=='devops-labs'
        first=healthy();assert first['image']=='devops-labs-demo-api:'+args.tag
        assert first['memoryLimit']==268435456 and first['memorySwapLimit']==268435456 and first['restartPolicy']=='unless-stopped'
        validated=True
        save('initial',first)
        p=http('POST','/api/projects',{'name':'lab12-retained-'+uuid.uuid4().hex});assert p['status']==201
        t=http('POST','/api/tasks',{'projectId':p['body']['id'],'title':'Lab12 retained through OOM and DB outage'});assert t['status']==201
        marker={'project':p['body'],'task':t['body']};save('marker',marker)
        stream=(out/'t2-events.jsonl').open('w',encoding='utf-8');errors=(out/'t2-stderr.txt').open('w',encoding='utf-8')
        argv=['docker','events','--since',str(int(time.time())),'--format','{{json .}}','--filter','container='+api]
        for event in ['start','kill','die','oom','stop','health_status']:argv+=['--filter','event='+event]
        observer=subprocess.Popen(argv,cwd=repo,stdout=stream,stderr=errors)
        worker=threading.Thread(target=stats,daemon=True);worker.start();time.sleep(1)
        assert observer.poll() is None
        oom=phase('scenario-6-oom');oom['cgroupBefore']=cgroup();oom['requests']=[]
        for _ in range(4):
            response=http('POST','/api/chaos/leak?mb=80');oom['requests'].append(response)
            time.sleep(1)
            current=inspect()
            if response['status'] is None or current['restartCount']>oom['before']['restartCount']:break
        oom['recovered']=wait_for(lambda s:s['restartCount']==oom['before']['restartCount']+1 and s['state'].get('Health',{}).get('Status')=='healthy')
        oom['cgroupAfter']=cgroup();oom['marker']=marker_check(marker)
        finish(oom)
        # Capture recent OOM before a later recreation or bounded event buffer loses it.
        diag=subprocess.run(['pwsh','-NoProfile','-File','scripts/diag.ps1',api],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=45)
        (out/'diag-after-oom.txt').write_text(diag.stdout+'\n'+diag.stderr,encoding='utf-8')
        assert diag.returncode==0,diag.stderr
        dependency=phase('scenario-7-db-unavailable')
        run('docker','compose','stop','db')
        dependency['live']=http('GET','/health/live');dependency['ready']=http('GET','/health/ready');dependency['tasks']=http('GET','/api/tasks')
        dependency['ps']=run('docker','compose','ps','-a')
        assert dependency['live']['status']==200 and dependency['ready']['status']==503 and dependency['tasks']['status']==500
        finish(dependency)
        assert dependency['after']['state']['Health']['Status']=='healthy'
        assert dependency['after']['restartCount']==dependency['before']['restartCount'] and dependency['after']['state']['StartedAt']==dependency['before']['state']['StartedAt']
        run('docker','compose','start','db')
        end=time.monotonic()+60
        while http('GET','/health/ready')['status']!=200:
            assert time.monotonic()<end;time.sleep(1)
        save('db-restored',{'inspection':inspect(),'marker':marker_check(marker)})
        text=original.decode('utf-8');anchor='    restart: unless-stopped'
        assert text.count(anchor)==3
        changed=text.replace(anchor,'    healthcheck:\n      test: ["CMD", "curl", "-fsS", "http://localhost:8080/no-such-endpoint"]\n      interval: 5s\n      retries: 2\n'+anchor,1)
        compose.write_bytes(changed.encode('utf-8'))
        run('docker','compose','up','-d','--no-build')
        unhealthy=phase('scenario-8-unhealthy')
        time.sleep(40)
        unhealthy['healthObserved']=inspect();unhealthy['live']=http('GET','/health/live');unhealthy['ready']=http('GET','/health/ready')
        unhealthy['ps']=run('docker','compose','ps')
        assert unhealthy['healthObserved']['state']['Health']['Status']=='unhealthy' and unhealthy['live']['status']==200
        finish(unhealthy)
        assert unhealthy['before']['id']==unhealthy['after']['id'] and unhealthy['before']['restartCount']==unhealthy['after']['restartCount']==0
        assert unhealthy['before']['state']['StartedAt']==unhealthy['after']['state']['StartedAt']
        compose.write_bytes(original)
        run('docker','compose','up','-d','--no-build','--wait','--wait-timeout','90');healthy()
        slow=phase('scenario-9-slow-response')
        slow['normal']=http('GET','/api/tasks');slow['delayed']=http('GET','/api/chaos/slow?ms=3000')
        slow['ready']=http('GET','/health/ready')
        assert slow['normal']['status']==slow['delayed']['status']==slow['ready']['status']==200
        assert slow['delayed']['body']=={'delayedMs':3000} and slow['delayed']['seconds']>=2.9
        finish(slow)
        assert slow['before']['id']==slow['after']['id'] and slow['before']['restartCount']==slow['after']['restartCount']
        save('final-local',{'inspection':healthy(),'info':http('GET','/'),'ready':http('GET','/health/ready'),
            'live':http('GET','/health/live'),'marker':marker_check(marker),
            'dbVolumes':json.loads(run('docker','inspect','--format','{{json .Mounts}}',db,record=False))})
    finally:
        try:
            if validated:
                compose.write_bytes(original)
                run('docker','compose','up','-d','--no-build','--wait','--wait-timeout','90')
        finally:
            stop_stats.set()
            if worker:worker.join(timeout=25)
            if observer:observer.terminate();observer.wait(timeout=10)
            if stream:stream.close()
            if errors:errors.close()
            transcript.close()
            save('compose-restored',{'exactBytesRestored':compose.read_bytes()==original,
                'originalSha256':hashlib.sha256(original).hexdigest(),'finalSha256':hashlib.sha256(compose.read_bytes()).hexdigest()})
    events=[json.loads(line) for line in (out/'t2-events.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    for value in [oom,dependency,unhealthy,slow]:
        value['events']=[e for e in events if value['startNs']<=e['timeNano']<=value['endNs']];save(value['name'],value)
    assert any(e['Action']=='oom' for e in oom['events'])
    assert any(e['Action']=='die' and e['Actor']['Attributes'].get('exitCode')=='137' for e in oom['events'])
    assert any(e['Action']=='start' for e in oom['events'])
    for value in [dependency,unhealthy,slow]:assert not any(e['Action'] in ['die','start','oom','kill','stop'] for e in value['events'])
    print('OOM137+restart, DB503/500 without restart, unhealthy without restart and slow200 confirmed; restored healthy, data preserved.',flush=True)

if __name__=='__main__':main()
