"""Save real monitoring responses and evaluate the nine lab 7 part 1 queries.

Requires the local API and monitoring Compose projects plus active load.ps1.
Creates a small named project to demonstrate HTTP 400/409; keeps it as evidence.
Never stops services or changes existing projects. Output must be a new directory.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import argparse,json,math,subprocess,time

QUERIES={
    'required-up':'up',
    'required-rps':'sum by (controller, action) (rate(http_requests_received_total{job="demo-api"}[1m]))',
    'required-p95':'histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job="demo-api"}[1m])))',
    'required-memory':'container_memory_working_set_bytes{name="devops-labs-api-1"} / 1024 / 1024',
    'required-cpu':'sum by (name) (rate(container_cpu_usage_seconds_total{name=~"devops-labs-.*"}[1m]))',
    'own-created':'sum(increase(http_requests_received_total{job="demo-api",controller="Tasks",action="Create",code="201"}[1m]))',
    'own-memory':'100 * container_memory_working_set_bytes{name="devops-labs-api-1"} / (container_spec_memory_limit_bytes{name="devops-labs-api-1"} > 0)',
    'own-p95':'histogram_quantile(0.95, sum by (le, controller, action) (rate(http_request_duration_seconds_bucket{job="demo-api"}[1m])))',
    'own-4xx':'sum by (controller, action, code) (rate(http_requests_received_total{job="demo-api",code=~"4.."}[1m]))',
}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    def save(name,value):
        (out/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    def http(url,method='GET',body=None):
        req=Request(url,method=method,headers={'Content-Type':'application/json'},
            data=json.dumps(body).encode() if body is not None else None)
        try:r=urlopen(req,timeout=20)
        except HTTPError as error:r=error
        text=r.read().decode('utf-8');content=r.headers.get('Content-Type','')
        return {'utc':datetime.now(timezone.utc).isoformat(),'method':method,'url':url,'status':r.status,
                'body':json.loads(text) if 'json' in content else text}
    api='http://localhost:8088';prom='http://localhost:9090'
    initial=http(api+'/');save('initial',initial)
    assert initial['status']==200
    bad=http(api+'/api/projects','POST',{'name':''})
    project=http(api+'/api/projects','POST',{'name':'lab13-errors-'+str(int(time.time()))})
    assert project['status']==201
    task=http(api+'/api/tasks','POST',{'projectId':project['body']['id'],'title':'lab13-Todo-to-Done'})
    assert task['status']==201
    conflict=http(api+'/api/tasks/'+str(task['body']['id'])+'/status','PATCH',{'status':'Done'})
    save('error-requests',{'badProject':bad,'project':project,'task':task,'conflict':conflict})
    assert bad['status']==400 and conflict['status']==409
    # Two scrapes after creating the error series give rate() enough samples.
    time.sleep(12)
    # A second increment makes the newly created error counters measurable.
    bad2=http(api+'/api/projects','POST',{'name':''})
    conflict2=http(api+'/api/tasks/'+str(task['body']['id'])+'/status','PATCH',{'status':'Done'})
    save('repeated-errors',{'badProject':bad2,'conflict':conflict2})
    time.sleep(8)
    targets=http(prom+'/api/v1/targets');save('targets',targets)
    active=targets['body']['data']['activeTargets']
    assert len(active)==3 and all(x['health']=='up' for x in active)
    for port,name in [(8088,'api'),(8081,'cadvisor')]:
        raw=http('http://localhost:'+str(port)+'/metrics')
        assert raw['status']==200
        wanted=('http_requests_received_total','http_request_duration_seconds_bucket') if name=='api' else ('container_memory_working_set_bytes','container_spec_memory_limit_bytes','container_cpu_usage_seconds_total','container_start_time_seconds')
        lines=[s for s in raw['body'].splitlines() if s.startswith(wanted) and (name=='api' or 'name="devops-labs-api-1"' in s)]
        assert lines
        (out/(name+'-metrics.txt')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    results={};now=time.time()
    for name,expr in QUERIES.items():
        instant=http(prom+'/api/v1/query?'+urlencode({'query':expr,'time':now}))
        result=instant['body']['data']['result']
        assert instant['body']['status']=='success' and result, name
        assert all(math.isfinite(float(s['value'][1])) for s in result),name
        if name=='required-up':assert all(s['value'][1]=='1' for s in result)
        if name=='own-created':assert float(result[0]['value'][1])>0
        if name=='own-memory':assert 0<float(result[0]['value'][1])<100
        if name=='own-4xx':assert {s['metric']['code'] for s in result if float(s['value'][1])>0}>={'400','409'}
        ranged=http(prom+'/api/v1/query_range?'+urlencode({'query':expr,'start':now-180,'end':now,'step':5}))
        assert ranged['body']['status']=='success'
        results[name]={'expression':expr,'instant':instant,'range':ranged}
        save(name,results[name])
    rules=http(prom+'/api/v1/rules');save('rules',rules)
    assert sum(len(g['rules']) for g in rules['body']['data']['groups'])==5
    save('summary',{'utc':datetime.now(timezone.utc).isoformat(),'queries':len(results),
        'targets':{x['labels']['job']:x['health'] for x in active},'errors':[400,409],
        'values':{n:[{'labels':s['metric'],'value':s['value'][1]} for s in v['instant']['body']['data']['result']] for n,v in results.items()},
        'loadRequired':True,'sourceVersion':initial['body'].get('version')})
    print('Nine queries returned finite samples; three targets UP; genuine 400/409 confirmed.')

if __name__=='__main__':main()
