# Grafana панельдері және алерттер — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 24 қазан, 14-материал, API lab14-7d78755. Бес сценарийде алты күтілетін firing ауысуы жазылған. ContainerRestarted үшін for=0, pending жоқ. a–c бастапқы іске қосудан, d–e сәтті жалғастырудан алынған; бақылау журналындағы үзіліс жасырылмаған. Бастапқы 80+100 MiB әрекеті ерте OOM туғызған және сәтті warning→OOM ретінде есептелмеген. Қайталауда 20 MiB қадамдар қолданылған.

demo_tasks_created_total тек сәтті сақтау операциясынан кейін өседі. 400/404 өсірмейді; санауыш процесс деңгейінде, БД жолдарының саны емес. Жаңа процесте бірінші Create-ке дейін метрика болмауы мүмкін; бастапқы тексеру оны 0 деп қабылдайды, кейінгі екі тексеру нақты жол мен initial+1 талап етеді. InMemory: 40/40; арнайы тест: 1/1; Postman: 10 сұрау/17 тексеру/0 қате; 30 дәлел тексеруі.

Grafana UID demo-api, 7 панель. Windows bind mount watch жұмыс істемегендіктен 20 s polling қосылған; өзгеріс 19,429 s кейін екінші restart-сіз көрінген. UI Add/Export және ақау кезіндегі Grafana/Dozzle визуалды бақылауы орындалмаған; API нәтижелері оларды алмастырмайды. Алдыңғы 1200 және жаңа 2231/531 тапсырма сақталған, жүктеме тоқтатылған, ready/live 200, 3 UP.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Бастапқы журнал: [a-errors-logs.txt](a-errors-logs.txt)

- Құрылымдық дерек: [a-errors.json](a-errors.json)

- Құрылымдық дерек: [alerts-range.json](alerts-range.json)

- Оқиғалар тізбегі: [alerts-timeline.jsonl](alerts-timeline.jsonl)

- Бастапқы журнал: [b-slow-logs.txt](b-slow-logs.txt)

- Құрылымдық дерек: [b-slow.json](b-slow.json)

- Құрылымдық дерек: [business-after-restarts.json](business-after-restarts.json)

- Құрылымдық дерек: [business-counter.json](business-counter.json)

- Құрылымдық дерек: [business-range.json](business-range.json)

- Бастапқы журнал: [c-crash-logs.txt](c-crash-logs.txt)

- Құрылымдық дерек: [c-crash.json](c-crash.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Бастапқы журнал: [d-memory-logs.txt](d-memory-logs.txt)

- Құрылымдық дерек: [d-memory.json](d-memory.json)

- Құрылымдық дерек: [dashboard-provisioning.json](dashboard-provisioning.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [docker-events-stderr.txt](docker-events-stderr.txt)

- Оқиғалар тізбегі: [docker-events.jsonl](docker-events.jsonl)

- Бастапқы журнал: [e-down-logs.txt](e-down-logs.txt)

- Құрылымдық дерек: [e-down.json](e-down.json)

- Құрылымдық дерек: [final.json](final.json)

- Құрылымдық дерек: [grafana-provisioned.json](grafana-provisioned.json)

- Құрылымдық дерек: [http-range.json](http-range.json)

- Құрылымдық дерек: [initial-attempt-business-counter.json](initial-attempt-business-counter.json)

- Оқиғалар тізбегі: [initial-attempt-docker-events.jsonl](initial-attempt-docker-events.jsonl)

- Құрылымдық дерек: [initial-attempt-final.json](initial-attempt-final.json)

- Бастапқы журнал: [initial-attempt-load-console.txt](initial-attempt-load-console.txt)

- Бастапқы журнал: [initial-attempt-load-stderr.txt](initial-attempt-load-stderr.txt)

- Құрылымдық дерек: [initial-attempt-phases.json](initial-attempt-phases.json)

- Құрылымдық дерек: [initial.json](initial.json)

- Құрылымдық дерек: [live-phase.json](live-phase.json)

- Бастапқы журнал: [load-console.txt](load-console.txt)

- Бастапқы журнал: [load-stderr.txt](load-stderr.txt)

- Құрылымдық дерек: [local-tests.json](local-tests.json)

- Құрылымдық дерек: [observer-errors.json](observer-errors.json)

- Құрылымдық дерек: [phases.json](phases.json)

- Құрылымдық дерек: [polling-reload.json](polling-reload.json)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Құрылымдық дерек: [restarts-range.json](restarts-range.json)

- Құрылымдық дерек: [retained-data.json](retained-data.json)

- Құрылымдық дерек: [scenario-table.json](scenario-table.json)

- Құрылымдық дерек: [unchanged-config.json](unchanged-config.json)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](https://github.com/Aruzhaaan-06/devops-labs/pull/23)
- [Дәлел 2](../../reports/lab07-alerts-report.pdf)
- [Дәлел 3](../../docs/lab07-alerts.md)

## Есеп және қабылдау шектері

[Есеп 7.2](../../reports/lab07-alerts-report.pdf)

[Нұсқаулық](../../docs/lab07-alerts.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
