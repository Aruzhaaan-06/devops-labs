# GitHub Actions арқылы үздіксіз интеграция — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

09-материал. Нақты GitHub Actions сценарийі: жасыл → қызыл және merge бұғатталуы → қайта жасыл. Қате нәтиже: Expected OK / Actual Conflict, 37/38; 07ef056 түзетуінен кейін 38/38. Approve болғанымен міндетті test біріктіруге жол бермеген. 24 техникалық тексеру мен үш түпнұсқа сурет сақталған.

PR кезінде тек test; main push кезінде test → image → deploy; v тегі кезінде test → image орындалады. Hosted Ubuntu PostgreSQL қызметін пайдаланады; self-hosted Windows runner деплойға арналған. Actions SHA-ға бекітілген, checkout тіркелгі деректерін сақтамайды, құқықтар job бойынша шектелген. Runner Online/Idle және құпияның тек метадеректері тексерілген. Осы кезең соңындағы ашық PR кейін 10-материалда біріктірілген. Екі аккаунт бір иеге тиесілі.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Құрылымдық дерек: [action-pins.json](action-pins.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [failure-blocked-ui.txt](failure-blocked-ui.txt)

- Құрылымдық дерек: [failure-check-runs.json](failure-check-runs.json)

- Бастапқы журнал: [failure-ci-log.txt](failure-ci-log.txt)

- Құрылымдық дерек: [failure-jobs.json](failure-jobs.json)

- Құрылымдық дерек: [failure-pr.json](failure-pr.json)

- Құрылымдық дерек: [failure-reviews.json](failure-reviews.json)

- Құрылымдық дерек: [failure-run.json](failure-run.json)

- Құрылымдық дерек: [fork-approval.json](fork-approval.json)

- Бастапқы журнал: [initial-ci-log.txt](initial-ci-log.txt)

- Құрылымдық дерек: [initial-jobs.json](initial-jobs.json)

- Құрылымдық дерек: [initial-review.json](initial-review.json)

- Құрылымдық дерек: [initial-run.json](initial-run.json)

- Бастапқы журнал: [local-build.txt](local-build.txt)

- Бастапқы журнал: [local-restore.txt](local-restore.txt)

- Бастапқы журнал: [local-test.txt](local-test.txt)

- Құрылымдық дерек: [local-tests.json](local-tests.json)

- Құрылымдық дерек: [pipeline-pr.json](pipeline-pr.json)

- Құрылымдық дерек: [repository-secrets.json](repository-secrets.json)

- Құрылымдық дерек: [restored-check-runs.json](restored-check-runs.json)

- Бастапқы журнал: [restored-ci-log.txt](restored-ci-log.txt)

- Құрылымдық дерек: [restored-jobs.json](restored-jobs.json)

- Құрылымдық дерек: [restored-review.json](restored-review.json)

- Құрылымдық дерек: [restored-run.json](restored-run.json)

- Құрылымдық дерек: [ruleset-required-test.json](ruleset-required-test.json)

- Құрылымдық дерек: [runner-current.json](runner-current.json)

- Құрылымдық дерек: [runner-download-metadata.json](runner-download-metadata.json)

- Бастапқы журнал: [runner-idle-ui.txt](runner-idle-ui.txt)

- Құрылымдық дерек: [runner-installed.json](runner-installed.json)

- Құрылымдық дерек: [runner-online.json](runner-online.json)

- Каталог: [screenshots](screenshots/)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](../../reports/lab05-ci-report.pdf)
- [Дәлел 2](../../docs/lab05-ci.md)
- [Дәлел 3](checks.json)
- [Дәлел 4](https://github.com/Aruzhaaan-06/devops-labs/pull/17)
- [Дәлел 5](local-build.txt)
- [Дәлел 6](local-restore.txt)
- [Дәлел 7](local-tests.json)
- [Дәлел 8](local-test.txt)
- [Дәлел 9](initial-run.json)
- [Дәлел 10](initial-jobs.json)
- [Дәлел 11](initial-ci-log.txt)
- [Дәлел 12](initial-review.json)
- [Дәлел 13](ruleset-required-test.json)
- [Дәлел 14](failure-run.json)
- [Дәлел 15](failure-jobs.json)
- [Дәлел 16](failure-ci-log.txt)
- [Дәлел 17](failure-pr.json)
- [Дәлел 18](failure-reviews.json)
- [Дәлел 19](failure-check-runs.json)
- [Дәлел 20](failure-blocked-ui.txt)
- [Дәлел 21](screenshots/merge-blocked.jpg)
- [Дәлел 22](restored-run.json)
- [Дәлел 23](restored-jobs.json)
- [Дәлел 24](restored-ci-log.txt)
- [Дәлел 25](restored-review.json)
- [Дәлел 26](screenshots/restored-green.jpg)
- [Дәлел 27](runner-download-metadata.json)
- [Дәлел 28](runner-installed.json)
- [Дәлел 29](runner-current.json)
- [Дәлел 30](runner-idle-ui.txt)
- [Дәлел 31](screenshots/runner-idle.jpg)
- [Дәлел 32](repository-secrets.json)
- [Дәлел 33](fork-approval.json)
- [Дәлел 34](action-pins.json)
- [Дәлел 35](pipeline-pr.json)
- [Дәлел 36](deliverables.json)
- [Дәлел 37](../lab05-cd/README.md)

## Есеп және қабылдау шектері

[Есеп 5.1](../../reports/lab05-ci-report.pdf)

[Нұсқаулық](../../docs/lab05-ci.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
