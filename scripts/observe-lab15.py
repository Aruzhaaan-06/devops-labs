"""Observe real coursework alert states and own one bounded load process.

Only talks to the fixed localhost Prometheus. The optional load writes a new
project/tasks in the fixed local coursework API. Create OUTPUT/STOP to finish.
The observer never probes the application to discover the incident.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen
import argparse,json,subprocess,time

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--with-load',action='store_true')
    parser.add_argument('--seconds',type=int,default=3600)
    args=parser.parse_args();assert 60<=args.seconds<=7200
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    assert (args.repo/'scripts/load.ps1').is_file()
    load=None;files=[];start=time.monotonic();errors=[];last=None
    def utc():return datetime.now(timezone.utc).isoformat()
    def save(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    try:
        if args.with_load:
            stdout=(out/'load-console.txt').open('w',encoding='utf-8');stderr=(out/'load-stderr.txt').open('w',encoding='utf-8');files=[stdout,stderr]
            load=subprocess.Popen(['pwsh','-NoProfile','-File','scripts/load.ps1','-Iterations','20000'],cwd=args.repo,stdout=stdout,stderr=stderr)
            save('owned-load.json',{'pid':load.pid,'startedUtc':utc(),'iterationsLimit':20000,'delayMs':300,'baseUrl':'http://localhost:8088'})
        with (out/'alerts-timeline.jsonl').open('w',encoding='utf-8',buffering=1) as f:
            while not (out/'STOP').exists() and time.monotonic()-start<args.seconds:
                try:
                    with urlopen('http://localhost:9090/api/v1/rules?type=alert',timeout=10) as response:body=json.load(response)
                    assert body['status']=='success'
                    phase=(out/'phase.txt').read_text(encoding='utf-8').strip() if (out/'phase.txt').exists() else 'baseline'
                    row={'observedUtc':utc(),'epoch':time.time(),'phase':phase,'groups':body['data']['groups']}
                    f.write(json.dumps(row,ensure_ascii=False)+'\n')
                    state=next(r['state'] for g in row['groups'] for r in g['rules'] if r['name']=='ApiSlowRequests')
                    if state!=last:
                        print(row['observedUtc'],phase,'ApiSlowRequests',state,flush=True);last=state
                    if phase=='bad-deploy' and state=='firing' and not (out/'first-firing.json').exists():
                        save('first-firing.json',row)
                        print('ALERT DETECTED: first-firing.json retained',flush=True)
                except Exception as error:errors.append({'utc':utc(),'error':str(error)})
                time.sleep(1)
    finally:
        if load is not None and load.poll() is None:
            load.terminate()
            try:load.wait(timeout=15)
            except subprocess.TimeoutExpired:load.kill();load.wait(timeout=5)
        for file in files:file.close()
        save('observer-final.json',{'utc':utc(),'errors':errors,'loadStopped':load is None or load.poll() is not None,
            'stopRequested':(out/'STOP').exists(),'durationSeconds':round(time.monotonic()-start,3)})
    print('Observer closed; owned load stopped',flush=True)

if __name__=='__main__':main()
