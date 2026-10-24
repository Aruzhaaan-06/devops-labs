# DevOps Labs — DemoApi: проекты и задачи

Учебные работы по DevOps на базе DemoApi — REST API на ASP.NET Core / .NET 10. Проекты, задачи, переходы статусов и статистика; хранение в памяти или PostgreSQL.

**Университет:** ВКТУ

**Студент:** Есімханова Аружан Түсіпханқызы · **Группа:** 25-ИСТК-2о

[Работы и статус](docs/README.md) · [Отчеты и исходники](reports/README.md) · [Результаты проверок](evidence/lab01/README.md) · [Разбор лабораторной 1](docs/lab01.md)

Все одиннадцать отчетов оформлены на казахском языке: [PDF и общий архив](reports/README.md). В отчетах указаны ВКТУ и полное ФИО.

## Выполненные работы

| Работа | Результат | Отчет |
|---|---|---|
| Лабораторная 1, часть 1 | Запуск InMemory, запросы, ошибки API, потеря данных после перезапуска | [PDF · 8 страниц](reports/lab01-part1-report.pdf) |
| Лабораторная 1, часть 2 | Статистика проекта, тесты, ответы по коду; дополнительно — проверка срока новой задачи | [PDF · 12 страниц](reports/lab01-part2-report.pdf) |
| Лабораторная 2, часть 1 · материал 03 | Multi-stage Dockerfile, кэш restore и проверка Linux-контейнера; нужен скриншот WSL 2 | [PDF · 6 страниц](reports/lab02-part1-report.pdf) |
| Лабораторная 3, части 1–2 · материал 05 | PostgreSQL, сохранение данных, две ошибки подключения и SQL-тесты; нужны скриншоты консоли Visual Studio и Test Explorer | [PDF · 7 страниц](reports/lab03-postgres-report.pdf) |
| Лабораторная 3, часть 3 · материал 06 | Docker Compose, 3 → 3 → 2, отказ БД, Windows-разработка и Adminer | [PDF · 7 страниц](reports/lab03-compose-report.pdf) |
| Лабораторная 4, часть 1 · материал 07 | Защита main, Board, ревью README и конфликт; два аккаунта одного владельца, преподаватель пока не добавлен | [PDF · 7 страниц](reports/lab04-git-report.pdf) |
| Лабораторная 4, часть 2 · материал 08 | Переименование проекта, PR template, Dependabot, CODEOWNERS и [релиз v0.1.0](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v0.1.0) | [PDF · 8 страниц](reports/lab04-release-report.pdf) |
| Лабораторная 5, часть 1 · материал 09 | GitHub Actions: 38/38, намеренный красный test с блокировкой merge, восстановление 38/38; runner Idle и DB_PASSWORD готовы | [PDF · 6 страниц](reports/lab05-ci-report.pdf) |
| Лабораторная 5, часть 2 · материал 10 | GHCR, deploy, Message, два отката, Environment local, Job summary и [v1.0.0](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0) | [PDF · 8 страниц](reports/lab05-cd-report.pdf) |
| Лабораторная 6, часть 1 · материал 11 | Четыре сценария сбоев: HTTP500, crash, restart no и штатная остановка; events/exit/logs, 35 проверок | [PDF · 7 страниц](reports/lab06-failures-report.pdf) |
| Лабораторная 6, часть 2 · материал 12 | OOM137, DB ready503, unhealthy без restart, slow3000ms и diag.ps1; полная таблица2–8, пять ответов | [PDF · 8 страниц](reports/lab06-resources-report.pdf) |

Код и проверки первой лабораторной подготовлены. Для полного комплекта сдачи остаются скриншоты коллекции Postman и Test Explorer, а также ручная пошаговая отладка с Locals и Call Stack. Подробности — в [чек-листе сдачи](docs/lab01.md#что-приложить-к-двум-отчётам). SQL-реализация проверена на настоящей PostgreSQL в [лабораторной 3](docs/lab03-postgres.md).

Материал 08 проверен 23 октября 2026 года: **38/38 тестов в InMemory и 38/38 в PostgreSQL**, полная коллекция Postman — **37 запросов и 99 проверок**. [Описание API и выполнения](docs/lab04-release.md) · [Доказательства](evidence/lab04-release/README.md).

Материал 09: **настоящий CI GitHub Actions с PostgreSQL, 38/38**. Обязательный `test` заблокировал merge при намеренной ошибке; после восстановления CI снова зеленый. PR #17 объединен при выполнении материала 10. [Подробности](docs/lab05-ci.md) · [Доказательства](evidence/lab05-ci/README.md).

Материал 10: **39/39 тестов, Postman 38/103**, полный `test → image → deploy`, GET / с `hello from CI/CD`, идемпотентный повторный deploy, ручной откат **12,823 с** и кнопочный откат **57,696 с** с сохранением контрольных данных. Выпущен **v1.0.0**; тег публикует образ без deploy. Настроены `local` с approval и Job summary. [Выполнение](docs/lab05-cd.md) · [34 проверки и доказательства](evidence/lab05-cd/README.md). Финальная сверка последнего main с живым API размещается в релизе как `lab10-final-verification.json`.

Материал 11: **четыре сценария и 35 проверок**, Postman **4 запроса / 10 assertions**. Временный `restart: no` отменен, исходный Compose восстановлен, API healthy и данные сохранены. Вкладки Docker Desktop просмотрены пользователем. [Выполнение и ответы](docs/lab06-failures.md) · [Доказательства](evidence/lab06-failures/README.md).

Материал 12: **OOM → die137 → start**, БД недоступна при live200/ready503/tasks500, unhealthy без restart, slow HTTP200 за 3,027 с. **38 проверок**, Postman **5/11**. Добавлен read-only `scripts/diag.ps1`, Compose восстановлен, данные сохранены. [Выполнение](docs/lab06-resources.md) · [Доказательства](evidence/lab06-resources/README.md).

Сохраненные результаты предыдущих этапов от 22 октября 2026 года:

| Проверка | Результат |
|---|---|
| Обязательный этап | 24/24 теста; [тег lab01-required-24](https://github.com/Aruzhaaan-06/devops-labs/tree/lab01-required-24) |
| Версия с дополнительным правилом | 28/28 тестов: 7 юнит и 21 интеграционный |
| Итоговая коллекция Postman CLI | 24 запроса, 73 проверки, без ошибок |
| Перезапуск InMemory | 4 проекта до остановки, 0 после запуска |
| PostgreSQL, лабораторная 3 | 24/24 обязательных и 28/28 полных тестов; данные пережили перезапуски |

Все журналы, сводки и два настоящих скриншота Swagger доступны в [каталоге результатов](evidence/lab01/README.md). Это результаты записанных запусков; текущий код можно проверить командами ниже.

## Быстрый запуск

Нужен .NET 10 SDK. Для отладки и Test Explorer — Visual Studio 2026 с компонентом «ASP.NET и разработка веб-приложений». В текущем режиме отдельная база данных не нужна.

```powershell
git clone https://github.com/Aruzhaaan-06/devops-labs.git
cd devops-labs
dotnet restore DemoApi.slnx
dotnet run --project src/DemoApi/DemoApi.csproj --launch-profile http
```

Откройте [Swagger](http://localhost:8088/swagger). В Visual Studio можно открыть `DemoApi.slnx`, выбрать проект `DemoApi`, профиль `http` и нажать F5. Порт 8088 выбран потому, что в исходной рабочей среде порт 8080 занят Oracle. Настройка — `src/DemoApi/Properties/launchSettings.json`.

Для Postman импортируйте [готовую коллекцию](postman/demo-api.postman_collection.json). Переменная `baseUrl` равна `http://localhost:8088`; при последовательном запуске коллекция сохраняет идентификаторы созданных объектов. Запросы также есть в [DemoApi.http](src/DemoApi/DemoApi.http).

## Запуск сервиса и БД через Compose

Нужны Docker Desktop с Linux-контейнерами и Docker Compose v2+. Из корня репозитория при первом запуске:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
# Задайте DB_PASSWORD в .env, затем:
docker compose config --quiet
docker compose up -d --build --wait
curl.exe http://localhost:8088/health/ready
```

Существующий `.env` повторно не перезаписывайте: пароль должен соответствовать сохраненному тому PostgreSQL. `.env` исключен из Git; полный вывод `docker compose config` содержит пароль и не предназначен для публикации. API доступен на localhost:8088, БД — localhost:15432. Обычная остановка `docker compose stop` сохраняет данные. Полная инструкция — [материал 06](docs/lab03-compose.md).

## Разработка с PostgreSQL в Visual Studio

Остановите API-контейнер, чтобы освободить порт 8088, и оставьте БД запущенной:

```powershell
docker compose stop api
docker compose up -d --wait db
dotnet user-secrets set "Storage" "Postgres" --project src/DemoApi/DemoApi.csproj
dotnet user-secrets set "ConnectionStrings:Db" "Host=localhost;Port=15432;Database=demo;Username=demo;Password=<пароль из .env>" --project src/DemoApi/DemoApi.csproj
```

Введите собственный пароль вместо примера. Секреты сохраняются локально вне репозитория. Затем откройте `DemoApi.slnx` в Visual Studio 2026, выберите DemoApi и профиль `http`, нажмите F5. В Development доступен Swagger. После завершения отладки остановите процесс и верните контейнер командой `docker compose up -d --wait`.

При возвращении к InMemory удалите обе локальные настройки:

```powershell
dotnet user-secrets remove "Storage" --project src/DemoApi/DemoApi.csproj
dotnet user-secrets remove "ConnectionStrings:Db" --project src/DemoApi/DemoApi.csproj
```

## Проверка

Запуск в Docker и результаты лабораторной 2: [инструкции](docs/lab02.md), [сборки и проверки контейнера](evidence/lab02/README.md).

PostgreSQL, сохраненный том и команды повторного запуска: [лабораторная 3](docs/lab03-postgres.md), [результаты SQL-проверок](evidence/lab03/README.md). Пароль хранится только в игнорируемом `.env`; [.env.example](.env.example) содержит пустой шаблон.

Весь стек через Docker Compose: [команды и ответы материала 06](docs/lab03-compose.md), [14 технических проверок и Adminer](evidence/lab03-compose/README.md). При первом запуске скопируйте `.env.example` в `.env`, задайте DB_PASSWORD и выполните `docker compose up -d --build --wait`. API: localhost:8088; PostgreSQL: localhost:15432. Adminer включается профилем `tools` на localhost:8083. Обычный запуск сохраняет именованный том.

Остановите отладку приложения перед пересборкой, затем из корня репозитория:

```powershell
$env:Storage = 'InMemory'
dotnet test DemoApi.slnx
Remove-Item Env:Storage
```

Для проверки отдельно запущенного API нужен PowerShell 7:

```powershell
pwsh -File scripts/verify-lab01.ps1 -Phase All -BaseUrl http://localhost:8088 -IncludePastDueValidation
```

Скрипт создает тестовые проекты, проверяет ответы и удаляет созданные им проекты; `-KeepData` сохраняет их для демонстрации. Каждый запуск записывает результаты в новый подкаталог `evidence/lab01/`.

## API и конфигурация

| Адрес | Назначение |
|---|---|
| `/` | service, version, host и сообщение hello from CI/CD |
| `/api/projects`, `/api/tasks` | Создание, чтение, удаление; изменение и фильтрация задач |
| `/api/tasks/{id}/status` | Смена статуса задачи |
| `/api/projects/{id}/stats` | Статистика задач проекта; отсутствующий проект — 404 |
| `/health/live`, `/health/ready` | Жизнеспособность и готовность |
| `/metrics` | Метрики Prometheus |
| `/swagger`, `/openapi/v1.json` | Интерфейс запросов и контракт OpenAPI в Development |

`Storage=InMemory` используется по умолчанию: данные существуют только до завершения процесса. Для SQL-режима нужны работающий PostgreSQL, `Storage=Postgres` и `ConnectionStrings__Db` в конфигурации окружения. При старте создается схема. Секреты в репозиторий не добавляются.

Статусы: Todo ↔ InProgress ↔ Done; прямой переход Todo ↔ Done возвращает 409. Статистика считает просроченными незавершенные задачи со сроком раньше текущего дня UTC. POST задачи с прошедшим сроком возвращает 400 с `errors.DueDate`; PUT позволяет изменить срок существующей задачи. Детали и примеры — в [разборе работы](docs/lab01.md).

## Структура

| Каталог | Содержимое |
|---|---|
| `src/DemoApi` | Контроллеры, сервисы, модели и два варианта хранилища |
| `tests/DemoApi.Tests` | Юнит- и интеграционные тесты |
| `postman`, `scripts` | Коллекция запросов и повторяемая HTTP-проверка |
| `docs` | Навигация по работам и пояснения |
| `reports` | PDF-отчеты и архив исходников для сдачи |
| `evidence/lab01`, `evidence/lab02`, `evidence/lab03`, `evidence/lab03-compose` | Сохраненные результаты проверок и скриншоты |

Карта компонентов и путь запроса — в [STRUCTURE.md](STRUCTURE.md). Dockerfile, PostgreSQL, том, общая сеть и Compose проверены. [Git/GitHub: материал 07](docs/lab04-git.md) содержит ссылки на PR, доску, правила и ограничения формальной сдачи. `main` принимает изменения через PR с одним одобрением. CI/CD с GHCR, локальным deploy и откатом проверен в материалах 09–10. Четыре сценария отказов и остановки проверены в материале 11. Материал 12 завершает разбор сбоев и добавляет diag.ps1. Работы 13–15 еще не начаты.
