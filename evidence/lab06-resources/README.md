# Ресурстар, тәуелділік және диагностика — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

12-материал: OOM → die 137 → start; БД тоқтағанда live 200/ready 503/tasks 500, API қайта қосылмаған; HTTP 404 healthcheck салдарынан unhealthy, автоматты restart жоқ; slow 3000 ms жауабы 200 және 3,027295 с. Compose қалпына келтіріліп, бақылау деректері сақталған. 38/38 тексеру; Postman: 5 сұрау/11 тексеру.

diag.ps1 тек оқу режимінде күйді, health, RestartCount, жадыны, соңғы 20 журнал жолын және 15 минуттағы die/oom оқиғаларын береді. Config.Env оқылмайды; құпия пішімдері жасырылады. Жұмыс істейтін және жоқ контейнермен тексерілген. Қате тег өзгеріссіз қабылданбаған. 78,58% — өлшеу үлгісіндегі максимум, нақты OOM шыңы деп көрсетілмейді. Restart-тен кейінгі OOMKilled/cgroup сбросы тарихи oom оқиғасын жоққа шығармайды. Бір stats EOF сақталған; 2–5-сценарийлер алдыңғы кезеңнен, уақыттары ашық көрсетілген.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Құрылымдық дерек: [baseline.json](baseline.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [compose-restored.json](compose-restored.json)

- Құрылымдық дерек: [db-restored.json](db-restored.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [diag-after-oom.txt](diag-after-oom.txt)

- Бастапқы журнал: [diag-healthy.txt](diag-healthy.txt)

- Бастапқы журнал: [diag-missing.txt](diag-missing.txt)

- Құрылымдық дерек: [diag-tests.json](diag-tests.json)

- Құрылымдық дерек: [final-local.json](final-local.json)

- Құрылымдық дерек: [initial.json](initial.json)

- Бастапқы журнал: [local-build-up.txt](local-build-up.txt)

- Құрылымдық дерек: [marker.json](marker.json)

- Құрылымдық дерек: [part1-references.json](part1-references.json)

- Бастапқы журнал: [postman-resources.txt](postman-resources.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Құрылымдық дерек: [preflight-tests.json](preflight-tests.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Құрылымдық дерек: [resource-summary.json](resource-summary.json)

- Бастапқы журнал: [scenario-6-oom-logs.txt](scenario-6-oom-logs.txt)

- Құрылымдық дерек: [scenario-6-oom.json](scenario-6-oom.json)

- Бастапқы журнал: [scenario-7-db-unavailable-logs.txt](scenario-7-db-unavailable-logs.txt)

- Құрылымдық дерек: [scenario-7-db-unavailable.json](scenario-7-db-unavailable.json)

- Бастапқы журнал: [scenario-8-unhealthy-logs.txt](scenario-8-unhealthy-logs.txt)

- Құрылымдық дерек: [scenario-8-unhealthy.json](scenario-8-unhealthy.json)

- Бастапқы журнал: [scenario-9-slow-response-logs.txt](scenario-9-slow-response-logs.txt)

- Құрылымдық дерек: [scenario-9-slow-response.json](scenario-9-slow-response.json)

- Құрылымдық дерек: [source-references.json](source-references.json)

- Бастапқы журнал: [t1-commands.txt](t1-commands.txt)

- Оқиғалар тізбегі: [t2-events.jsonl](t2-events.jsonl)

- Бастапқы журнал: [t2-stderr.txt](t2-stderr.txt)

- Оқиғалар тізбегі: [t3-stats.jsonl](t3-stats.jsonl)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](checks.json)
- [Дәлел 2](local-build-up.txt)
- [Дәлел 3](baseline.json)
- [Дәлел 4](initial.json)
- [Дәлел 5](t1-commands.txt)
- [Дәлел 6](t2-events.jsonl)
- [Дәлел 7](t2-stderr.txt)
- [Дәлел 8](t3-stats.jsonl)
- [Дәлел 9](resource-summary.json)
- [Дәлел 10](scenario-6-oom.json)
- [Дәлел 11](scenario-6-oom-logs.txt)
- [Дәлел 12](scenario-7-db-unavailable.json)
- [Дәлел 13](scenario-7-db-unavailable-logs.txt)
- [Дәлел 14](db-restored.json)
- [Дәлел 15](scenario-8-unhealthy.json)
- [Дәлел 16](scenario-8-unhealthy-logs.txt)
- [Дәлел 17](scenario-9-slow-response.json)
- [Дәлел 18](scenario-9-slow-response-logs.txt)
- [Дәлел 19](marker.json)
- [Дәлел 20](final-local.json)
- [Дәлел 21](compose-restored.json)
- [Дәлел 22](diag-after-oom.txt)
- [Дәлел 23](diag-tests.json)
- [Дәлел 24](diag-healthy.txt)
- [Дәлел 25](diag-missing.txt)
- [Дәлел 26](preflight-tests.json)
- [Дәлел 27](postman-results.json)
- [Дәлел 28](postman-resources.txt)
- [Дәлел 29](part1-references.json)
- [Дәлел 30](source-references.json)
- [Дәлел 31](../../docs/lab06-resources.md)
- [Дәлел 32](../../reports/lab06-resources-report.pdf)
- [Дәлел 33](../../scripts/diag.ps1)
- [Дәлел 34](../../scripts/check-lab12-evidence.py)

## Есеп және қабылдау шектері

[Есеп 6.2](../../reports/lab06-resources-report.pdf)

[Нұсқаулық](../../docs/lab06-resources.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
