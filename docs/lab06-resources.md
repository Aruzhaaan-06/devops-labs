# 6-зертханалық жұмыс, 2-бөлім - 12-материал

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 2026 жылғы 24 қазан**

6-9-тармақтар, толық 2-8 сценарий кестесі, тапсырудағы бес жауап және қосымша `scripts/diag.ps1` орындалды. 2-5-сценарийлер [11-материалдағы](lab06-failures.md) 23 қазанның нақты дәлелдерінен алынды; олар бүгін қайта орындалған жоқ. Олардың SHA-256 сәйкестігі сақталған.

## Дайындау және орта

Жергілікті main коды: `2dd5a9f`. Docker Desktop Linux containers, PowerShell 7, Docker Compose. Оқу API - `localhost:8088`, контейнер ішінде 8080; 8080 хост портын басқа қызмет қолданады. DB - localhost:15432, том - `devops-labs_pgdata`. `.env` бұрынғы томға сай құпиясөзді қамтиды; ол жарияланбайды.

```powershell
git switch main
git pull --ff-only
$env:API_IMAGE = 'devops-labs-demo-api'
$env:API_TAG = 'lab12-2dd5a9f'
docker compose up -d --build --wait --wait-timeout 120
$api = 'http://localhost:8088'
```

Тәжірибе тек осы Compose жобасына бағытталған. API жад шегі - 256 MiB; RAM+swap жиынтық шегі де 256 MiB, қосымша swap жоқ. OOM-killer өшірілмейді. Басқа deploy осы жобаны қатар өзгертпеуі тиіс.

T1 пәрмен/HTTP журналы, T2 сүзілген `docker events` ағыны және T3 API/DB үшін қайталанған `docker stats --no-stream` қатар орындалды. T3 жаңа контейнерді атауы бойынша табады. Бұл үш көрінетін терминалдың суреті ретінде көрсетілмейді; нақты шығыстары файлдарға сақталған.

## Толық кесте

| Сценарий | T2 | Exit code | Restart | Лог / нәтиже |
|---|---|---|---|---|
| 2: HTTP қатесі | Lifecycle оқиғасы жоқ | Процесс аяқталмады | Жоқ | Error, exception/стек; HTTP500 |
| 3: crash | die1 → start → healthy | 1 | Иә, сол ID | Critical және startup; RestartCount 0→1 |
| 4: restart no | die1, start жоқ | 1 | Жоқ | Critical, Exited(1), RestartCount0 |
| 5: штаттық stop | kill15 → stop → die0 | 0 | Жоқ | Application is shutting down... |
| 6: OOM | oom → die137 → start → healthy | 137 | Иә, сол ID | 3-сұрауда байланыс үзілді; startup; OOM үшін Docker оқиғасы шешуші |
| 7: БД жоқ | API lifecycle оқиғасы жоқ | Процесс аяқталмады | Жоқ | Error/Npgsql; live200, ready503, tasks500; API healthy |
| 8: қате healthcheck | health_status: unhealthy | Процесс аяқталмады | Жоқ | curl exit22/HTTP404 Health.Log ішінде; live/ready200 |

5-сценарийдің хабарламалары нақты сол ретпен жеткізілген, өзгертілмеді. HTTP500 мен healthcheck exit22 API процесінің exit code-ы емес. Сақталған ақау уақыты мен оның оқиғаларын ағымдағы inspect күйімен шатастырмау қажет.

## 6. OOM

```powershell
1..4 | ForEach-Object { curl.exe -s -m 10 -X POST "$api/api/chaos/leak?mb=80"; '' }
docker inspect devops-labs-api-1 --format '{{.State.OOMKilled}} {{.RestartCount}}'
```

Автоматты тексеру OOM расталғанда сұрауларды тоқтатты: алғашқы екі жауап `leakedMb=80` және `160`, үшінші сұрауда байланыс үзілді. Төртінші сұрау жаңа процеске жіберілген жоқ. Тізбек: **oom → die137 → start → healthy**. RestartCount 0→1, контейнер ID бірдей. Кейінгі State: OOMKilled=false, ExitCode=0. Деректер сақталды.

T3: 38 топтама, API бойынша 37 үлгі; өлшенген жад максимумы 78,58%. Үлгілер аралығындағы шын максимум бұдан жоғары болуы мүмкін. Compose қайта жасаған кезде бір EOF/exit1 болды; ол толық сақталған, өлшемдер кейін жалғасты. Restart-тен кейін cgroup `memory.events`/`memory.peak` жаңа күйді көрсетті; олар бұрынғы OOM-ды жоққа шығармайды. Нақты тарих - T2 ағыны.

## 7. БД қолжетімсіз

```powershell
docker compose stop db
curl.exe -s -w ' %{http_code}' "$api/health/live"
curl.exe -s -w ' %{http_code}' "$api/health/ready"
curl.exe -s -o NUL -w '%{http_code}' "$api/api/tasks"
docker compose ps
docker compose start db
```

Нәтиже: **live200 / ready503 / tasks500**; API healthy, ID/StartedAt/RestartCount өзгермеді. Логта Npgsql және Name or service not known. DB start-тен кейін ready200 мен деректер қолжетімділігі API restart-ынсыз қалпына келді.

## 8. Unhealthy

api қызметіне уақытша ғана қосылды:

```yaml
healthcheck:
  test: ["CMD", "curl", "-fsS", "http://localhost:8080/no-such-endpoint"]
  interval: 5s
  retries: 2
```

`docker compose up -d --no-build`, 40 секундтан кейін: unhealthy, Health.Log ішінде HTTP404/exit22. API-дің live/ready жауаптары 200. Сол ID мен StartedAt, RestartCount0; автоматты restart болмады. Бастапқы Compose байттары қайтарылып, `up -d --no-build --wait` арқылы healthy қалпына келді. Файлдың бастапқы/соңғы SHA-256 бірдей; `down` немесе томды жою орындалмады.

## 9. Баяу жауап

Нақты екі өлшем: `/api/tasks` - **0,114133 с**, `/api/chaos/slow?ms=3000` - **3,027295 с**, екеуі де HTTP200. API healthy, restart жоқ. Бұл жүктеме benchmark-і немесе p95/p99 өлшемі емес. Мониторинг latency histogram, percentile және tracing арқылы осындай мәселені көрсетеді; ол келесі бөлімге жатады.

## Бес жауап

1. **Сценарий2 және3:** 2-де бір HTTP500 және Error логы, процесс тірі. 3-де процесс exit1 береді, клиент уақытша қосыла алмауы мүмкін; Docker die/start және RestartCount өсімі бар.
2. **Қолмен stop:** unless-stopped әкімшінің тоқтату ниетін құрметтейді; нақты start қажет, daemon restart-ы оны автоматты көтермейді.
3. **OOMKilled=false:** ағымдағы іске қосылудың күйі. Бұрынғы себеп үшін сақталған oom/die137 оқиғалары, логтар, RestartCount және мониторинг қолданылады; State не cgroup санауышы қайта жазылуы мүмкін.
4. **Live пен ready:** live - процесс, ready - БД сияқты тәуелділік. БД-ны live арқылы restart шартына айналдыру оркестраторда каскадты ақау тудыруы мүмкін. Docker өзі unhealthy үшін restart жасамайды.
5. **ps-те көрінбейтіндер:** жекелеген HTTP500, live тексеруі кезіндегі БД ақауы, баяу жауап; қайта іске қосылып үлгерген процестің бұрынғы crash/OOM себебі. Қате healthcheck unhealthy ретінде көрінеді.

Дәрістегі сегіз өзіндік сұраққа қосымша жауаптар PDF-тің 7-бетінде берілген.

## Қосымша: diag.ps1

```powershell
pwsh -NoProfile -File scripts/diag.ps1 devops-labs-api-1
```

Скрипт тек оқиды: status/health, RestartCount, memory limit, ағымдағы stats, соңғы 20 лог жолы және 15 минуттағы die/oom. Config.Env оқымайды; password/token үлгілері бүркемеленеді. Қалыпты контейнерде exit0, жоқ атауда нақты Docker қатесі мен нөлден өзгеше exit алынды. ID/StartedAt/RestartCount өзгермегені тексерілді. OOM-нан кейін бірден алынған шығыста ағымдағы OOMKilled=false және бұрынғы oom/die137 қатар бар.

Docker тек шектеулі соңғы оқиғаларды ұстайды; 15m параметрі толық 15 минуттық тарихқа кепіл емес. Уақытында экспортталған T2 немесе мониторинг қажет.

## Қайта орындау және артефактілер

- Нақты әсер ететін тәжірибе: `python scripts/verify-lab12.py --output ../lab12-state/new-run --tag lab12-2dd5a9f`. Алдын ала осы тегпен жергілікті образды жинаңыз; output жаңа каталог болуы тиіс. Тек оқу стендінде және қатар deploy жоқ кезде іске қосыңыз.
- Сақталған дәлелдерді офлайн тексеру: `python scripts/check-lab12-evidence.py` - **38 шарт сәтті**.
- Нақты GET тексерулері: `postman collection run postman/lab06-resources.postman_collection.json --env-var baseUrl=http://localhost:8088 --env-var expectedVersion=lab12-2dd5a9f --no-report-events` - **5 сұрау / 11 assertion**, қате0. Кейінгі main deploy үшін expectedVersion мәнін өзгертіңіз. Коллекция OOM/crash жасамайды.
- PDF құрастыру: `python scripts/build-lab12-report.py`, Windows Arial/Consolas және reportlab қажет.
- [8 беттік қазақша есеп](../reports/lab06-resources-report.pdf), [толық дәлелдер](../evidence/lab06-resources/README.md).

Жариялау PR арқылы өтеді. Міндетті CI мен main deploy аяқталған соң SHA/runtime/health және PDF/ZIP хештері `lab12-final-verification.json` ретінде [v1.0.0 релизіне](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0) қосылады. Жаңа архив бөлек `devops-reports-kk-material12.zip` атымен беріледі; ескі релиз файлдары өзгертілмейді. Есептің жергілікті тәжірибе тегі соңғы deploy SHA-ы емес.

Дереккөздер: [Docker resource constraints](https://docs.docker.com/engine/containers/resource_constraints/), [HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck), [Docker events](https://docs.docker.com/reference/cli/docker/system/events/). Бұрынғы қолмен сдача тармақтары мен оқытушы логині туралы шектеулер өз чек-парағында қалады; екі аккаунттың техникалық ревьюі тәуелсіз студенттің ревьюі емес.
