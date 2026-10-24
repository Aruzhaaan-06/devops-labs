"""Run authorized lab7 part2 failures ONLY on the fixed local coursework API.

Requires --tag matching its local lab14 image. Generates 500/slow requests,
crashes process, deliberately causes OOM in 256MiB, and stops/starts only API.
Never alters Compose, DB, monitoring, or existing data. Polls real alert rules;
waits for crash alert to clear before the OOM scenario. Do not run with deploy.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import argparse,json,subprocess,threading,time

API='http://localhost:8088';PROM='http://localhost:9090';NAME='devops-labs-api-1'
def utc():return datetime.now(timezone.utc).isoformat()
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--tag',required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();repo=Path(__file__).resolve().parents[1];out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    if not args.tag.startswith('lab14-'):raise ValueError('Only explicit local lab14 tag allowed')
    def save(n,v):(out/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def run(*cmd):
        p=subprocess.run(cmd,cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=35)
        if p.returncode:raise RuntimeError('Command failed: '+subprocess.list2cmdline(cmd)+'\n'+p.stderr)
        return p.stdout
    def inspect():
        fmt='{"id":{{json .Id}},"image":{{json .Config.Image}},"startedAt":{{json .State.StartedAt}},"running":{{json .State.Running}},"health":{{json .State.Health.Status}},"restartCount":{{json .RestartCount}},"memory":{{json .HostConfig.Memory}},"swap":{{json .HostConfig.MemorySwap}},"restartPolicy":{{json .HostConfig.RestartPolicy.Name}}}'
        return json.loads(run('docker','inspect','--format',fmt,NAME))
    initial=inspect();assert initial['image']=='devops-labs-demo-api:'+args.tag
    assert initial['running'] and initial['health']=='healthy' and initial['memory']==initial['swap']==268435456 and initial['restartPolicy']=='unless-stopped'
    def http(url,method='GET',body=None):
        v={'utc':utc(),'method':method,'url':url};t=time.perf_counter()
        req=Request(url,method=method,data=json.dumps(body).encode() if body is not None else (b'' if method=='POST' else None),headers={'Content-Type':'application/json'})
        try:
            try:r=urlopen(req,timeout=12)
            except HTTPError as e:r=e
            raw=r.read().decode('utf-8')
            try:b=json.loads(raw)
            except json.JSONDecodeError:b=raw
            v.update(status=r.status,body=b)
        except OSError as e:v.update(status=None,error=type(e).__name__+': '+str(e))
        v['seconds']=round(time.perf_counter()-t,6);return v
    def query(expr):
        r=http(PROM+'/api/v1/query?'+urlencode({'query':expr}));assert r['status']==200
        return r['body']['data']['result']
    def raw_counter():
        raw=http(API+'/metrics')['body'];return next(float(s.split()[1]) for s in raw.splitlines() if s.startswith('demo_tasks_created_total '))
    # Initialize then measure the service counter and matching HTTP counter.
    project=http(API+'/api/projects','POST',{'name':'lab14-counter-'+str(int(time.time()))});assert project['status']==201
    def create(title):return http(API+'/api/tasks','POST',{'projectId':project['body']['id'],'title':title})
    init=create('initialize');assert init['status']==201
    before=raw_counter();created=create('counted');assert created['status']==201
    after=raw_counter();bad=create('');missing=http(API+'/api/tasks','POST',{'projectId':2147483647,'title':'missing'})
    assert after==before+1 and raw_counter()==after and bad['status']==400 and missing['status']==404
    save('business-counter',{'before':before,'afterSuccess':after,'afterRejected':raw_counter(),'project':project,'created':created,'bad':bad,'missing':missing})
    save('initial',{'utc':utc(),'inspection':initial,'info':http(API+'/')})
    stop=threading.Event();observations=[];lock=threading.Lock();observer_errors=[];phase='warmup';phases=[]
    def observer():
        with (out/'alerts-timeline.jsonl').open('w',encoding='utf-8',buffering=1) as f:
            while not stop.is_set():
                try:
                    r=http(PROM+'/api/v1/rules?type=alert');assert r['status']==200
                    row={'observedUtc':utc(),'epoch':time.time(),'phase':phase,'groups':r['body']['data']['groups']}
                    f.write(json.dumps(row,ensure_ascii=False)+'\n')
                    with lock:observations.append(row)
                except Exception as e:observer_errors.append({'utc':utc(),'error':str(e)})
                stop.wait(1)
    worker=threading.Thread(target=observer,daemon=True);worker.start()
    event_file=(out/'docker-events.jsonl').open('w',encoding='utf-8');event_err=(out/'docker-events-stderr.txt').open('w',encoding='utf-8')
    events=subprocess.Popen(['docker','events','--filter','container='+initial['id'],'--format','{{json .}}'],cwd=repo,stdout=event_file,stderr=event_err)
    load_file=(out/'load-console.txt').open('w',encoding='utf-8');load_err=(out/'load-stderr.txt').open('w',encoding='utf-8')
    load=subprocess.Popen(['pwsh','-NoProfile','-File','scripts/load.ps1','-Iterations','6000'],cwd=repo,stdout=load_file,stderr=load_err)
    def state(name):
        with lock:last=observations[-1] if observations else None
        if last:
            return next((r['state'] for g in last['groups'] for r in g['rules'] if r['name']==name),None)
    def wait(predicate,seconds=140):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if predicate():return
            time.sleep(.5)
        raise TimeoutError('Expected state not reached in '+str(seconds)+'s; phase='+phase)
    def live(name,status,extra=None):save('live-phase',{'phase':name,'status':status,'utc':utc(),**(extra or {})})
    def start(name,alerts):
        nonlocal phase
        phase=name;v={'name':name,'startUtc':utc(),'startEpoch':time.time(),'before':inspect(),'expectedAlerts':alerts,'requests':[]}
        phases.append(v);live(name,'running');print('Started',name,flush=True);return v
    def fired(v,name):
        wait(lambda:state(name)=='firing',160);v.setdefault('firingSnapshots',{})[name]=http(PROM+'/api/v1/rules?type=alert')
        live(v['name'],'firing',{'alert':name});print(v['name'],name,'firing',utc(),flush=True)
        v.setdefault('metricsAtFiring',{})[name]={'p95':query('histogram_quantile(0.95,sum by(le)(rate(http_request_duration_seconds_bucket{job="demo-api"}[1m])))'),
            'httpCodes':query('sum by(code)(rate(http_requests_received_total{job="demo-api"}[1m]))'),
            'memoryPercent':query('100 * container_memory_working_set_bytes{name="devops-labs-api-1"} / (container_spec_memory_limit_bytes{name="devops-labs-api-1"}>0)')}
        time.sleep(15)
    def finish(v):
        v['after']=inspect();v['endUtc']=utc();v['endEpoch']=time.time()
        p=subprocess.run(['docker','logs','--since',v['startUtc'],NAME],cwd=repo,capture_output=True,text=True,encoding='utf-8',errors='replace')
        assert p.returncode==0;(out/(v['name']+'-logs.txt')).write_text(p.stdout+p.stderr,encoding='utf-8');save(v['name'],v)
    try:
        wait(lambda:state('ApiDown')=='inactive');time.sleep(65)
        a=start('a-errors',['ApiHighErrorRate'])
        for _ in range(60):
            r=http(API+'/api/chaos/error');a['requests'].append(r);assert r['status']==500;time.sleep(1)
        fired(a,'ApiHighErrorRate');finish(a);wait(lambda:state('ApiHighErrorRate')=='inactive')
        b=start('b-slow',['ApiSlowRequests'])
        for _ in range(40):
            r=http(API+'/api/chaos/slow?ms=1500');b['requests'].append(r);assert r['status']==200 and r['seconds']>=1.4
        fired(b,'ApiSlowRequests');finish(b);wait(lambda:state('ApiSlowRequests')=='inactive')
        # A new local deployment can itself make the rolling restart rule fire.
        # The crash trial must begin from inactive to attribute its new firing.
        live('baseline-before-crash','waiting for ContainerRestarted inactive')
        wait(lambda:state('ContainerRestarted')=='inactive',360)
        c=start('c-crash',['ContainerRestarted']);c['requests'].append(http(API+'/api/chaos/crash','POST'))
        wait(lambda:inspect()['running'] and inspect()['health']=='healthy' and inspect()['restartCount']>c['before']['restartCount'])
        fired(c,'ContainerRestarted');finish(c)
        live('between-c-d','waiting for ContainerRestarted inactive');print('Waiting full restart window before d',flush=True)
        wait(lambda:state('ContainerRestarted')=='inactive',380)
        d=start('d-memory',['ContainerHighMemory','ContainerRestarted'])
        for mb in [80,100]:
            r=http(API+'/api/chaos/leak?mb='+str(mb),'POST');d['requests'].append(r);assert r['status']==200
        # Follow the lab's extra20MiB clause only when measured memory is low.
        time.sleep(12)
        pct=query('100 * container_memory_working_set_bytes{name="devops-labs-api-1"} / (container_spec_memory_limit_bytes{name="devops-labs-api-1"}>0)')
        d['memoryAfter180MiB']=pct
        if pct and float(pct[-1]['value'][1])<80:
            d['requests'].append(http(API+'/api/chaos/leak?mb=20','POST'))
        fired(d,'ContainerHighMemory')
        d['requests'].append(http(API+'/api/chaos/leak?mb=60','POST'))
        wait(lambda:inspect()['running'] and inspect()['health']=='healthy' and inspect()['restartCount']>d['before']['restartCount'])
        fired(d,'ContainerRestarted');finish(d)
        wait(lambda:state('ContainerHighMemory')=='inactive')
        e=start('e-down',['ApiDown']);run('docker','compose','stop','api');e['stopCompletedUtc']=utc()
        fired(e,'ApiDown');run('docker','compose','start','api');e['startCompletedUtc']=utc()
        wait(lambda:inspect()['health']=='healthy');wait(lambda:state('ApiDown')=='inactive');finish(e)
        save('business-after-restarts',{'utc':utc(),'counter':raw_counter(),'resetExpected':True,'projectRetained':http(API+'/api/projects/'+str(project['body']['id'])),'taskRetained':http(API+'/api/tasks/'+str(created['body']['id']))})
    finally:
        run('docker','compose','start','api')
        load.terminate();load.wait(timeout=15);load_file.close();load_err.close()
        stop.set();worker.join(timeout=15);events.terminate();events.wait(timeout=10);event_file.close();event_err.close()
        save('observer-errors',observer_errors);save('phases',phases)
        save('final',{'utc':utc(),'inspection':inspect(),'info':http(API+'/'),'live':http(API+'/health/live'),'ready':http(API+'/health/ready'),
            'targets':http(PROM+'/api/v1/targets'),'loadStopped':load.poll() is not None})
    assert len(phases)==5 and not observer_errors
    print('All five scenarios finished; API restored; raw rule timeline retained.',flush=True)

if __name__=='__main__':main()
