# 12-материал: ресурстар және дайындық дәлелдері

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 2026-10-24**

[38 шарт сәтті](checks.json), қате0. 6-9-тармақтар және қосымша diag.ps1 орындалды; толық 2-8 кестесі бұрынғы дәлелдермен біріктірілді. Осы күнгі жергілікті код - main2dd5a9f, APP_VERSION=lab12-2dd5a9f.

| Дәлел | Нақты файл |
|---|---|
| Жергілікті build/up және бастапқы healthy | [build журналы](local-build-up.txt), [baseline](baseline.json), [initial](initial.json) |
| T1 пәрмендер және HTTP | [t1-commands.txt](t1-commands.txt) |
| T2 нақты үздіксіз events | [t2-events.jsonl](t2-events.jsonl), [stderr бос](t2-stderr.txt) |
| T3 ресурс өлшемдері | [38 топтама](t3-stats.jsonl), [37 API үлгісі/78,58% максимум](resource-summary.json) |
| 6: OOM | [80/160MB, transport error, before/after, cgroup, events](scenario-6-oom.json), [startup логтары](scenario-6-oom-logs.txt) |
| 7: БД ақауы | [live200/ready503/tasks500, restart жоқ](scenario-7-db-unavailable.json), [Npgsql/Error](scenario-7-db-unavailable-logs.txt) |
| БД қалпына келді | [сол API ID және сақталған деректер](db-restored.json) |
| 8: unhealthy | [HTTP404/curl22 Health.Log және restart жоқ](scenario-8-unhealthy.json), [қолданба логы](scenario-8-unhealthy-logs.txt) |
| 9: баяу жауап | [0,114133 с және 3,027295 с](scenario-9-slow-response.json), [лог](scenario-9-slow-response-logs.txt) |
| Бақылау деректері | [marker](marker.json), [final-local healthy және том](final-local.json) |
| Compose толық қайтарылды | [Бастапқы/соңғы байттар SHA-256](compose-restored.json) |
| diag OOM тарихын тапты | [ағымдағы OOMKilled=false және тарихи oom/die137](diag-after-oom.txt) |
| diag қалыпты/жоқ контейнер | [нәтиже](diag-tests.json), [healthy](diag-healthy.txt), [missing](diag-missing.txt) |
| Тәжірибе скриптінің бастапқы қорғанысы | [Қате тег қабылданбады; API/DB ID, StartedAt, RestartCount және Compose өзгермеді](preflight-tests.json) |
| Postman нақты API | [5/11, exit0](postman-results.json), [толық CLI шығысы](postman-resources.txt) |
| Толық кестенің бұрынғы 2-5 бөлігі | [11-материал файлдарының SHA-256](part1-references.json) |
| Әдістеме және ресми дереккөздер | [source-references.json](source-references.json) |

OOM оқиғасы exit137 себебін растайды. Қайта іске қосылған State.OOMKilled=false/ExitCode0 және жаңа cgroup-тағы oom_kill0 бұрынғы өлімді жоққа шығармайды. T3 үлгілері жадтың шын шыңын өткізіп алуы мүмкін. Бір stats EOF/exit1 Compose recreation аралығында сақталды; келесі өлшемдер жалғасты.

БД және unhealthy кезінде API процесі аяқталған жоқ; HTTP500 мен healthcheck exit22 процесс exit code-ына тең емес. Health.Log404 - қате тексерудің белгісі, ал нақты live/ready сол уақытта200 болған. Баяу жауап - жеке сұраудың өлшемі; load benchmark/p95/p99 өлшемі ретінде берілмейді.

2-5-сценарийлер 2026-10-23 тәжірибесінен, осы күнгі 6-9 тәжірибелерінен бөлек көрсетілген. Docker daemon оқиғаларының буфері тарихи архив емес. Үш CLI арнасы параллель процестерде орындалды; үш көрінетін терезе суреті ретінде көрсетілмейді.

DB_PASSWORD пен GitHub токендері жарияланбады; Config.Env сақталмады. Postman cloud-қа жариялау орындалмады; CLI login ескертуі жергілікті 5/11 нәтижесін өзгертпейді. Негізгі src/tests/Dockerfile/compose.yaml мінез-құлқы өзгертілмеді. Бұрынғы оқытушы/тәуелсіз парлық ревью және қолмен сдача тармақтары сақталды.

[Орындау және жауаптар](../../docs/lab06-resources.md) · [Қазақша PDF](../../reports/lab06-resources-report.pdf) · [diag.ps1](../../scripts/diag.ps1) · [Офлайн тексеру](../../scripts/check-lab12-evidence.py)
