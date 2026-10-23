# 10-материал: жариялау және кері қайтару дәлелдері

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 2026-10-23**

Міндетті 6-9-тармақтар және үш қосымша тапсырма орындалды. [34 шарт тексерілді](checks.json), қате 0. Бұл жинақ сақталған нақты іске қосуларды сипаттайды; соңғы құжат коммитінің тірі API-мен сәйкестігі [v1.0.0 релизіндегі](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0) `lab10-final-verification.json` файлына жазылады.

| Кезең | Нәтиже және дәлел |
|---|---|
| PR #17 біріктіру | [Squash merge](first-merge.json), main `8511c6c` |
| Бірінші толық пайплайн | [Run 39926367307](baseline-run.json), [jobs](baseline-jobs.json), [толық лог](baseline-ci-log.txt), [шынайы сурет](screenshots/baseline-pipeline.jpg) |
| Бастапқы жауап және health | [sha-8511c6c, message жоқ](baseline-runtime.json); live/ready 200 |
| Жаңа Message және тест | [PR #18](message-pr.json), [ашық көрсетілген техникалық ревью](message-reviews.json), [merge](message-merge.json) |
| PR CI | [Run](message-pr-run.json), [jobs](message-pr-jobs.json), [39/39 PostgreSQL логы](message-pr-ci-log.txt) |
| Жаңа main | [Run 39927177292, attempt 1](message-main-run.json), [jobs](message-main-jobs.json), [толық лог](message-main-ci-log.txt) |
| API жауабы | [sha-349a0b1, hello from CI/CD](message-runtime.json) |
| InMemory | [39/39 нәтижесі мен тест атаулары](inmemory-tests.json) |
| Тірі Postman | [38 сұрау / 103 assertion, exit 0](postman-results.json), [толық шығыс](postman-live.txt) |
| Бір тегке қайталанған deploy | [Attempt 2](repeat-run.json), [jobs](repeat-jobs.json), [бірдей контейнер ID/StartedAt](repeat-runtime.json) |
| Қолмен кері қайтару | [12,823 секунд](manual-rollback-timing.json), [пәрмен шығысы](manual-rollback-log.txt), [ескі жауап және сақталған деректер](manual-rollback-runtime.json) |
| Re-run all jobs арқылы оралу | [Attempt 3](return-after-manual-run.json), [jobs](return-after-manual-jobs.json), [лог](restored-main-ci-log.txt), [ағымдағы жауап](return-after-manual-runtime.json) |
| Батырмамен кері қайтару | [Dispatch](button-dispatch.json), [Run 39927957374](button-run.json), [jobs](button-jobs.json), [лог](button-ci-log.txt), [57,696 секунд](button-rollback-timing.json), [ескі жауап](button-rollback-runtime.json) |
| Батырмадан кейінгі оралу | [Attempt 4](return-after-button-run.json), [jobs](return-after-button-jobs.json), [sha-349a0b1](return-after-button-runtime.json) |
| Environment local | [Required reviewer, protected branches, bypass=false](environment-local.json), [deploy күтті](message-main-pending-approval.json), [rollback күтті](button-pending-approval.json) |
| Job summary | [Тексерілген образ, version және approval суреті](screenshots/deploy-summary.jpg) |
| v1.0.0 | [Release](release.json), [Run 39928705609](release-run.json), [jobs](release-jobs.json), [лог](release-ci-log.txt) |
| Тег deploy жасамады | [Салыстыру](release-no-deploy-check.json), [өзгермеген контейнер](release-runtime.json) |
| Packages | [latest, sha-349a0b1, 1.0.0 суреті](screenshots/packages-tags.jpg), [нақты төрт manifest](registry-manifests.json) |
| Деректердің сақталуы | [Бақылау жобасы мен тапсырмасы](marker.json), барлық runtime JSON-дарда мәндері дәл салыстырылды |
| Қорғаныс сақталды | [Required test және PR approval](ruleset.json), [сыртқы workflow approval](fork-approval.json), [runner күйі](runner.json) |
| PDF және ZIP | [8 бет, 12 сілтеме, суреттердің бастапқы байттары](report-validation.json), [9 есеп / 69 бет және SHA-256](deliverables.json) |

Қолмен өлшеу бірінші Compose пәрменінен ескі GET / жауабын растауға дейін есептелді. Батырмалық өлшеу dispatch сұрауынан басталып, approval, runner кезегі мен бақылау аралығын қамтиды. Екі көрсеткіштің өлшеу шекаралары әртүрлі.

Екі rollback-тан кейін де жаңа нұсқа қалпына келтірілді. Бақылау жобасы мен тапсырмасы барлық сегіз runtime кезеңінде сақталған; `devops-labs_pgdata` томы жойылған жоқ. Тег run-ының алдында және соңында API контейнер ID, StartedAt, image ID және жауап бірдей болды.

`sha-*` атауы код коммитін көрсетеді; registry тегі өзгермейтін digest-пен тең емес. Manifest JSON-дары сол өлшеу сәтіндегі registry артефактілерін, runtime JSON-дары нақты іске қосылған image ID-ді тіркейді.

Жергілікті DB_PASSWORD, GitHub токендері және runner credential файлдары жарияланбайды. Толық CI логтарындағы уақытша PostgreSQL `demo` мәні оқу CI қызметіне арналған, жергілікті томның құпиясөзі емес. Postman cloud-қа жариялау орындалмады; CLI-дің соңғы тіркелгі ескертуі жергілікті 38/103 нәтижесін өзгертпейді.

Екі GitHub аккаунты бір иеге тиесілі. Code owner ревьюі - техникалық сценарий; тәуелсіз топтас студенттің ревьюі ретінде көрсетілмейді. local approval иенің тапсырмасымен ассистент арқылы орындалды, API күтуі мен GitHub жазбасы сақталды. Оқытушы логині берілмеген.

Қайта тексеру: `python scripts/check-lab10-evidence.py`. PDF: `python scripts/build-lab10-report.py` (Windows Arial/Consolas, reportlab). Бұл скрипттер желіге сұрау жібермейді және контейнерлерді өзгертпейді.

[Орындау тәртібі және сегіз жауап](../../docs/lab05-cd.md) · [Қазақша PDF](../../reports/lab05-cd-report.pdf) · [09-материалдың тарихи қызыл/жасыл CI дәлелдері](../lab05-ci/README.md)
