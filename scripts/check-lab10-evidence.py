"""Check saved lab 10 evidence. Does not contact GitHub or change containers."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
EV=ROOT/'evidence/lab05-cd'
load=lambda n:json.loads((EV/n).read_text(encoding='utf-8-sig'))
checks=[]
def check(name,condition):checks.append({'name':name,'passed':bool(condition)})
def jobs(name):return {j['name']:j['conclusion'] for j in load(name+'-jobs.json')['jobs']}
baseline=load('baseline-runtime.json'); message=load('message-runtime.json'); repeat=load('repeat-runtime.json')
old='sha-8511c6c'; new='sha-349a0b1'
check('Initial PR merged to baseline main',load('first-merge.json')['merged'] and load('first-merge.json')['sha'].startswith(old[4:]))
check('Initial full pipeline success',jobs('baseline')=={'test':'success','image':'success','deploy':'success'})
check('Initial API version matches baseline main',baseline['info']['body']['version']==old and 'message' not in baseline['info']['body'])
check('Message PR merged',load('message-pr.json')['merged'] and load('message-pr.json')['merge_commit_sha'].startswith(new[4:]))
check('Code owner approved message PR',any(r['state']=='APPROVED' and r['user']=='temirkhanerbolatovich-coder' for r in load('message-reviews.json')))
check('PR test passed without publishing or deploy',jobs('message-pr')=={'test':'success','image':'skipped','deploy':'skipped','rollback':'skipped'})
check('New main pipeline passed',jobs('message-main')=={'test':'success','image':'success','deploy':'success','rollback':'skipped'})
check('Message and configured main version returned',message['info']['body']['message']=='hello from CI/CD' and message['info']['body']['version']==new)
check('InMemory tests passed 39/39',load('inmemory-tests.json')['counters']['passed']=='39' and load('inmemory-tests.json')['counters']['failed']=='0')
log=(EV/'message-main-ci-log.txt').read_text(encoding='utf-8')
check('Actual PostgreSQL CI passed 39 tests',bool(re.search(r'Passed:\s+39.*Total:\s+39',log)) and 'Storage: Postgres' in log)
postman=load('postman-results.json')
check('Real API Postman 38 requests, 103 assertions',postman['requests']==38 and postman['assertions']==103 and postman['failedAssertions']==0 and postman['exitCode']==0)
check('Same-tag deploy preserves container identity',message['apiContainerId']==repeat['apiContainerId'] and message['apiStartedAt']==repeat['apiStartedAt'])
check('Same-tag deploy completed',jobs('repeat')['deploy']=='success')
manual=load('manual-rollback-runtime.json'); timing=load('manual-rollback-timing.json')
check('Manual rollback selects old version without message',manual['info']['body']['version']==old and 'message' not in manual['info']['body'])
check('Manual rollback duration measured',timing['seconds']==12.823 and timing['startUtc']<timing['confirmedUtc'])
check('Restore through Re-run all jobs succeeded',jobs('return-after-manual')=={'test':'success','image':'success','deploy':'success','rollback':'skipped'})
check('Main restored after manual rollback',load('return-after-manual-runtime.json')['info']['body']['version']==new)
button=load('button-rollback-runtime.json')
check('Button rollback uses workflow_dispatch',load('button-run.json')['event']=='workflow_dispatch' and load('button-dispatch.json')['tag']==old)
check('Button only executes rollback job',jobs('button')=={'test':'skipped','image':'skipped','deploy':'skipped','rollback':'success'})
check('Button rollback returns old response',button['info']['body']['version']==old and 'message' not in button['info']['body'])
check('Button duration includes approval and queue',load('button-rollback-timing.json')['seconds']==57.696)
check('Main restored after button rollback',load('return-after-button-runtime.json')['info']['body']['version']==new and jobs('return-after-button')['deploy']=='success')
env=load('environment-local.json')
rule=next(r for r in env['protection_rules'] if r['type']=='required_reviewers')
check('Local Environment requires owner approval',env['name']=='local' and any(r['reviewer']['login']=='Aruzhaaan-06' for r in rule['reviewers']))
check('Protected branches only and no admin bypass',env['deployment_branch_policy']['protected_branches'] and env['can_admins_bypass'] is False)
check('Deploy and rollback actually waited for local approval',any(e['environment']['name']=='local' for e in load('message-main-pending-approval.json')) and any(e['environment']['name']=='local' for e in load('button-pending-approval.json')))
check('Release pipeline publishes without deploy',load('release-run.json')['head_branch']=='v1.0.0' and jobs('release')=={'test':'success','image':'success','deploy':'skipped','rollback':'skipped'})
check('Release did not recreate running API',load('release-no-deploy-check.json')['passed'])
manifests=load('registry-manifests.json')
check('Four GHCR tags resolve to real manifests',{x['tag'] for x in manifests}=={old,new,'latest','1.0.0'} and all(x['manifest'].get('schemaVersion')==2 for x in manifests))
marker=load('marker.json')
names=['baseline-runtime','message-runtime','repeat-runtime','manual-rollback-runtime','return-after-manual-runtime','button-rollback-runtime','return-after-button-runtime','release-runtime']
check('Control project and task persisted through all phases',all(load(n+'.json')['markerProject']['body']==marker['project'] and load(n+'.json')['markerTask']['body']==marker['task'] for n in names))
check('Named PostgreSQL volume retained throughout',all(any(v['name']=='devops-labs_pgdata' for v in load(n+'.json')['databaseVolumes']) for n in names))
check('Live and ready endpoints healthy throughout',all(load(n+'.json')['live']['status']==200 and load(n+'.json')['ready']['status']==200 and load(n+'.json')['health']=='healthy' for n in names))
ruleset=load('ruleset.json')
check('Required test and PR approval retained',ruleset['enforcement']=='active' and any(r['type']=='required_status_checks' and any(c['context']=='test' for c in r['parameters']['required_status_checks']) for r in ruleset['rules']) and any(r['type']=='pull_request' and r['parameters']['required_approving_review_count']==1 for r in ruleset['rules']))
check('External workflows still require approval',load('fork-approval.json')['approval_policy']=='all_external_contributors')
check('Required genuine screenshots saved',all((EV/'screenshots'/n).read_bytes()[:2]==b'\xff\xd8' for n in ['baseline-pipeline.jpg','packages-tags.jpg','deploy-summary.jpg']))
summary={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,
    'scope':'Saved evidence consistency and acceptance conditions for material 10; not a substitute for live final verification.'}
(EV/'checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(1 if summary['failed'] else 0)
