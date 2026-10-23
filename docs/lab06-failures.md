# 6-зертханалық жұмыс, 1-бөлім - 11-материал

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о**

Мақсат: 1-5-тармақтарды орындап, сұрау қатесі мен процесс ақауын оқиғалар, exit code және логтар арқылы ажырату. Бұл бөлім OOM, БД ақауы немесе unhealthy тәжірибелерін қамтымайды; олар 12-материалға жатады.

## Орта және дайындау

Бастапқы код: main `89a0e2b`. API - `http://localhost:8088`; 8080 портын басқа жергілікті қызмет қолданады. Контейнер аты: `devops-labs-api-1`, БД: `devops-labs-db-1`. Docker Desktop Linux containers, PowerShell 7 және Docker Compose қажет. API PostgreSQL мен `devops-labs_pgdata` атаулы томын пайдаланады.

```powershell
git switch main
git pull --ff-only
$env:API_IMAGE = 'devops-labs-demo-api'
$env:API_TAG = 'lab11-89a0e2b'
docker compose up -d --build --wait --wait-timeout 120
$api = 'http://localhost:8088'
```

Қайта орындағанда тегтің SHA бөлігін сол кездегі main-ге сәйкестендіріңіз. `.env` ішінде бұрынғы томға сай DB_PASSWORD болуы тиіс; оның мәні жарияланбайды. CI runner басқа уақытта осы Compose жобасына deploy жасамауы керек: тәжірибені басқа deploy-мен қатар іске қоспаңыз.

## Үш бақылау арнасы

T1 - осы бөлімнің пәрмендері. T2 және T3-ті бөлек терминалдарда орындауға болады:

```powershell
# T2: бір жолдағы пәрмен
docker events --filter container=devops-labs-api-1 --filter event=start --filter event=kill --filter event=die --filter event=oom --filter event=stop --filter event=health_status

# T3: ресурстардың үздіксіз көрінісі
docker stats devops-labs-api-1 devops-labs-db-1
```

Нақты автоматтандырылған тексеруде үш CLI арнасы параллель орындалды: T1 - пәрмен/HTTP журналы, T2 - үздіксіз events процесі, T3 - қайталанған `docker stats --no-stream`. T3 контейнер Compose арқылы қайта жасалғанда жаңа ID-ді атауы бойынша табады. Бөлек үш көрінетін терминалдың суреті жасалмады. Тіркелген өлшем: 25 топтама, API бойынша 24 үлгі; бұлар толық performance benchmark емес. Контейнерді қайта жасау аралығында бір stats пәрмені exit1/EOF берді; ол жасырылмады, келесі өлшемдер жалғасты. Бұл lifecycle тәжірибелерінің HTTP/event нәтижелеріне әсер етпеді.

## 1. Бастапқы қарау

```powershell
docker compose ps
docker compose logs api --tail 20
docker inspect devops-labs-api-1 --format '{{json .HostConfig.LogConfig}}'
docker inspect devops-labs-api-1 --format '{{.HostConfig.RestartPolicy.Name}}'
```

Нақты мәндер: running/healthy, restart=unless-stopped, json-file log rotation max-size=10m/max-file=3. RAM шегі - 256 MiB, RAM+swap жиынтық шегі де 256 MiB (қосымша swap жоқ), CPU - 1. ENTRYPOINT exec пішімінде: `dotnet DemoApi.dll`.

Docker Desktop → Containers → devops-labs → api-1 ішіндегі Logs, Inspect, Exec, Stats қойындыларын пайдаланушы өзі қарап, «вкладки просмотрены» деп растады. Ассистенттің басқару құралы сурет түсіре алмады; UI тармағы пайдаланушы растауы ретінде белгіленді. CLI дәлелі бөлек сақталған.

## 2-5. Нақты нәтижелер

| Сценарий | T2 оқиғалары | Exit code | Қайта іске қосу | Лог |
|---|---|---|---|---|
| 2: GET /api/chaos/error | Lifecycle оқиғасы жоқ | Қолданылмайды: процесс аяқталмады | Жоқ, ID/StartedAt/RestartCount бірдей | Error, exception және стек; HTTP 500 клиентке ішкі дерексіз |
| 3: POST /api/chaos/crash | die(1) → start → health_status: healthy | 1, die оқиғасынан | Иә; сол ID, RestartCount 0 → 1 | Critical және қайта іске қосылу |
| 4: restart: no + crash | die(1), start жоқ | 1; State.ExitCode=1 | Жоқ; 5 с кейін де Exited(1), RestartCount=0 | Critical |
| 5: docker compose stop api | kill(signal=15) → stop → die(0) | 0 | Жоқ; нақты start пәрменіне дейін stopped | Information, Application is shutting down... |

Соңғы жолдағы оқиға реті T2 ағынында қалай келсе, солай сақталған; stop хабарламасы die-дан бұрын жеткізілді. Оны теориялық ретке сәйкестендіру үшін өзгерткен жоқпыз. Негізгі дәлелдер - SIGTERM, exit0, stop және автоматты start болмауы.

```powershell
curl.exe -s -w ' [%{http_code}]' "$api/api/chaos/error"
curl.exe -X POST "$api/api/chaos/crash"
docker inspect devops-labs-api-1 --format '{{.RestartCount}}'

# api.restart мәнін уақытша "no" етіп өзгерткеннен кейін:
docker compose up -d --no-build --wait --wait-timeout 90
curl.exe -X POST "$api/api/chaos/crash"
Start-Sleep 5
docker compose ps -a

# api.restart мәнін unless-stopped етіп қайтарғаннан кейін:
docker compose up -d --no-build --wait --wait-timeout 90
docker compose stop api
docker compose logs api --tail 5 --no-log-prefix
docker compose start api
```

Файлды қалпына келтіру кезінде пайдаланушы өзгерістерін жоймаймыз: тексеру скрипті алдымен compose.yaml Git айырмасының жоқ екенін тексеріп, оның бастапқы байттарын есте сақтайды және finally ішінде дәл сол байттарды қайта жазады. SHA-256 сәйкес. `down`, томды жою немесе басқа жобалардың контейнерлерін өзгерту қолданылмайды. Соңында API healthy, live/ready=200; бақылау жобасы мен тапсырмасы сақталған.

## Тапсыру сұрақтары

**1. 2-сценарий 3-сценарийден пайдаланушы және Docker үшін несімен ерекшеленеді?** 2-де тек бір сұрау 500 алады; процесс қызмет көрсетуді жалғастырады. Docker running/healthy күйінде, restart жоқ; ақау Error логы мен HTTP нәтижесінде көрінеді. 3-де crash сұрауы 202 алғаннан кейін процесс exit1 береді; қайта іске қосылу аралығында клиент қосыла алмауы мүмкін. Docker die/start жариялап, RestartCount өсіреді. HTTP status - сұраудың нәтижесі, exit code - процестің аяқталуы.

**2. docker compose stop api орындалғанда unless-stopped неге қайта іске қоспайды?** Қолмен тоқтату - әкімшінің нақты ниеті. unless-stopped мұндай контейнерді автоматты көтермейді; қайта қосу үшін start қажет. Docker daemon қайта іске қосылса да stopped контейнер сол күйде қалады. always саясаты daemon қайта қосылғанда оны көтеруі мүмкін. Процестің өзінен болған crash-та қолмен stop белгісі жоқ, сондықтан 3-сценарийде авторестарт болды.

## Тексеру және артефактілер

- [35 дәлел тексеруі](../evidence/lab06-failures/checks.json), қате 0.
- [Нақты Postman: 4 сұрау, 10 assertion](../evidence/lab06-failures/postman-results.json), қате 0; cloud-қа жариялау орындалмады.
- [7 беттік қазақша есеп](../reports/lab06-failures-report.pdf), [толық T1/T2/T3 және JSON дәлелдері](../evidence/lab06-failures/README.md).
- [Қайта орындау скрипті](../scripts/verify-lab11.py) сервиске нақты әсер етеді: crash пен stop жасайды. Оны тек жергілікті оқу стендінде, дайын образбен қолданыңыз: `python scripts/verify-lab11.py --output ../lab11-state/new-run --tag lab11-89a0e2b`. Output каталогы бұрын болмауы тиіс.
- Дәлелді офлайн тексеру: `python scripts/check-lab11-evidence.py`. PDF құрастыру: `python scripts/build-lab11-report.py` (Windows Arial/Consolas, Python reportlab).
- Postman коллекциясы тек GET сұрауларын жібереді: `postman collection run postman/lab06-failures.postman_collection.json --env-var baseUrl=http://localhost:8088 --env-var expectedVersion=lab11-89a0e2b --no-report-events`. Кейінгі CI deploy үшін expectedVersion мәнін жаңа main SHA-ына сәйкестендіріңіз.

Есеп жергілікті тәжірибе нұсқасын тіркейді. Құжаттар біріктірілген кейін main үшін CI/CD орындалады; соңғы SHA, runtime, health, тест және PDF/ZIP хештері `lab11-final-verification.json` ретінде v1.0.0 релизіне қосылады. 10-материалдың тарихи релиз архиві өзгертілмейді; жаңа 10 есептік архив бөлек атпен беріледі.

Ресми түсіндірме: [Docker restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/), [docker stop](https://docs.docker.com/reference/cli/docker/container/stop/), [docker events](https://docs.docker.com/reference/cli/docker/system/events/).

Екі аккаунт бір иеге тиесілі; техникалық ревью тәуелсіз топтас студенттің ревьюі емес. Оқытушы логині және бұрынғы жұмыстардың ашық қолмен тексеру тармақтары өз чек-парағында қалады.
