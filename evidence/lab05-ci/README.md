# 09-материал: CI дәлелдері

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 2026 жылғы 23 қазан**

[Есеп](../../reports/lab05-ci-report.pdf) · [Түсіндірме](../../docs/lab05-ci.md) · [24 тексеру](checks.json) · [PR #17](https://github.com/Aruzhaaan-06/devops-labs/pull/17).

| Тексеру | Сақталған дәлел |
|---|---|
| Жергілікті Release құрастыруы | [0 ескерту, 0 қате](local-build.txt), [restore](local-restore.txt) |
| Жергілікті PostgreSQL тесттері | [38/38 тест тізімі](local-tests.json), [журнал](local-test.txt); бөлек demo_lab09_tests |
| Алғашқы жасыл CI | [Run](initial-run.json), [jobs](initial-jobs.json), [толық лог](initial-ci-log.txt) |
| Approve тест бұзылмай тұрып алынды | [Мақұлдау](initial-review.json) |
| GitHub Actions test міндетті | [main ruleset](ruleset-required-test.json); bypass бос |
| Нақты қызыл test | [Run](failure-run.json), [jobs](failure-jobs.json), [қате жолдары](failure-ci-log.txt) |
| Merge блокталды, Approve сақталды | [PR](failure-pr.json), [ревьюлер](failure-reviews.json), [checks](failure-check-runs.json), [интерфейс мәтіні](failure-blocked-ui.txt), [сурет](screenshots/merge-blocked.jpg) |
| Қалпына келген жасыл CI | [Run](restored-run.json), [jobs](restored-jobs.json), [лог](restored-ci-log.txt), [38/38-ден кейінгі мақұлдау](restored-review.json), [сурет](screenshots/restored-green.jpg) |
| Ресми runner, SHA-256 | [Архив метадеректері](runner-download-metadata.json), [тексерілген орнату](runner-installed.json) |
| Runner Online/Idle | [API күйі](runner-current.json), [интерфейс](runner-idle-ui.txt), [сурет](screenshots/runner-idle.jpg) |
| DB_PASSWORD secret | [Тек атауы мен уақыт метадеректері](repository-secrets.json); мәні GitHub-тан алынбайды |
| Сыртқы workflow мақұлдауы | [all_external_contributors](fork-approval.json) |
| Actions нақты ресми коммиттері | [Алты SHA](action-pins.json) |
| Бес жауап және ашық PR | [PR метадеректері](pipeline-pr.json) |
| PDF/ZIP тексеруі | [SHA-256, беттер, сілтемелер және суреттер](deliverables.json) |

Қате тесттің нақты айырмасы: Expected: OK, Actual: Conflict. Нәтиже: Failed: 1, Passed: 37, Total: 38. Бұл әдейі жасалған оқу кезеңі; тест 07ef056 коммитінде қалпына келтірілді. Қате коммит main-ге кірген жоқ. Merge жасау сұрауы жіберілмеді; сервердің blocked күйі мен қолжетімсіз түйме тексерілді.

Алғашқы және қалпына келген коммиттердің src/tests/workflow файлдары бірдей. Есепті қосатын кейінгі коммит те PR оқиғасымен CI іске қосады. Мұндағы үш run демонстрация кезеңдеріне қатысты; соңғы құжат коммитін тексерді деген тұжырым жоқ.

Runner тіркелгі файлдары мен ZIP орнатқышы Git-ке қосылмайды; токендер оқылып жарияланбайды. Жергілікті пароль тек stdin/процесс ортасы арқылы қолданылды, журналдарда жоқ. TRX файлы жұмыс каталогында сақталған, Git-ке енгізілмеген. CI-дің уақытша postgres қызметіндегі demo паролі жергілікті томның құпиясөзі емес.

Бұл жинақта PR #17-нің 09-материалдағы ашық кезеңі тіркелген. Кейін ол [10-материалда](../lab05-cd/README.md) біріктіріліп, image/GHCR/deploy/smoke/rollback орындалды. Екі аккаунт бір иеге тиесілі; тәуелсіз студенттің ревьюі ретінде көрсетілмейді.
