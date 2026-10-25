# Инцидентті анықтау және қалпына келтіру — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 24 қазан, 15-материал. Тек жергілікті оқу стенді. T0: 18:10:54 UTC, PR #26 біріктірілген; T1: 18:14:18.726369 UTC, алғашқы сақталған ApiSlowRequests firing; T2: 18:15:58.875623 UTC, sha-cf768be қайтарылған және алерт inactive. Анықтау: 204,726 с, оның ішінде CI/жинақтау/кезек/deploy бар. Қалпына келтіру: 100,149 с, оның ішінде диагностика/dispatch/мақұлдау/runner/растау бар.

Tasks/List p95: 1,9968 с; алерттен кейінгі HTTP 200 сұрауы: 1,512395 с. Гистограмма бағасы мен нақты сұрау уақыты араластырылмайды. T1-ге дейін қолмен API сұрауы жасалмаған; CI smoke, жүктеме және Prometheus бақылаушысы жұмыс істеген. GitHub нақты Revert PR #28 жасаған, src/tests қалпына келген; кейінгі p95 шамамен 1,76 ms. Төрт тарихи PostgreSQL CI: 40/40.

Latency smoke нашар нұсқада 1615,960 ms нәтижесін қабылдамаған (exit 1); түзетілген нұсқада 98,281/4,096/2,590 ms өткен (exit 0). #29 және #31 жабылған; қосымша performance baseline #30 ашық. Жоба 37 ішінде 1771 InProgress тапсырмасы мен нақты жиынтық хэші сақталған. Бес көлік қатесі сәтті сұрау ретінде саналмаған. Жүктеме мен бақылаушы тоқтатылған; 20 000 шегі аяқталған цикл саны емес.

Postman: тек оқу, 6 сұрау/13 тексеру/0 қате; бес ереже inactive. PDF графигі шынайы Prometheus деректерінен құрылған, UI скриншоты емес. UI суреттері, форум слоты, онлайн қорғау және СДО тармақтары ашық. Соңғы main/runtime релиздегі lab15-final-verification.json ішінде; ол инциденттің ертеректегі уақыттарынан бөлек.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Құрылымдық дерек: [alert-range.json](alert-range.json)

- Оқиғалар тізбегі: [alerts-timeline.jsonl](alerts-timeline.jsonl)

- Бастапқы журнал: [bad-latency-guard.txt](bad-latency-guard.txt)

- Құрылымдық дерек: [baseline.json](baseline.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [ci-summary.json](ci-summary.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Құрылымдық дерек: [diagnosis.json](diagnosis.json)

- Құрылымдық дерек: [first-firing.json](first-firing.json)

- Бастапқы журнал: [fixed-api-logs.txt](fixed-api-logs.txt)

- Құрылымдық дерек: [github-links.json](github-links.json)

- Бастапқы журнал: [good-latency-guard.txt](good-latency-guard.txt)

- Құрылымдық дерек: [incident-metrics.json](incident-metrics.json)

- Құрылымдық дерек: [latency-guard.json](latency-guard.json)

- Бастапқы журнал: [load-console.txt](load-console.txt)

- Бастапқы журнал: [load-stderr.txt](load-stderr.txt)

- Құрылымдық дерек: [load-tasks.json](load-tasks.json)

- Құрылымдық дерек: [observer-final.json](observer-final.json)

- Құрылымдық дерек: [owned-load.json](owned-load.json)

- Құрылымдық дерек: [p95-actions-range.json](p95-actions-range.json)

- Құрылымдық дерек: [p95-global-range.json](p95-global-range.json)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Құрылымдық дерек: [postmortem.json](postmortem.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Құрылымдық дерек: [retained-data.json](retained-data.json)

- Құрылымдық дерек: [revert-operation.json](revert-operation.json)

- Құрылымдық дерек: [revert-recovered.json](revert-recovered.json)

- Құрылымдық дерек: [rollback-dispatch.json](rollback-dispatch.json)

- Құрылымдық дерек: [snapshot-after-revert.json](snapshot-after-revert.json)

- Құрылымдық дерек: [source-proof.json](source-proof.json)

- Құрылымдық дерек: [T0.json](T0.json)

- Құрылымдық дерек: [T1.json](T1.json)

- Құрылымдық дерек: [T2.json](T2.json)

- Құрылымдық дерек: [ui-status.json](ui-status.json)

- Құрылымдық дерек: [up-range.json](up-range.json)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](https://github.com/Aruzhaaan-06/devops-labs/issues/27)
- [Дәлел 2](https://github.com/Aruzhaaan-06/devops-labs/issues/27#issuecomment-6387899631)
- [Дәлел 3](https://github.com/Aruzhaaan-06/devops-labs/pull/26)
- [Дәлел 4](https://github.com/Aruzhaaan-06/devops-labs/pull/28)
- [Дәлел 5](../../reports/lab08-incident-report.pdf)
- [Дәлел 6](../../docs/lab08-incident.md)

## Есеп және қабылдау шектері

[Есеп 8](../../reports/lab08-incident-report.pdf)

[Нұсқаулық](../../docs/lab08-incident.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
