# Docker контейнерін іске қосу және тексеру

Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · Д. Серікбаев атындағы ШҚТУ.

№04 · 4-апта · 2-зертханалық жұмыс, 2-бөлім. Тәжірибе: 22.10.2026. Есеп: 01.11.2026.

## Мақсаты

DemoApi контейнерінің күйін, HTTP жауаптарын, журналдарын және орындалу ортасын тексеріп, Swagger 404/200 жауаптарының себебін түсіндіру.

**Тапсырма:** №04, 4-апта, 2-зертханалық жұмыстың 2-бөлімі.
**Тәжірибе күні:** 22.10.2026.
**Есеп күні:** 01.11.2026.

## Жұмыс ортасы

| Параметр | Мәні |
|---|---|
| Қолданба | DemoApi, ASP.NET Core / .NET 10 |
| Docker Engine | 29.8.0; Linux/amd64 |
| Бейне | devops-labs-demo-api:lab02-1.1 |
| Production контейнері | devops-labs-lab02-api; 127.0.0.1:8089 → 8080 |
| Development контейнері | devops-labs-lab02-swagger; 127.0.0.1:8090 → 8080 |
| Қойма | InMemory |
| Нұсқа | lab02-1.1 |

Есепте 22 қазанда сақталған контейнер, HTTP және тест нәтижелері қолданылды. Тәжірибеге сәйкес код [runtime-checks.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/runtime-checks.json) файлымен және [lab02-docker](https://github.com/Aruzhaaan-06/devops-labs/tree/lab02-docker) тегімен байланысты.

## Соңғы Dockerfile

```text
# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY src/DemoApi/DemoApi.csproj src/DemoApi/
RUN dotnet restore src/DemoApi/DemoApi.csproj
COPY src/ src/
RUN dotnet publish src/DemoApi/DemoApi.csproj -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /app .
ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION
USER $APP_UID
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:8080/health/live || exit 1
ENTRYPOINT ["dotnet", "DemoApi.dll"]
```

build кезеңінде SDK арқылы тәуелділіктер қалпына келтіріліп, Release жинағы жарияланды. runtime кезеңіне /app ішіндегі жарияланған файлдар көшірілді. curl құралы healthcheck сұрауын орындайды. USER $APP_UID қолданбаны root құқықтарынсыз іске қосады.

## .dockerignore

```text
**/bin/
**/obj/
**/TestResults/
.git
.github
.vs
.vscode
.idea
tests/
monitoring/
scripts/
db/
docs/
reports/
evidence/
postman/
*.md
Dockerfile
compose*.yaml
compose*.yml
.env
.env.*
**/.env
**/.env.*
**/*.pfx
**/*.p12
```

bin, obj және TestResults каталогтары, Git тарихы, редактор параметрлері, тесттер, есептер және жергілікті құпия файлдар құрастыру контекстіне кірмейді. Dockerfile мен .dockerignore мазмұны lab02-docker нұсқасымен салыстырылды.

## Контейнерді іске қосу және күйін тексеру

```text
docker run -d --name devops-labs-lab02-api -p 127.0.0.1:8089:8080 -e Storage=InMemory devops-labs-demo-api:lab02-1.1
docker ps --filter name=devops-labs-lab02-api
docker inspect --format "{{.State.Health.Status}}" devops-labs-lab02-api
```

Контейнер іске қосылғаннан кейін healthcheck /health/live мекенжайын тексерді. Docker inspect нәтижесі бойынша процесс жұмыс істеп тұрды, Health.Status мәні healthy болды. Нақты күй [health-production.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/health-production.json) файлында сақталған.

```text
{
  "Status": "running",
  "Running": true,
  "Health": {
    "Status": "healthy",
    "FailingStreak": 0,
    "Log": [
      {
        "ExitCode": 0,
        "Output": "Healthy"
      }
    ]
  }
}
```

Healthcheck аралығы - 10 секунд, timeout - 3 секунд, бастапқы күту кезеңі - 15 секунд, қайталау саны - 3. Хосттағы 8089 порты контейнердің 8080 портына бағытталған.

## GET / және health маршруттары

```text
curl.exe -i http://localhost:8089/
curl.exe -i http://localhost:8089/health/live
curl.exe -i http://localhost:8089/health/ready
```

```text
GET / → HTTP 200
{
  "service": "DemoApi",
  "version": "lab02-1.1",
  "host": "e7ee83006c4d"
}
```

version өрісі құрастыру кезінде берілген lab02-1.1 мәнін көрсетті. host өрісіндегі e7ee83006c4d - контейнердің hostname мәні; ол Windows компьютерінің атауы емес.

| Сұрау | HTTP коды | Жауап |
|---|---|---|
| GET / | 200 | service=DemoApi; version=lab02-1.1 |
| GET /health/live | 200 | Healthy |
| GET /health/ready | 200 | Healthy |

## Logs: қолданба журналы

```text
docker logs devops-labs-lab02-api
```

Журналдан InMemory қоймасы, контейнер ішіндегі 8080 порты, Production ортасы және /app жұмыс каталогы анықталды. Төменде [api-logs.txt](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/api-logs.txt) файлындағы алғашқы бес JSON жазбасының Message өрістері берілген.

```text
Хранилище: в памяти
Now listening on: http://[::]:8080
Application started. Press Ctrl+C to shut down.
Hosting environment: Production
Content root path: /app
```

Контейнердегі стандартты шығыс Docker журналына жиналады. Docker Desktop ішіндегі Logs вкладкасы осы ағынды көрсетуге арналған. Бұл есепте сақталған docker logs шығысы пайдаланылды.

## Exec: контейнер ішіндегі тексерулер

```text
docker exec devops-labs-lab02-api id
docker exec devops-labs-lab02-api dotnet --list-sdks
docker exec devops-labs-lab02-api find /app -type f
```

```text
uid=1654(app) gid=1654(app) groups=1654(app)
```

| Тексеру | Нақты нәтиже |
|---|---|
| id | uid=1654(app); процесс root емес |
| dotnet --list-sdks | Бос шығыс: соңғы бейнеде SDK жоқ |
| find /app -type f | Жарияланған файлдар бар; .cs, .csproj және .slnx жоқ |
| Кіру нүктесі | dotnet DemoApi.dll |

Exec тексерулері контейнердің орындалу ортасын көрсетті. SDK тек build кезеңінде қалды. /app ішіндегі файлдардың толық тізімі [runtime-files.txt](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/runtime-files.txt) файлында, UID мен SDK тексерулері [runtime-checks.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/runtime-checks.json) файлында сақталған.

## Контейнер қайта іске қосылғанда деректердің өзгеруі

InMemory қоймасында «Lab02 restart evidence» жобасы құрылды. Одан кейін сол контейнер docker stop және docker start арқылы қайта іске қосылды. Контейнердің өзі сақталғанымен, қолданба процесінің жедел жады қайта құрылды.

```text
docker stop devops-labs-lab02-api
docker start devops-labs-lab02-api
curl.exe http://localhost:8089/api/projects
```

| Кезең | HTTP коды | Жобалар саны |
|---|---|---|
| Қайта іске қосуға дейін | 200 | 1 |
| Қайта іске қосқаннан кейін | 200 | 0 |

Нақты жауаптар [restart-before.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/restart-before.json) және [restart-after.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/restart-after.json) файлдарында сақталған. InMemory деректері контейнердің файлдық жүйесінде емес, процесс жадында болғандықтан жоғалды. Тұрақты сақтау үшін дерекқор мен оның деректер томы қажет.

## Swagger: Production ортасындағы 404 және Development ортасындағы 200

Алғашқы контейнерде ASPNETCORE_ENVIRONMENT айнымалысы берілмегендіктен, Production ортасы қолданылды. Program.cs ішінде OpenAPI және Swagger тек app.Environment.IsDevelopment() шарты орындалғанда тіркеледі. Сондықтан Production контейнеріндегі Swagger сұрауы 404 қайтарды.

```text
GET http://localhost:8089/swagger/index.html
HTTP 404
Body: ""
```

Сол devops-labs-demo-api:lab02-1.1 бейнесінен Development ортасымен екінші контейнер іске қосылды. Chaos__Enabled=false параметрі оқу ақауларын өшірді. Бейне қайта құрастырылған жоқ.

```text
docker run -d --name devops-labs-lab02-swagger -p 127.0.0.1:8090:8080 -e Storage=InMemory -e ASPNETCORE_ENVIRONMENT=Development -e Chaos__Enabled=false devops-labs-demo-api:lab02-1.1
curl.exe -i http://localhost:8090/swagger/index.html
```

| Орта | Мекенжай | HTTP коды |
|---|---|---|
| Production | localhost:8089/swagger/index.html | 404 |
| Development | localhost:8090/swagger/index.html | 200 |
| Development | localhost:8090/openapi/v1.json | 200 |

404 жауабы бұл жағдайда сервистің тоқтағанын білдірмейді: GET / және health маршруттары 200 қайтарды. Айырмашылық - Swagger маршрутының ортаға байланысты тіркелуі. Екі жауап [swagger-production.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/swagger-production.json) және [swagger-development.json](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/swagger-development.json) файлдарында берілген.

## Сақталған тест нәтижелері

| Тексеру | Нәтиже |
|---|---|
| Контейнер мен API бойынша тексерулер | 14/14 сәтті |
| HTTP сценарийлері | 26 сұрау: 23 сценарий және 3 тазалау сұрауы |
| Postman CLI | 24 сұрау; 73 тексеру; қате 0 |
| .NET Release / InMemory | 28/28; failed 0; skipped 0 |

Бұл нәтижелер 22.10.2026 күнгі lab02-1.1 нұсқасына жатады. Postman шығысы [postman-console.txt](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/postman-console.txt) файлында, .NET тест нәтижелері [lab02-regression.trx](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/tests/lab02-regression.trx) файлында сақталған.

## Жұмыс материалдары

[Dockerfile](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/Dockerfile); [.dockerignore](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/.dockerignore); [Program.cs](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/src/DemoApi/Program.cs); [контейнер тәжірибесінің журналдары](https://github.com/Aruzhaaan-06/devops-labs/blob/065a222e2f384df496ad8294cd843325ec20b963/evidence/lab02/README.md).

## Талдау

Қызметтің жұмыс істеуі мен Swagger қолжетімділігі бөлек тексерілді. Production ортасында Swagger тіркелмегендіктен 404 қайтты; Development ортасы сол бейнеде 200 берді. InMemory деректері процесс жадында сақталғандықтан қайта іске қосылғанда жоғалды.

## Қорытынды

DemoApi Docker контейнерінде жұмыс істеді. Healthcheck, журналдар және контейнер ішіндегі командалар арқылы іске қосу ортасы тексерілді. 404/200 жауаптарының конфигурацияға тәуелділігі анықталды.

[PDF есебі](../reports/lab02-part2-report.pdf) · [Бастапқы материалдар](../evidence/lab02/README.md).
