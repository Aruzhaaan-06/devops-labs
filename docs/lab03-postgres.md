# Лабораторная 3 · PostgreSQL · материал 05

**Есімханова Аружан · 25-ИСТК-2о**

Неделя 5, контрольная точка 3. Выполняются части 1 и 2 лабораторной: разделы 1–5 — база в контейнере и сервис с PostgreSQL. Compose относится к материалу 06 и здесь не выполняется.

Состояние проекта сохраняет [тег lab03-postgres](https://github.com/Aruzhaaan-06/devops-labs/tree/lab03-postgres). [Отчет PDF](../reports/lab03-postgres-report.pdf) · [Доказательства выполнения](../evidence/lab03/README.md).

## Что требуется для сдачи

Один PDF/DOCX с ФИО, группой, номером задания, подписями результатов и кликабельными ссылками на GitHub:

1. Ответы на вопросы пунктов 1 и 3.
2. Скриншот консоли со строкой «Хранилище: PostgreSQL», подтверждение сохранения проекта после перезапуска сервиса и 24 зеленых теста.
3. Строки ошибок двух неудачных запусков контейнера и объяснение каждой.

Технические действия выполнены, настоящий скриншот Swagger сохранен. Сервис Windows запускался через dotnet с конфигурацией окружения. Скриншоты консоли Visual Studio и Test Explorer пока отсутствуют; ручной запуск через F5 не подтвержден. Сводки настоящих запусков тестов и журналы опубликованы отдельно от этих UI-пунктов.

## Подготовка и конфигурация

Нужны Docker Desktop с Linux-контейнерами, PowerShell 7 и .NET 10 SDK; для UI-пунктов — Visual Studio 2026. Архив kit.zip распакован вне репозитория, наличие `.env.example` проверено. В репозитории оставлен безопасный шаблон [.env.example](../.env.example).

Пароль сгенерирован локально и записан в игнорируемый `.env`. В опубликованных материалах его нет. Для нового развертывания:

```powershell
if (-not (Test-Path .env)) {
    "DB_PASSWORD=$([Guid]::NewGuid().ToString('N'))" | Set-Content -Encoding utf8 .env
}
$passwordEntry = Get-Content .env | Where-Object { $_ -match '^DB_PASSWORD=.+$' } | Select-Object -First 1
if (-not $passwordEntry) { throw 'Задайте DB_PASSWORD в локальном .env.' }
$env:POSTGRES_PASSWORD = $passwordEntry.Substring('DB_PASSWORD='.Length)
```

При повторном подключении имеющегося тома пароль должен совпадать с тем, который использовался при его первой инициализации. Изменение `.env` не меняет пароль пользователя в существующей базе.

Имена ресурсов начинаются с `devops-labs-lab03`. Порты опубликованы только на localhost: PostgreSQL — 15432, API Windows — 8091, API-контейнер — 8092. Существующие сервисы на 8080/8088 не используются.

## Часть 1: база и данные

В отдельном одноразовом PostgreSQL-контейнере были выполнены:

```sql
CREATE TABLE notes (text text);
INSERT INTO notes VALUES ('check');
SELECT * FROM notes;
```

После удаления контейнера и создания нового без повторного подключения того же хранилища `SELECT * FROM notes` вернул `ERROR: relation "notes" does not exist`.

**Ответ пункта 1.** Образ PostgreSQL сам объявляет VOLUME. Без явного именованного тома Docker создает анонимный; новый контейнер получает другой анонимный том. Прежние данные автоматически не подключаются. `docker rm` без `-v` может оставить старый анонимный том, но новый контейнер его не использует. После эксперимента удалены только его одноразовые ресурсы.

Основной стенд при первом создании:

```powershell
docker volume create devops-labs-lab03-pgdata
docker run -d --name devops-labs-lab03-db `
    -e POSTGRES_DB=demo -e POSTGRES_USER=demo -e POSTGRES_PASSWORD `
    -v devops-labs-lab03-pgdata:/var/lib/postgresql `
    --mount "type=bind,source=${PWD}\db,target=/docker-entrypoint-initdb.d,readonly" `
    -p 127.0.0.1:15432:5432 postgres:18-alpine
docker exec devops-labs-lab03-db pg_isready -h 127.0.0.1 -U demo -d demo
```

Дождитесь готовности PostgreSQL перед обращением к базе. Журнал первого старта подтвердил выполнение `seed.sql`: 2 проекта и 4 задачи. Затем через psql добавлена пятая задача «Задача из лабы 3». После пересоздания контейнера с тем же томом все 5 задач сохранились; журнал содержит `Skipping initialization`.

**Ответ пункта 3.** Именованный том сохраняет кластер PostgreSQL независимо от контейнера. Init-скрипты выполняются только на пустом каталоге данных. Поэтому новый контейнер с непустым томом пропускает инициализацию, не повторяет seed.sql и видит добавленную задачу.

Для PostgreSQL 18 том подключается в `/var/lib/postgresql`, фактический PGDATA — `/var/lib/postgresql/18/docker`. Это изменение относительно образов до 18: [официальное описание образа](https://hub.docker.com/_/postgres).

## Часть 2: сервис Windows и тесты

Для запуска с конфигурацией через окружение:

```powershell
$env:Storage = 'Postgres'
$env:ConnectionStrings__Db = "Host=127.0.0.1;Port=15432;Database=demo;Username=demo;Password=$env:POSTGRES_PASSWORD"
$env:Chaos__Enabled = 'false'
dotnet run --project src/DemoApi/DemoApi.csproj --launch-profile http -- --urls http://127.0.0.1:8091
```

Запуск в этой работе фактически выполнен через собранную Release DLL с этими настройками в окружении Development. В журнале есть «Хранилище: PostgreSQL»; проект «Лаба 3: проект с Windows» сохранился после завершения и повторного запуска процесса. Скриншот Swagger показывает его вместе с учебными проектами и проектом API-контейнера.

Для запуска из Visual Studio те же переменные должны быть доступны ее процессу или задаваться локальной конфигурацией разработки. Реальный пароль не следует записывать в отслеживаемые `appsettings*.json` и `launchSettings.json`.

Для тестов создана отдельная база `demo_tests` с владельцем demo в том же контейнере. Она не смешивает интеграционные фикстуры с учебными проектами:

```powershell
docker exec devops-labs-lab03-db psql -U demo -d demo -c 'CREATE DATABASE demo_tests OWNER demo;'
$env:Storage = 'Postgres'
$env:ConnectionStrings__Db = "Host=127.0.0.1;Port=15432;Database=demo_tests;Username=demo;Password=$env:POSTGRES_PASSWORD"
dotnet test DemoApi.slnx -c Release --filter 'FullyQualifiedName!~Create_PastDueDate&FullyQualifiedName!~Create_ValidDueDate'
dotnet test DemoApi.slnx -c Release
Remove-Item Env:Storage, Env:ConnectionStrings__Db, Env:Chaos__Enabled
```

Создание `demo_tests` требуется только один раз. Обязательная выборка дала 24/24 (7 юнит + 17 интеграционных), полный набор — 28/28 (7 + 21). В первой команде исключаются четыре дополнительных случая срока задачи. SQL-статистика и 404 неизвестного проекта проверены по-настоящему; изменение `ProjectRepository.GetStatsAsync` не потребовалось.

## Три запуска API-контейнера

Образ собран с `APP_VERSION=lab03-postgres`. Первые два запуска действительно завершились с ошибками:

| Попытка | Фактическая строка | Причина |
|---|---|---|
| Только Storage=Postgres | `System.InvalidOperationException: Не задана строка подключения ConnectionStrings:Db` | В Production не загружается appsettings.Development.json, строка подключения не передана |
| Строка с Host=localhost | `Npgsql.NpgsqlException: Failed to connect to 127.0.0.1:5432`; `Connection refused` | localhost — сам API-контейнер, PostgreSQL работает в другом |
| Общая сеть и имя БД | healthy, ready 200, видны те же проекты | Контейнеры находят друг друга через DNS пользовательской сети |

Стандартный пул подсетей Docker на рабочей машине оказался исчерпан. После проверки пересечений создана отдельная сеть с явной свободной подсетью 10.254.53.0/24. Для другого компьютера нужно проверить доступность выбранной подсети.

```powershell
docker network create --subnet 10.254.53.0/24 devops-labs-lab03-net
docker network connect devops-labs-lab03-net devops-labs-lab03-db
$env:ConnectionStrings__Db = "Host=devops-labs-lab03-db;Database=demo;Username=demo;Password=$env:POSTGRES_PASSWORD"
docker run -d --name devops-labs-lab03-api --network devops-labs-lab03-net `
    -p 127.0.0.1:8092:8080 -e Storage=Postgres -e ConnectionStrings__Db `
    devops-labs-demo-api:lab03-postgres
Remove-Item Env:ConnectionStrings__Db
```

Публикация 15432 нужна для Windows-клиента. API в общей сети идет на внутренний порт 5432; опубликованный порт Windows здесь не участвует. После `docker stop/start` API-контейнера его проект также сохранился. На нем прошли 26 HTTP-запросов и 24 запроса/73 проверки Postman CLI.

## Возврат к сохраненному стенду

После демонстрации учебные API и БД остановлены, именованный том сохранен. Чтобы снова открыть API-контейнер:

```powershell
docker start devops-labs-lab03-db
docker exec devops-labs-lab03-db pg_isready -h 127.0.0.1 -U demo -d demo
# После готовности БД:
docker start devops-labs-lab03-api
Invoke-RestMethod http://localhost:8092/api/projects
```

Для повторения эксперимента с пересозданием БД не удаляйте именованный том. Полное удаление тома уничтожило бы данные и не требуется для продолжения курса. Compose в этой работе еще не создан.

[Сводка и журналы](../evidence/lab03/README.md) · [Отчет](../reports/lab03-postgres-report.pdf) · [Список работ](README.md)
