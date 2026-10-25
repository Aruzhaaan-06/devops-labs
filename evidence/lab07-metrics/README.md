# Метрикалар және PromQL — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 24 қазан, 13-материал; API sha-e8be38f, Storage PostgreSQL. Негізгі өлшем: 16:40:13 UTC (21:40:13 UTC+5). Үш нысан UP; бес берілген және төрт жеке PromQL өрнегі тексерілген. Raw /metrics, instant/query_range, нақты 400/409 жауаптары және Chrome арқылы түсірілген 13 PNG сақталған. Трафиксіз әдістердің p95 мәні NaN күйінде қалдырылған; increase бөлшек болуы мүмкін.

Жүктеме: 1200 итерация, 0 қате, project 26 ішінде 1200 InProgress. Процесс аяқталған, 10–12-кезең бақылау нысандары сақталған. Postman тек оқу режимінде: 5 сұрау/15 тексеру/0 қате. 28 дәлел тексеруі бар. Container жазбаларында Config.Env жоқ; cAdvisor тек оқу API-імен шектелген. Суреттер қайта сызылмаған. Соңғы main/runtime дәлелі lab13-final-verification.json релиз файлында; бұл өлшем сәтінен бөлек.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Бастапқы журнал: [api-metrics.txt](api-metrics.txt)

- Бастапқы журнал: [cadvisor-metrics.txt](cadvisor-metrics.txt)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [containers.json](containers.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Құрылымдық дерек: [error-requests.json](error-requests.json)

- Құрылымдық дерек: [initial.json](initial.json)

- Бастапқы журнал: [load-console.txt](load-console.txt)

- Құрылымдық дерек: [load-results.json](load-results.json)

- Құрылымдық дерек: [own-4xx.json](own-4xx.json)

- Құрылымдық дерек: [own-created.json](own-created.json)

- Құрылымдық дерек: [own-memory.json](own-memory.json)

- Құрылымдық дерек: [own-p95.json](own-p95.json)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Бастапқы журнал: [promtool.txt](promtool.txt)

- Құрылымдық дерек: [repeated-errors.json](repeated-errors.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Құрылымдық дерек: [required-cpu.json](required-cpu.json)

- Құрылымдық дерек: [required-memory.json](required-memory.json)

- Құрылымдық дерек: [required-p95.json](required-p95.json)

- Құрылымдық дерек: [required-rps.json](required-rps.json)

- Құрылымдық дерек: [required-up.json](required-up.json)

- Құрылымдық дерек: [retained-markers.json](retained-markers.json)

- Құрылымдық дерек: [rules.json](rules.json)

- Каталог: [screenshots](screenshots/)

- Құрылымдық дерек: [screenshots.json](screenshots.json)

- Құрылымдық дерек: [summary.json](summary.json)

- Құрылымдық дерек: [targets.json](targets.json)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](https://github.com/Aruzhaaan-06/devops-labs/pull/22)
- [Дәлел 2](../../reports/lab07-metrics-report.pdf)
- [Дәлел 3](../../docs/lab07-metrics.md)
- [Дәлел 4](screenshots/targets-up.png)
- [Дәлел 5](screenshots/own-created.png)
- [Дәлел 6](screenshots/own-memory.png)
- [Дәлел 7](screenshots/own-p95.png)
- [Дәлел 8](screenshots/own-4xx.png)

## Есеп және қабылдау шектері

[Есеп 7.1](../../reports/lab07-metrics-report.pdf)

[Нұсқаулық](../../docs/lab07-metrics.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
