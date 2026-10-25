# Қолданба ақаулары және қайта іске қосу — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

11-материал: төрт нақты тізбек — HTTP 500 кезінде процесс сақталуы; crash exit 1 және автоматты қайта қосылу; restart=no кезінде Exited(1); SIGTERM арқылы қалыпты тоқтау, exit 0. T1/T2/T3 журналдары мен уақыттары сақталған. T3 ішінде контейнер қайта жасалғанда бір EOF/exit 1 болған; кейін өлшеу жалғасқан, қате жасырылмаған.

35/35 дәлел тексеруі; Postman: 4 сұрау/10 тексеру. Бақылау жобасы мен тапсырмасы сақталған, Compose бастапқы байттарына қайтарылған, API healthy. Үш параллель CLI арнасы үш терминал суреті ретінде көрсетілмейді. Docker Desktop Logs/Inspect/Exec/Stats вкладкаларын студент қарағанын растаған; бөлек сурет сақталмаған. Тарихи PDF: 7 бет, жалпы архив: 10 есеп/76 бет; кейінгі рәсімдеу бұл тарихи сандарды өзгертпейді.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [compose-restored.json](compose-restored.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Құрылымдық дерек: [docker-desktop-inspection.json](docker-desktop-inspection.json)

- Құрылымдық дерек: [final-local.json](final-local.json)

- Құрылымдық дерек: [initial-inspection.json](initial-inspection.json)

- Құрылымдық дерек: [marker.json](marker.json)

- Құрылымдық дерек: [observation-streams.json](observation-streams.json)

- Бастапқы журнал: [postman-failure-checks.txt](postman-failure-checks.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Құрылымдық дерек: [resource-summary.json](resource-summary.json)

- Құрылымдық дерек: [restored-after-no.json](restored-after-no.json)

- Бастапқы журнал: [scenario-2-request-error-logs.txt](scenario-2-request-error-logs.txt)

- Құрылымдық дерек: [scenario-2-request-error.json](scenario-2-request-error.json)

- Бастапқы журнал: [scenario-3-auto-restart-logs.txt](scenario-3-auto-restart-logs.txt)

- Құрылымдық дерек: [scenario-3-auto-restart.json](scenario-3-auto-restart.json)

- Бастапқы журнал: [scenario-4-no-restart-logs.txt](scenario-4-no-restart-logs.txt)

- Құрылымдық дерек: [scenario-4-no-restart.json](scenario-4-no-restart.json)

- Бастапқы журнал: [scenario-5-graceful-stop-logs.txt](scenario-5-graceful-stop-logs.txt)

- Құрылымдық дерек: [scenario-5-graceful-stop.json](scenario-5-graceful-stop.json)

- Құрылымдық дерек: [source-references.json](source-references.json)

- Бастапқы журнал: [t1-commands.txt](t1-commands.txt)

- Оқиғалар тізбегі: [t2-events.jsonl](t2-events.jsonl)

- Бастапқы журнал: [t2-stderr.txt](t2-stderr.txt)

- Оқиғалар тізбегі: [t3-stats.jsonl](t3-stats.jsonl)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](checks.json)
- [Дәлел 2](initial-inspection.json)
- [Дәлел 3](marker.json)
- [Дәлел 4](t1-commands.txt)
- [Дәлел 5](t2-events.jsonl)
- [Дәлел 6](t2-stderr.txt)
- [Дәлел 7](t3-stats.jsonl)
- [Дәлел 8](resource-summary.json)
- [Дәлел 9](observation-streams.json)
- [Дәлел 10](scenario-2-request-error.json)
- [Дәлел 11](scenario-2-request-error-logs.txt)
- [Дәлел 12](scenario-3-auto-restart.json)
- [Дәлел 13](scenario-3-auto-restart-logs.txt)
- [Дәлел 14](scenario-4-no-restart.json)
- [Дәлел 15](scenario-4-no-restart-logs.txt)
- [Дәлел 16](restored-after-no.json)
- [Дәлел 17](scenario-5-graceful-stop.json)
- [Дәлел 18](scenario-5-graceful-stop-logs.txt)
- [Дәлел 19](final-local.json)
- [Дәлел 20](compose-restored.json)
- [Дәлел 21](docker-desktop-inspection.json)
- [Дәлел 22](postman-results.json)
- [Дәлел 23](postman-failure-checks.txt)
- [Дәлел 24](source-references.json)
- [Дәлел 25](../../reports/lab06-failures-report.pdf)
- [Дәлел 26](../../docs/lab06-failures.md)
- [Дәлел 27](../../scripts/check-lab11-evidence.py)

## Есеп және қабылдау шектері

[Есеп 6.1](../../reports/lab06-failures-report.pdf)

[Нұсқаулық](../../docs/lab06-failures.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
