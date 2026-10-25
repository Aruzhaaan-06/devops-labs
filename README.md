# DevOps зертханалық жұмыстары

## Жоба туралы

DemoApi - ASP.NET Core негізіндегі жобалар мен тапсырмаларға арналған оқу API-і. Репозиторий HTTP сұрауларынан бастап контейнерлеу, PostgreSQL, GitHub Actions, мониторинг және инцидентті қалпына келтіруге дейінгі нақты жұмыстарды біріктіреді.

Репозиторийде бастапқы код, іске қосу конфигурациялары, тесттер, жұмыс нәтижелері және қазақ тіліндегі есептер берілген.

## Пән туралы ақпарат

| Мәлімет | Мәні |
|---|---|
| Университет | Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті (ШҚТУ / ВКТУ) |
| Пән | DevOps құралдары |
| Оқу кезеңі | 2025-2026 |
| Нақты тәжірибелер | 2026 жылғы 22-25 қазан; журналдардың бастапқы уақыттары сақталған |
| Есеп тілі | Қазақ тілі; код, командалар, API жауаптары мен шынайы интерфейс мәтіні бастапқы тілінде |

## Қолданылған технологиялар

| Құрал | Қолданылуы |
|---|---|
| .NET 10, ASP.NET Core, C# | REST API, контроллерлер және сервистер |
| PostgreSQL 18, Npgsql | Тұрақты деректер мен SQL репозиторийлері |
| Docker, Compose | Linux контейнерлері, желі, атаулы томдар және іске қосу |
| Git, GitHub Actions, GHCR | PR, міндетті CI, бейне жариялау және жергілікті орналастыру |
| xUnit, WebApplicationFactory, Postman | Юнит, интеграциялық және HTTP тексерулер |
| Prometheus, Grafana, cAdvisor, Dozzle | Метрикалар, алерттер, ресурстар және журналдар |
| Python, ReportLab, pypdf, pdfplumber | Есептерді қайта құру және техникалық PDF тексеруі |

## Зертханалық жұмыстар

**14 зертханалық есеп, 8 негізгі зертханалық жұмыс және қорытынды есеп.** 04-материалдың шарты жоқ; ол орындалған жұмыс ретінде қосылмаған. Бастапқы 1.1/1.3 файлдары дәрістерді, 1.2/1.4 файлдары практиканы қамтиды; олардың нәтижесі бірінші жұмыстың екі есебінде жинақталған.

| № / бөлім | Зертханалық жұмыстың тақырыбы | Есеп | Бастапқы код |
|---|---|---|---|
| 1.1 | Тапсырмалар сервисінің API интерфейсі | [PDF · 13 бет](reports/lab01-part1-report.pdf) | [Есеп JSON](reports/source/lab01-part1-report.json) · [Код және кезең](docs/lab01.md) |
| 1.2 | Сұрауды талдау және жоба статистикасы | [PDF · 19 бет](reports/lab01-part2-report.pdf) | [Есеп JSON](reports/source/lab01-part2-report.json) · [Код және кезең](docs/lab01.md) |
| 2.1 | Dockerfile және құрастыру кэші | [PDF · 12 бет](reports/lab02-part1-report.pdf) | [Есеп JSON](reports/source/lab02-part1-report.json) · [Код және кезең](docs/lab02.md) |
| 3.1-3.2 | Сервиске арналған PostgreSQL | [PDF · 15 бет](reports/lab03-postgres-report.pdf) | [Есеп JSON](reports/source/lab03-postgres-report.json) · [Код және кезең](docs/lab03-postgres.md) |
| 3.3 | Docker Compose және деректердің өмірлік циклі | [PDF · 14 бет](reports/lab03-compose-report.pdf) | [Есеп JSON](reports/source/lab03-compose-report.json) · [Код және кезең](docs/lab03-compose.md) |
| 4.1 | Git және GitHub-та бірлескен жұмыс | [PDF · 15 бет](reports/lab04-git-report.pdf) | [Есеп JSON](reports/source/lab04-git-report.json) · [Код және кезең](docs/lab04-git.md) |
| 4.2 | GitHub ережелері және шығарылым | [PDF · 17 бет](reports/lab04-release-report.pdf) | [Есеп JSON](reports/source/lab04-release-report.json) · [Код және кезең](docs/lab04-release.md) |
| 5.1 | GitHub Actions арқылы үздіксіз интеграция | [PDF · 14 бет](reports/lab05-ci-report.pdf) | [Есеп JSON](reports/source/lab05-ci-report.json) · [Код және кезең](docs/lab05-ci.md) |
| 5.2 | Үздіксіз жеткізу және кері қайтару | [PDF · 14 бет](reports/lab05-cd-report.pdf) | [Есеп JSON](reports/source/lab05-cd-report.json) · [Код және кезең](docs/lab05-cd.md) |
| 6.1 | Қолданба ақаулары және қайта іске қосу | [PDF · 13 бет](reports/lab06-failures-report.pdf) | [Есеп JSON](reports/source/lab06-failures-report.json) · [Код және кезең](docs/lab06-failures.md) |
| 6.2 | Ресурстар, тәуелділік және диагностика | [PDF · 15 бет](reports/lab06-resources-report.pdf) | [Есеп JSON](reports/source/lab06-resources-report.json) · [Код және кезең](docs/lab06-resources.md) |
| 7.1 | Метрикалар және PromQL | [PDF · 17 бет](reports/lab07-metrics-report.pdf) | [Есеп JSON](reports/source/lab07-metrics-report.json) · [Код және кезең](docs/lab07-metrics.md) |
| 7.2 | Grafana панельдері және алерттер | [PDF · 17 бет](reports/lab07-alerts-report.pdf) | [Есеп JSON](reports/source/lab07-alerts-report.json) · [Код және кезең](docs/lab07-alerts.md) |
| 8 | Инцидентті анықтау және қалпына келтіру | [PDF · 17 бет](reports/lab08-incident-report.pdf) | [Есеп JSON](reports/source/lab08-incident-report.json) · [Код және кезең](docs/lab08-incident.md) |

[Қорытынды есеп](reports/submission-summary-kk.pdf) · [Барлық есептер](reports/README.md) · [Бірыңғай архив](reports/devops-reports-kk.zip) · [Файлдарды тексеру](docs/REPORT_AUDIT.md).

## Репозиторий құрылымы

```text
src/DemoApi/       API, сервис, модельдер және InMemory/PostgreSQL қоймалары
tests/            Юнит және интеграциялық тестілер
postman/          Негізгі және тақырыптық HTTP коллекциялар
db/               Бастапқы схема мен оқу деректері
monitoring/       Prometheus, Grafana, cAdvisor және Dozzle
.github/          CI/CD, PR үлгісі, Dependabot және CODEOWNERS
docs/             Жұмыс нұсқаулықтары, рәсімдеу негізі және аудит
evidence/         Нақты журналдар, JSON, өлшемдер және шынайы суреттер
reports/          Соңғы PDF есептер мен архив
  source/         Өңделетін JSON мәтіні және каталог
  assets/         Өзгертілмеген түпнұсқа суреттер
scripts/          Диагностика, тексерулер және есеп жинақтаушысы
```

Алдыңғы нұсқалар Git тарихында және [v1.1.0 релизінде](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.1.0) сақталған.

## Жобаны іске қосу

### InMemory режимі

.NET 10 SDK қажет. 8088 порты бос болуы тиіс; осы порттағы Compose API мен жергілікті процесті қатар іске қоспаңыз.

```powershell
git clone https://github.com/Aruzhaaan-06/devops-labs.git
cd devops-labs
dotnet restore DemoApi.slnx
$env:Storage = 'InMemory'
dotnet run --project src/DemoApi/DemoApi.csproj --launch-profile http
```

[Swagger](http://localhost:8088/swagger) тек Development ортасында ашылады. [Postman коллекциясының](postman/demo-api.postman_collection.json) `baseUrl` мәні - `http://localhost:8088`. InMemory деректері процесс аяқталғанға дейін ғана сақталады. Visual Studio 2026 үшін `DemoApi.slnx`, DemoApi жобасы және `http` профилі қолданылады.

### API және PostgreSQL арқылы Compose

Docker Desktop Linux containers және Docker Compose v2 қажет.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# .env ішінде өз DB_PASSWORD мәнін орнатыңыз; бар файлды қайта жазбаңыз.
docker compose config --quiet
docker compose up -d --build --wait
curl.exe http://localhost:8088/health/ready
```

API - localhost:8088; PostgreSQL - localhost:15432. `.env` Git-тен алынып тасталған. Бос емес томда тек орта айнымалысын өзгерту дерекқор пайдаланушысының құпиясөзін өзгертпейді. Қалыпты тоқтату `docker compose stop` арқылы деректерді сақтайды. Толық `docker compose config` шығысын жарияламаңыз: құпия мәндер көрінуі мүмкін.

Мониторингті бөлек іске қосу:

```powershell
docker compose -f monitoring/compose.yaml up -d
```

Prometheus - localhost:9090, Grafana - localhost:3000, cAdvisor - localhost:8081, Dozzle - localhost:8888. Интерфейстер 127.0.0.1-ге байланған. Оқу ақауларын іске қосатын скрипттер әдейі crash/OOM/stop жасайды; олар әдеттегі тексеруге автоматты қосылмайды. [Орналастыру және кері қайтару](docs/lab05-cd.md), [мониторинг](docs/lab07-metrics.md), [инцидент нұсқаулығы](docs/lab08-incident.md).

### Құрастыру және тестілеу

```powershell
dotnet build DemoApi.slnx -c Release
$env:Storage = 'InMemory'
dotnet test DemoApi.slnx -c Release --no-build
Remove-Item Env:Storage
```

SQL тестілері жеке тест дерекқорын қажет етеді. `Storage=Postgres` және `ConnectionStrings__Db` мәнін жергілікті ортада қауіпсіз беріңіз; негізгі оқу дерекқорын тестке көрсетпеңіз. [PostgreSQL нұсқаулығы](docs/lab03-postgres.md). GitHub CI уақытша PostgreSQL сервисін қолданады; main үшін `test` мәртебесі міндетті.

## Нәтижелер

- Бірінші жұмыстың міндетті тарихи нұсқасы - **24/24**, қосымша ережесі бар нұсқасы - **28/28**. Қазіргі кодта **40 тест** бар; олардың іске қосу деректері [сақталған дәлелдерде](evidence/submission-readiness/README.md) және CI журналдарында берілген. Бұл сандар тест қамтуының пайызы емес.
- CI/CD, екі rollback, PostgreSQL деректерінің сақталуы және нақты GitHub Revert PR орындалған. [15-материал инциденті](docs/lab08-incident.md): анықтау 204,726 с, қалпына келтіру 100,149 с; өлшеу шекарасы есепте түсіндірілген.
- [13-материалда](evidence/lab07-metrics/README.md) мониторингтің 13 суреті, PromQL сұраулары және жүктеме нәтижелері берілген.

## Есептерді қарау және редакциялау

[Есеп каталогы](reports/README.md), [рәсімдеу негізі](docs/FORMATTING_STANDARDS.md), [аудит](docs/REPORT_AUDIT.md), [жұмыс мәртебесі](docs/REPORT_COMPLETENESS.md), [өзгерістер](docs/CHANGELOG.md).

```powershell
python -m pip install -r scripts/requirements-reports.txt
python scripts/build_reports.py
python scripts/check_reports.py
```

Өңделетін түпнұсқалар - `reports/source/*.json`. [Толық редакциялау нұсқаулығы](reports/source/README.md). Қаріптер репозиторийге таратылмайды; Times New Roman/Consolas каталогы `--font-dir` арқылы беріледі. Құрастырудан кейін беттердің орналасуын, кестелер мен суреттерді қарап шығу керек.

## Пайдаланылған дереккөздер

[ШҚТУ](https://www.ektu.kz/?lang=kz) · [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) · [PostgreSQL 18](https://www.postgresql.org/docs/18/index.html) · [GitHub Actions .NET](https://docs.github.com/en/actions/tutorials/build-and-test-code/net) · [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) · [Grafana экспорт нұсқаулығы](https://grafana.com/docs/grafana/latest/visualizations/dashboards/share-dashboards-panels/). Нормативтік дереккөздер мен тексеру күні [бөлек құжатта](docs/FORMATTING_STANDARDS.md) көрсетілген.

## Автор туралы ақпарат

Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · ШҚТУ / ВКТУ. Репозиторийде DevOps пәні бойынша орындалған жұмыстар жинақталған.
