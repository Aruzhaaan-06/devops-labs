# Қолданба ақаулары және қайта іске қосу

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

Бұл нұсқаулық қазақша редакцияланған есептердің толық мазмұнын және қайталауға арналған бастапқы командаларды біріктіреді. Төмендегі өлшемдер мен тексерулер тиісті тарихи кезеңге жатады; аударма оларды қайта орындау болып саналмайды. Код, нақты HTTP жауаптары мен журнал үзінділері бастапқы тілінде сақталған. Қазіргі толықтық пен орындалмаған UI тармақтары [жеке тізімде](REPORT_COMPLETENESS.md) берілген.

## 6.1 — Қолданба ақаулары және қайта іске қосу

### Жұмыстың мақсаты

HTTP қатесі, процесс ақауы, қайта іске қосу саясаты және штаттық тоқтату айырмашылықтарын нақты тәжірибемен анықтау.

### Теориялық мәліметтер

HTTP 500 жауабы процестің аяқталғанын білдірмейді. Контейнердің негізгі процесі аяқталғанда restart саясаты қолданылады. Штаттық stop әрекеті ақаулы аяқталудан бөлек қарастырылады.

ВКТУ · DEVOPS · 11-МАТЕРИАЛ

## 1-бөлім: 1-5-тармақтар, бақылау нүктесі 6

| Мәлімет | Мәні |
|---|---|
| Орындаған | Есімханова Аружан Түсіпханқызы |
| Тобы | 25-ИСТК-2о |
| Университет | ВКТУ |
| Күні | 2026 жылғы 23 қазан |
| Тапсырма | 11-материал, 6-зертханалық жұмыстың 1-бөлімі |

## Мақсаты

HTTP сұрауының қатесін процестің тоқтауынан ажырату; Docker оқиғалары, exit code, JSON логтары және RestartCount арқылы төрт сценарийді дәлелдеу. restart: no мен unless-stopped саясатын салыстырып, штаттық тоқтаудың себебін түсіндіру.

## Нақты орындалған жұмыс

Ағымдағы main коды 89a0e2b негізінде жергілікті Docker бейнесі құрастырылды. HTTP 500, автоматты қайта іске қосу, қайта іске қосуды өшіру және штаттық тоқтату нақты орындалды. Үш параллель CLI арнасы сақталды. 35 дәлел тексеруі сәтті өтті; Postman 4 сұрау мен 10 тексеруді қатесіз орындады.

[Дәлелдер](https://github.com/Aruzhaaan-06/devops-labs/tree/main/evidence/lab06-failures) · [Қайта орындау скрипті](https://github.com/Aruzhaaan-06/devops-labs/tree/main/scripts/verify-lab11.py) · [Орындау тәртібі](https://github.com/Aruzhaaan-06/devops-labs/tree/main/docs/lab06-failures.md)

API мекенжайы - http://localhost:8088, контейнер ішіндегі порт - 8080. Бұл компьютерде 8080 портын басқа қызмет қолданады. 12-материалдың OOM, БД ақауы және unhealthy тәжірибелері осы есепке кірмейді.

## Дайындау және контейнерді қарау

CI бейнесіның орнына әдістеме талабына сай жергілікті main құрастыруы қолданылды: devops-labs-demo-api:lab11-89a0e2b. compose.yaml тек api.restart параметрін уақытша ауыстыру үшін өзгертілді; файлдың бастапқы байттары соңында толық қайтарылды. Атаулы PostgreSQL томы жойылған жоқ.

```text
git switch main
git pull --ff-only
$env:API_IMAGE = "devops-labs-demo-api"
$env:API_TAG = "lab11-89a0e2b"
docker compose up -d --build --wait --wait-timeout 120
$api = "http://localhost:8088"
docker compose ps
docker compose logs api --tail 20
```

| Параметр | Нақты мән |
|---|---|
| API контейнері | devops-labs-api-1; running, healthy |
| Restart policy | unless-stopped |
| Лог драйвері | json-file; max-size=10m; max-file=3 |
| Ресурс шектері | Memory=268435456 байт (256 MiB); swap-пен жалпы шек 256 MiB; CPU=1 |
| ENTRYPOINT | [&quot;dotnet&quot;, &quot;DemoApi.dll&quot;] - exec пішімі |
| Бастапқы RestartCount | 0 |

## T1, T2, T3 бақылау арналары

T1 командалар мен HTTP жауаптарын жазады; T2 docker events ағынын нақты API атымен сүзеді; T3 API мен БД ресурстарын қатар өлшейді. Үш бөлек көрінетін терминал терезесінің суреті жасалмады: үш CLI арнасы параллель процестер мен файлдар арқылы тіркелді. T3 контейнер қайта жасалғанда жаңа ID-ді атауы бойынша табуы үшін --no-stream өлшемін қайталайды.

```text
docker events --filter container=devops-labs-api-1 --filter event=start
  --filter event=kill --filter event=die --filter event=oom
  --filter event=stop --filter event=health_status
docker stats --no-stream devops-labs-api-1 devops-labs-db-1
```

T2 командасы терминалда бір жолмен енгізіледі; exec_* оқиғалары сүзілді. T3: 25 топтама, API бойынша 24 өлшем. Контейнерді қайта жасау кезінде бір stats командасы EOF/exit1 берді; қате сақталды, келесі өлшемдер жалғасты.

## Тапсыру кестесі: сценарийлер 2-5

| Сценарий | T2 оқиғалары | Exit code | Қайта іске қосу | Логтағы дерек |
|---|---|---|---|---|
| 2. Сұрау қатесі | die/start/kill/stop/oom жоқ | Процесс аяқталған жоқ | Жоқ; ID, StartedAt және RestartCount өзгермеді | Error; exception және стек |
| 3. Процестің құлауы | die(exit=1) → start → health_status: healthy | 1; die оқиғасынан алынды | Иә; сол контейнердің RestartCount мәні 0 → 1 | Critical; кейін PostgreSQL және іске қосылу логтары |
| 4. restart: no | die(exit=1); start жоқ | 1; State мәні | Жоқ; 5 с бақылаудан кейін Exited (1), RestartCount=0 | Critical; жаңа іске қосылу логы жоқ |
| 5. Штаттық тоқтату | kill(signal=15) → stop → die(exit=0) | 0; State мәні | Жоқ; қолмен start жасалғанға дейін stopped | Information: Application is shutting down... |

Кесте нақты сақталған оқиғаларға сүйенеді. Штаттық тоқтауда T2 файлы stop оқиғасын die-дан бұрын жеткізді; бұл рет әдейі өзгертілмеді. Негізгі белгілер - SIGTERM=15, exit=0, stop және автоматты start болмауы.

## Exit code пен HTTP коды екі бөлек өлшем

HTTP 500 бір сұраудың нәтижесін білдіреді. Ол контейнер процесінің exit code-ы емес. 2-сценарийде процесс тірі болғандықтан, оның аяқталу коды жоқ. 3-сценарийде қайта іске қосылған контейнердің ағымдағы State.ExitCode мәні 0 болуы мүмкін; бұрынғы 1 коды die оқиғасында сақталады.

## Дәлел сілтемелері

[2: сұрау қатесі](https://github.com/Aruzhaaan-06/devops-labs/blob/main/evidence/lab06-failures/scenario-2-request-error.json) · [3: автоматты қайта іске қосу](https://github.com/Aruzhaaan-06/devops-labs/blob/main/evidence/lab06-failures/scenario-3-auto-restart.json)

[4: no саясаты](https://github.com/Aruzhaaan-06/devops-labs/blob/main/evidence/lab06-failures/scenario-4-no-restart.json) · [5: штаттық тоқтату](https://github.com/Aruzhaaan-06/devops-labs/blob/main/evidence/lab06-failures/scenario-5-graceful-stop.json)

Әр JSON файлында UTC аралығы, контейнердің before/after күйі, HTTP жауабы, лог жазбалары және сол уақыт аралығындағы нақты оқиғалар бар. Бөлек толық T2 ағыны Compose қайта жасаған кездегі қосымша оқиғаларды да сақтайды.

## Сұрау қатесі және процестің авариялық аяқталуы

## 2-сценарий: HTTP 500, процесс тірі

```text
curl.exe -s -w " [%{http_code}]`n" "$api/api/chaos/error"
docker compose logs api --tail 3 --no-log-prefix
```

```text
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.6.1",
  "title": "An error occurred while processing your request.",
  "status": 500,
  "traceId": "00-11be4563175ace3df3d4f1b6cb7cd9e7-7d84eaf95437df08-00"
}
```

Жауап application/problem+json пішімінде, status=500. Ішкі Chaos хабарламасы мен exception stack trace клиентке шыққан жоқ. Олар сервер логында Error деңгейімен сақталған:

```text
LogLevel: Error
Category: Microsoft.AspNetCore.Diagnostics.ExceptionHandlerMiddleware
Exception: System.InvalidOperationException: Chaos: искусственная ошибка
  at DemoApi.Controllers.ChaosController.Error()
```

Толық стек бөлек лог файлында берілген; бұл қысқа үзінді негізгі белгілерін ғана көрсетеді. API контейнерінің ID-і, StartedAt және RestartCount өзгермеді; /health/live 200 қайтарды.

## 3-сценарий: exit 1 және автоматты қайта іске қосу

```text
curl.exe -X POST "$api/api/chaos/crash"
docker inspect devops-labs-api-1 --format "{{.RestartCount}}"
docker compose logs api --since 2m --no-log-prefix
```

POST /api/chaos/crash алдымен 202 қайтарады; шамамен 200 мс кейін қолданба Environment.Exit(1) шақырады. Critical логы жазылып, процесс тоқтайды. unless-stopped саясаты сол контейнерді қайта іске қосады. T2 тізбегі:

```text
die (exit=1) → start → health_status: healthy
```

RestartCount 0-ден 1-ге өсті, контейнер ID-і өзгермеді, StartedAt жаңарды. Readiness 200-ге оралды; бақылау жобасы мен тапсырмасы PostgreSQL-де сақталды. Бұл Compose арқылы контейнерді жаңадан жасаудан бөлек жағдай.

## no саясаты және штаттық тоқтату

## 4-сценарий: автоматты қайта іске қосуды өшіру

compose.yaml ішінде тек api қызметінің restart мәні уақытша "no" деп өзгертілді. DB мен Adminer саясаттары сол қалпында қалды. Compose up --no-build --wait контейнерді жаңа конфигурациямен қайта жасады; содан кейін crash сұрауы жіберілді.

```text
restart: "no"
docker compose up -d --no-build --wait --wait-timeout 90
curl.exe -X POST "$api/api/chaos/crash"
Start-Sleep 5
docker compose ps -a
```

| Өлшем | Нәтиже |
|---|---|
| State.Status | exited |
| State.ExitCode | 1 |
| RestartCount | 0 |
| Оқиға | die (exit=1) |
| Лог | Critical: Chaos: аварийное завершение процесса |

Параметр unless-stopped мәніне қайтарылып, API қайта іске қосылды. Бақылау деректері сақталды. Compose файлының бастапқы және соңғы SHA-256 мәндері бірдей; уақытша no параметрі Git-ке енгізілген жоқ.

## 5-сценарий: SIGTERM арқылы штаттық тоқтату

```text
docker compose stop api
docker compose logs api --tail 5 --no-log-prefix
docker compose start api
```

Оқиғалар: kill (signal=15) → stop → die (exit=0). Лог: Application is shutting down...; State.ExitCode=0. SIGKILL=9 тіркелген жоқ. Контейнер қолмен start жасалғанға дейін 5 секундтық бақылауда stopped күйінде қалды.

docker compose start api командасынан кейін API healthy болды, live/ready 200 қайтарды. Кері қайтару немесе down/up қолданылған жоқ; дәлел ретінде бастапқы ақау логтары мен оқиғалары сақталды.

## Тапсырудағы екі сұраққа жауап

## 2-сценарий 3-сценарийден пайдаланушы және Docker үшін несімен ерекшеленеді?

| Өлшем | 2: сұрау қатесі | 3: процесс тоқтайды |
|---|---|---|
| Пайдаланушыға әсері | Бір сұрау HTTP 500 қайтарады; басқа сұраулар орындала береді | Crash сұрауы 202 алуы мүмкін; қайта іске қосылу кезінде жаңа сұраулар үзіледі не қосылу қатесін алады |
| Docker күйі | Процесс running/healthy; қайта іске қосу жоқ | Процесс exit 1 береді; policy рұқсат етсе, Docker қайта іске қосады |
| Негізгі дәлел | Error және exception stack; lifecycle оқиғасы жоқ | Critical, die(exit=1), start, RestartCount өсімі |

Осылайша, HTTP 500 саны мен контейнердің авариялық аяқталу саны бірдей емес. Тек docker compose ps-ке қарап 2-сценарийді анықтау мүмкін емес: контейнер healthy көрінеді. Сұрау логтары мен HTTP нәтижесі қажет.

## docker compose stop api орындалғанда unless-stopped неге қайта іске қоспайды?

Бұл - әкімшінің әдейі тоқтатуы. unless-stopped саясаты мұндай контейнерді автоматты көтермейді; әйтпесе оны қолмен өшіру мүмкін болмас еді. Контейнерді қайта қосу үшін docker compose start api сияқты нақты команда қажет. Docker daemon қайта іске қосылса да unless-stopped қолмен тоқтатылған контейнерді көтермейді; always саясатының осы жағдайда айырмасы бар.

Процестің өзі қателікпен аяқталғанда қолмен тоқтату белгісі қойылмайды: 3-сценарийде сондықтан автоматты қайта іске қосу болды. 5-сценарийде SIGTERM-ді ASP.NET өңдеп, қолданбаны exit 0 арқылы аяқтады; бұл error crash емес.

## Ресми анықтамалар

[Docker restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/) · [Docker stop және сигналдар](https://docs.docker.com/reference/cli/docker/container/stop/) · [Docker events](https://docs.docker.com/reference/cli/docker/system/events/)

Бұлар механизмді түсіндіретін ресми дереккөздер; кестедегі нақты нәтижелер репозиторийдегі өлшенген JSON/лог файлдарынан алынған.

## Қорытынды және тапсыру құрамы

| Талап | Күйі |
|---|---|
| 1: бастапқы қарау | ps, logs, LogConfig, restart policy, ресурстар және ENTRYPOINT сақталды |
| 2-5: төрт сценарий | HTTP, events, exit code, logs және restart нақты тексерілді |
| Тапсыру кестесі | Осы есептің 3-бетінде бес бағанмен берілген |
| Сұрақтар 1 және 2 | Осы есептің 6-бетінде жауап берілген |
| Дәлел тексерулері | 35 сәтті, қате 0 |
| Postman | 4 сұрау, 10 assertion, қате 0; нақты localhost API |
| Compose және деректер | Бастапқы файл толық қайтарылды; атаулы том, жоба және тапсырма сақталды |

## Docker Desktop арқылы қарау

Docker Desktop ішіндегі Containers → devops-labs → api-1 бөлімінің Logs, Inspect, Exec және Stats қойындыларын пайдаланушы өзі қарап, «вкладки просмотрены» деп растады. Ассистенттің басқару құралы сурет түсіре алмағандықтан, экран суреті берілмеді; бұл тармақ пайдаланушының растауы ретінде белгіленді. Техникалық мәндер CLI арқылы бөлек дәлелденген.

## Тапсыру файлдары

Бұл қазақша PDF, жұмыс нұсқаулығы, қайта орындау скрипті, бөлек Postman коллекциясы және evidence/lab06-failures ішіндегі T1/T2/T3 файлдары жария репозиторийге қосылады. Бастапқы код пен тұрақты Compose конфигурациясына мінез-құлық өзгерісі енгізілген жоқ.

Есеп жарияланатын PR PostgreSQL қатысатын міндетті CI-ден өтеді. Біріктірілген main үшін CI/CD қайта орындалып, соңғы API version мен main SHA сәйкестігі қосымша lab11-final-verification.json файлында беріледі. Есептегі lab11-89a0e2b - жергілікті тәжірибе нұсқасы, соңғы deploy SHA-ы емес.

[Қазақша есептер мен ортақ мұрағат](https://github.com/Aruzhaaan-06/devops-labs/tree/main/reports) · [35 тексеру](https://github.com/Aruzhaaan-06/devops-labs/tree/main/evidence/lab06-failures/checks.json)

## Қауіпсіздік және шектеулер

Тәжірибелер тек localhost-тағы оқу Compose жобасында жасалды. DB_PASSWORD пен GitHub токендері есепке қосылған жоқ. Chaos crash сұрауы негізгі Postman коллекциясына енгізілмеді; оны тек айқын таңдалған тексеру скрипті орындайды. Құпия деректер көрінуі мүмкін толық inspect Config.Env жарияланбады.

Екі GitHub аккаунты бір адамға тиесілі; техникалық Approve тәуелсіз студенттің ревьюі емес. Оқытушы логині берілмеген; бұрынғы жұмыстардың қолмен жөндеу/сурет тармақтары өз чек-парағында қалады. Осы есеп 12-15-материалдардың орындалғанын мәлімдемейді.

## Нәтижелер және шектеулер

Төрт сценарий және 35 тексеру, T1/T2/T3 уақыттары, Postman 4 сұрау/10 тексеру сақталған. Уақытша restart: no конфигурациясы қайтарылған.

Docker Desktop вкладкаларын студент қарағанын хабарлады; бұл әр вкладканың бөлек суреті бар дегенді білдірмейді.

[PDF есебі](../reports/lab06-failures-report.pdf) · [Өңделетін бастапқы файл](../reports/source/lab06-failures-report.json) · [Нақты дәлелдер](../evidence/lab06-failures/README.md)

## Қайта орындауға арналған командалар

Бұл блоктар бастапқы нұсқаулықтан сақталған. Олар автоматты түрде орындалмайды. Томды жою, контейнерді тоқтату немесе ақау туғызу командалары тек тиісті оқшауланған оқу тәжірибесіне арналған. Бар `.env` файлын қайта жазбаңыз; нақты құпиясөзді Git-ке қоспаңыз. Бұрынғы тег/нұсқа атаулары тарихи кезеңді білдіреді.

```powershell
git switch main
git pull --ff-only
$env:API_IMAGE = 'devops-labs-demo-api'
$env:API_TAG = 'lab11-89a0e2b'
docker compose up -d --build --wait --wait-timeout 120
$api = 'http://localhost:8088'
```

```powershell
# T2: бір жолдағы пәрмен
docker events --filter container=devops-labs-api-1 --filter event=start --filter event=kill --filter event=die --filter event=oom --filter event=stop --filter event=health_status

# T3: ресурстардың үздіксіз көрінісі
docker stats devops-labs-api-1 devops-labs-db-1
```

```powershell
docker compose ps
docker compose logs api --tail 20
docker inspect devops-labs-api-1 --format '{{json .HostConfig.LogConfig}}'
docker inspect devops-labs-api-1 --format '{{.HostConfig.RestartPolicy.Name}}'
```

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

## Бастапқы нұсқаулықтағы сілтемелер

- [Дереккөз 1](../evidence/lab06-failures/checks.json)
- [Дереккөз 2](../evidence/lab06-failures/postman-results.json)
- [Дереккөз 3](../reports/lab06-failures-report.pdf)
- [Дереккөз 4](../evidence/lab06-failures/README.md)
- [Дереккөз 5](../scripts/verify-lab11.py)
- [Дереккөз 6](https://docs.docker.com/engine/containers/start-containers-automatically/)
- [Дереккөз 7](https://docs.docker.com/reference/cli/docker/container/stop/)
- [Дереккөз 8](https://docs.docker.com/reference/cli/docker/system/events/)

<!-- Бұрын жарияланған бөлім сілтемелерінің тұрақты идентификаторлары. -->
<a id="6-зертханалық-жұмыс-1-бөлім---11-материал"></a>
<a id="орта-және-дайындау"></a>
<a id="үш-бақылау-арнасы"></a>
<a id="t2-бір-жолдағы-пәрмен"></a>
<a id="t3-ресурстардың-үздіксіз-көрінісі"></a>
<a id="1-бастапқы-қарау"></a>
<a id="2-5-нақты-нәтижелер"></a>
<a id="apirestart-мәнін-уақытша-no-етіп-өзгерткеннен-кейін"></a>
<a id="apirestart-мәнін-unless-stopped-етіп-қайтарғаннан-кейін"></a>
<a id="тапсыру-сұрақтары"></a>
<a id="тексеру-және-артефактілер"></a>
