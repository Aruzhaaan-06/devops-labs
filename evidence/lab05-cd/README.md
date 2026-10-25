# Үздіксіз жеткізу және кері қайтару — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

10-материал. GET / жауабына hello from CI/CD қосылған. Жергілікті InMemory және GitHub PostgreSQL: 39/39; Postman: 38 сұрау/103 тексеру. Нақты test → image → deploy, өзгеріссіз қайталанған deploy, қолмен қайтару және workflow_dispatch арқылы rollback орындалған. Қолмен қайтару: 12,823 с; батырмалық қайтару: 57,696 с, оның ішінде мақұлдау/кезек/бақылау бар. Бақылау деректері сақталып, жаңа нұсқа қайта орнатылған.

local ортасы мақұлдауды талап етеді; tag env арқылы беріліп, Docker командасына дейін тексеріледі. Rollback бар бейнені қайта құрастырмай қолданады. Job summary нақты нұсқаны көрсетеді. v1.0.0 GHCR-ға 1.0.0 жариялаған, тег деплой жасамаған. 34 дәлел тексеруі өтті. Соңғы main/runtime бөлек lab10-final-verification.json файлында; PDF-тегі уақытпен шатастырылмайды. Мақұлдау иенің тапсырмасымен орындалған, тәуелсіз жұптық жұмыс емес.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Бастапқы журнал: [baseline-ci-log.txt](baseline-ci-log.txt)

- Құрылымдық дерек: [baseline-jobs.json](baseline-jobs.json)

- Құрылымдық дерек: [baseline-run.json](baseline-run.json)

- Құрылымдық дерек: [baseline-runtime.json](baseline-runtime.json)

- Бастапқы журнал: [button-ci-log.txt](button-ci-log.txt)

- Құрылымдық дерек: [button-dispatch.json](button-dispatch.json)

- Құрылымдық дерек: [button-jobs.json](button-jobs.json)

- Құрылымдық дерек: [button-pending-approval.json](button-pending-approval.json)

- Құрылымдық дерек: [button-rollback-runtime.json](button-rollback-runtime.json)

- Құрылымдық дерек: [button-rollback-timing.json](button-rollback-timing.json)

- Құрылымдық дерек: [button-run.json](button-run.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Құрылымдық дерек: [environment-local.json](environment-local.json)

- Құрылымдық дерек: [first-merge.json](first-merge.json)

- Құрылымдық дерек: [fork-approval.json](fork-approval.json)

- Құрылымдық дерек: [inmemory-tests.json](inmemory-tests.json)

- Бастапқы журнал: [manual-rollback-log.txt](manual-rollback-log.txt)

- Құрылымдық дерек: [manual-rollback-runtime.json](manual-rollback-runtime.json)

- Құрылымдық дерек: [manual-rollback-timing.json](manual-rollback-timing.json)

- Құрылымдық дерек: [marker.json](marker.json)

- Бастапқы журнал: [message-main-ci-log.txt](message-main-ci-log.txt)

- Құрылымдық дерек: [message-main-jobs.json](message-main-jobs.json)

- Құрылымдық дерек: [message-main-pending-approval.json](message-main-pending-approval.json)

- Құрылымдық дерек: [message-main-run.json](message-main-run.json)

- Құрылымдық дерек: [message-merge.json](message-merge.json)

- Бастапқы журнал: [message-pr-ci-log.txt](message-pr-ci-log.txt)

- Құрылымдық дерек: [message-pr-jobs.json](message-pr-jobs.json)

- Құрылымдық дерек: [message-pr-run.json](message-pr-run.json)

- Құрылымдық дерек: [message-pr.json](message-pr.json)

- Құрылымдық дерек: [message-reviews.json](message-reviews.json)

- Құрылымдық дерек: [message-runtime.json](message-runtime.json)

- Бастапқы журнал: [postman-live.txt](postman-live.txt)

- Құрылымдық дерек: [postman-results.json](postman-results.json)

- Құрылымдық дерек: [registry-manifests.json](registry-manifests.json)

- Бастапқы журнал: [release-ci-log.txt](release-ci-log.txt)

- Құрылымдық дерек: [release-jobs.json](release-jobs.json)

- Құрылымдық дерек: [release-no-deploy-check.json](release-no-deploy-check.json)

- Құрылымдық дерек: [release-run.json](release-run.json)

- Құрылымдық дерек: [release-runtime.json](release-runtime.json)

- Құрылымдық дерек: [release.json](release.json)

- Құрылымдық дерек: [repeat-jobs.json](repeat-jobs.json)

- Құрылымдық дерек: [repeat-run.json](repeat-run.json)

- Құрылымдық дерек: [repeat-runtime.json](repeat-runtime.json)

- Құрылымдық дерек: [report-validation.json](report-validation.json)

- Бастапқы журнал: [restored-main-ci-log.txt](restored-main-ci-log.txt)

- Құрылымдық дерек: [return-after-button-jobs.json](return-after-button-jobs.json)

- Құрылымдық дерек: [return-after-button-run.json](return-after-button-run.json)

- Құрылымдық дерек: [return-after-button-runtime.json](return-after-button-runtime.json)

- Құрылымдық дерек: [return-after-manual-jobs.json](return-after-manual-jobs.json)

- Құрылымдық дерек: [return-after-manual-run.json](return-after-manual-run.json)

- Құрылымдық дерек: [return-after-manual-runtime.json](return-after-manual-runtime.json)

- Құрылымдық дерек: [ruleset.json](ruleset.json)

- Құрылымдық дерек: [runner.json](runner.json)

- Каталог: [screenshots](screenshots/)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](checks.json)
- [Дәлел 2](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0)
- [Дәлел 3](first-merge.json)
- [Дәлел 4](baseline-run.json)
- [Дәлел 5](baseline-jobs.json)
- [Дәлел 6](baseline-ci-log.txt)
- [Дәлел 7](screenshots/baseline-pipeline.jpg)
- [Дәлел 8](baseline-runtime.json)
- [Дәлел 9](message-pr.json)
- [Дәлел 10](message-reviews.json)
- [Дәлел 11](message-merge.json)
- [Дәлел 12](message-pr-run.json)
- [Дәлел 13](message-pr-jobs.json)
- [Дәлел 14](message-pr-ci-log.txt)
- [Дәлел 15](message-main-run.json)
- [Дәлел 16](message-main-jobs.json)
- [Дәлел 17](message-main-ci-log.txt)
- [Дәлел 18](message-runtime.json)
- [Дәлел 19](inmemory-tests.json)
- [Дәлел 20](postman-results.json)
- [Дәлел 21](postman-live.txt)
- [Дәлел 22](repeat-run.json)
- [Дәлел 23](repeat-jobs.json)
- [Дәлел 24](repeat-runtime.json)
- [Дәлел 25](manual-rollback-timing.json)
- [Дәлел 26](manual-rollback-log.txt)
- [Дәлел 27](manual-rollback-runtime.json)
- [Дәлел 28](return-after-manual-run.json)
- [Дәлел 29](return-after-manual-jobs.json)
- [Дәлел 30](restored-main-ci-log.txt)
- [Дәлел 31](return-after-manual-runtime.json)
- [Дәлел 32](button-dispatch.json)
- [Дәлел 33](button-run.json)
- [Дәлел 34](button-jobs.json)
- [Дәлел 35](button-ci-log.txt)
- [Дәлел 36](button-rollback-timing.json)
- [Дәлел 37](button-rollback-runtime.json)
- [Дәлел 38](return-after-button-run.json)
- [Дәлел 39](return-after-button-jobs.json)
- [Дәлел 40](return-after-button-runtime.json)
- [Дәлел 41](environment-local.json)
- [Дәлел 42](message-main-pending-approval.json)
- [Дәлел 43](button-pending-approval.json)
- [Дәлел 44](screenshots/deploy-summary.jpg)
- [Дәлел 45](release.json)
- [Дәлел 46](release-run.json)
- [Дәлел 47](release-jobs.json)
- [Дәлел 48](release-ci-log.txt)
- [Дәлел 49](release-no-deploy-check.json)
- [Дәлел 50](release-runtime.json)
- [Дәлел 51](screenshots/packages-tags.jpg)
- [Дәлел 52](registry-manifests.json)
- [Дәлел 53](marker.json)
- [Дәлел 54](ruleset.json)
- [Дәлел 55](fork-approval.json)
- [Дәлел 56](runner.json)
- [Дәлел 57](report-validation.json)
- [Дәлел 58](deliverables.json)
- [Дәлел 59](../../docs/lab05-cd.md)
- [Дәлел 60](../../reports/lab05-cd-report.pdf)
- [Дәлел 61](../lab05-ci/README.md)

## Есеп және қабылдау шектері

[Есеп 5.2](../../reports/lab05-cd-report.pdf)

[Нұсқаулық](../../docs/lab05-cd.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
