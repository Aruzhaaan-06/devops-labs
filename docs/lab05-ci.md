# 5-зертханалық жұмыс, 1-бөлім - материал 09

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о**

Мақсаты: PostgreSQL-мен автоматты тестілеу, қызыл test кезінде merge-ті бұғаттау, жергілікті runner және GitHub Actions құпия дерегін дайындау. Методичкадағы 1-5-тармақтар орындалады; PR келесі 10-материалға дейін ашық қалады.

## Workflow құрылымы

| Оқиға | test | image | deploy |
|---|---|---|---|
| main тармағына PR | Ubuntu + PostgreSQL | skipped | skipped |
| main push | Ubuntu + PostgreSQL | test-тен кейін GHCR | image-ден кейін жергілікті Windows |
| v*.*.* тегі | Ubuntu + PostgreSQL | test-тен кейін GHCR | skipped |

Бұл кесте workflow шарттарын сипаттайды. 09-материалда нақты тек PR сценарийі орындалады; образ жариялау және деплой нәтижелері 10-материалда тексеріледі.

Оқу kit файлының жұмыстары мен реті сақталды. GitHub Actions және Docker actions ресми тегтері нақты commit SHA-ларына бекітілді; checkout `persist-credentials: false` арқылы орындалады. .NET шешімі - `DemoApi.slnx`, SDK - 10.0.x. Кэш үшін жаңа lock-файлдар немесе қосымша құралдар енгізілген жоқ.

`test` job уақытша postgres:18-alpine қызметін іске қосады. Health check аяқталған соң `Storage=Postgres` және `ConnectionStrings__Db` тесттерді runner-дің localhost:5432 портына бағыттайды. Оқу demo паролі тек осы уақытша CI дерекқорына қатысты; жергілікті `.env` немесе GitHub secret қолданылмайды.

`image` үшін contents: read және packages: write қажет; қалған workflow contents: read құқығымен жұмыс істейді. `deploy` job contents: read және packages: read пайдаланады. GHCR жүйесіне workflow-ға берілетін GITHUB_TOKEN арқылы кіреді.

## Жергілікті runner және secret

Runner: `C:\actions-runner`, репозиторийден тыс. Ресми Windows x64 архивінің SHA-256 сомасы GitHub API метадеректерімен салыстырылды. Атауы - `devops-labs-windows`, белгілері: self-hosted, Windows, X64, devops-labs. Windows қызметі ретінде орнатылған жоқ; `run.cmd` фондық процесте орындалады. Компьютер немесе процесс тоқтаса, runner Offline болады.

Жергілікті Windows-та PowerShell 7 және Docker Desktop қажет. Deploy үшін API_PORT=8088, DB_PORT=15432 және COMPOSE_SUBNET=10.254.54.0/24 берілді, өйткені runner `.gitignore` ішіндегі жергілікті `.env` файлын алмайды. `DB_PASSWORD` repository secret-іне бұрыннан бар томның нақты құпиясөзі stdin арқылы жіберілді; оның мәні Git-ке, есепке немесе журналға енгізілмейді.

Қоғамдық репозиторийдегі self-hosted runner жергілікті пайдаланушы құқықтарымен код орындайды. Сондықтан PR тесттері GitHub-hosted Ubuntu-да қалады, deploy тек осы репозиторийдің main push оқиғасына арналған, ал сыртқы қатысушылардың workflow-лары үшін `all_external_contributors` мақұлдауы сақталған. Бұл толық sandbox емес; сыртқы PR кодын тексермей мақұлдауға болмайды.

## Қате және қалпына келтіру сценарийі

Тест: `Create_DuplicateName_ReturnsConflict`. Уақытша қате күтілетін код 409 орнына 200 деп қойылады. Нақты API 409 қайтарады, сондықтан test қызыл болуы тиіс. main ruleset GitHub Actions-тің `test` тексеруін талап етеді; Approve бар болса да қызыл test merge-ті тоқтатады. Кейін күтілетін мән 409-ға қайтарылып, жаңа жасыл run алынады. Осы үш кезеңнің нақты сілтемелері мен нәтижелері evidence-де сақталады.

## Пайплайнның келесі бөлігі

Deploy `--wait --wait-timeout 90` арқылы healthy күйін күтеді. Бұл пәрмен сәтсіз болса, job қызыл болып, readiness smoke test орындалмайды. Workflow автоматты rollback жасамайды; ол 10-материалда бөлек тексеріледі.

Негізгі дереккөздер: [GitHub Actions .NET](https://docs.github.com/en/actions/tutorials/build-and-test-code/net), [checkout](https://github.com/actions/checkout), [setup-dotnet](https://github.com/actions/setup-dotnet), [self-hosted runner тәуекелдері](https://docs.github.com/en/actions/reference/security/secure-use).

## 2026 жылғы 23 қазандағы нәтиже

| Кезең | Нақты дәлел |
|---|---|
| Алғашқы жасыл CI | [Run 39922701822](https://github.com/Aruzhaaan-06/devops-labs/actions/runs/39922701822), 4052ddb, 38/38 |
| Әдейі қате тест | [Run 39922922366](https://github.com/Aruzhaaan-06/devops-labs/actions/runs/39922922366), bfd8617, 37/38, test failure |
| Қалпына келген CI | [Run 39923354322](https://github.com/Aruzhaaan-06/devops-labs/actions/runs/39923354322), 07ef056, 38/38 |

Қызыл кезеңде кодты мақұлдау сақталды, required `test` қызыл болды, API `mergeable_state=blocked` қайтарды және Merge pull request түймесі қолжетімсіз болды. Қате күту OK → Conflict жеке коммитпен түзетілді. Үш кезеңде де image/deploy skipped болды.

[24 техникалық тексеру](../evidence/lab05-ci/checks.json) · [Дәлелдер](../evidence/lab05-ci/README.md) · [Қазақша 6 беттік есеп](../reports/lab05-ci-report.pdf) · [Workflow және бес жауап берілген PR #17](https://github.com/Aruzhaaan-06/devops-labs/pull/17).

Жұмыс тармағы - `ci/pipeline`. Есеп пен құжаттар қосылғаннан кейін де GitHub Actions соңғы PR коммитін автоматты тексереді. PDF-тегі тұрақты сілтемелер жасыл-қызыл-жасыл демонстрациясының нақты run-дарына бағытталған; олар кейінгі құжат коммитінің орнына көрсетілмейді.

Есепті қайта құрастыру: Windows-та Arial/Consolas қаріптері мен Python reportlab пакеті болса, репозиторий түбірінен `python scripts/build-lab09-report.py`. Скрипт сақталған evidence арқылы PDF жасайды, CI-ді қайта орындамайды.
