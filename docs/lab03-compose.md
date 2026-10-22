# Лабораторная 3, часть 3 · материал 06 · Docker Compose

**Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 22 октября 2026 года.**

Выполнены разделы 6–11 и дополнительное задание Adminer. [Отчет](../reports/lab03-compose-report.pdf), [результаты](../evidence/lab03-compose/README.md), [фиксированная версия](https://github.com/Aruzhaaan-06/devops-labs/tree/lab03-compose).

## Требования и результат

| Требование | Подтвержденный результат |
|---|---|
| Разбор ручного развертывания | 7 команд и 21 вхождение опций; состав и границы подсчета сохранены в manual-command-count.json |
| Один compose.yaml | API, PostgreSQL, том, сеть, healthcheck, ожидание БД, ресурсы и ротация журналов |
| Запуск up --build --wait | API и БД healthy |
| Три числа из пункта 9 | 3 перед down, 3 после down/up, 2 после down -v/up |
| DNS и отказ БД | db разрешается; live 200, ready 503, tasks 500; API остается healthy |
| Восстановление | После start db снова 200; API не перезапускался |
| Режим разработки | Windows dotnet + БД Compose; проекты и задачи 200 |
| Проверки | PostgreSQL: обязательные 24/24, полные 28/28; HTTP 26 запросов; Postman 24 запроса / 73 assertions |
| .env | Точная команда Select-String нашла правило; файл исключен из Git |
| Adminer ⭐ | Вход на db и просмотр projects/tasks; два настоящих снимка |

## Запуск

Нужны Docker Desktop с Linux-контейнерами и Compose v2+; для запуска на Windows и тестов — .NET 10 SDK. PowerShell 7 нужен для скрипта HTTP-проверки. Postman CLI необязателен для самого стека.

```powershell
Copy-Item .env.example .env
# Откройте .env и задайте собственный DB_PASSWORD.
docker compose config --quiet
docker compose up -d --build --wait
docker compose ps
curl.exe http://localhost:8088/health/ready
curl.exe http://localhost:8088/api/projects
```

Копировать шаблон следует только при первом запуске: сохраните существующий `.env` и его пароль при повторном подключении тома. Изменение пароля в `.env` само по себе не меняет пароль уже инициализированной PostgreSQL.

`.env.example` содержит пустой пароль и безопасные настройки портов. Compose требует непустой DB_PASSWORD. Полный `docker compose config` содержит подставленный пароль — для публикации используйте только обезличенную копию. В репозитории сохранена именно такая копия.

Фиксированное имя проекта `devops-labs` отделяет ресурсы от других стендов. Порт API 8088 выбран из-за занятого 8080; БД — 15432, Adminer — 8083. Все публикации привязаны к 127.0.0.1. Внутри сети API использует `Host=db` и порт 5432. Не задавайте второму экземпляру такое же имя проекта.

API_IMAGE и API_TAG управляют именем и тегом собираемого образа. Для зафиксированного запуска использован API_TAG=lab03-compose. Дефолт `local` подходит для повторной сборки. Явная подсеть 10.254.54.0/24 выбрана после проверки свободных диапазонов, поскольку стандартный пул Docker в рабочей среде исчерпан; при конфликте замените COMPOSE_SUBNET в `.env` на свободную подсеть.

## Жизненный цикл данных

На свежем `devops-labs_pgdata` seed.sql создал два проекта и четыре задачи. Через API добавлен проект Compose, после чего получены **3 → 3 → 2**:

1. Перед остановкой — два seed-проекта и Compose.
2. `docker compose down`, затем `docker compose up -d --wait` — том сохранен, все три проекта остались.
3. `docker compose down -v`, затем `docker compose up -d --wait` — удален только отдельный учебный том Compose; на новом томе seed.sql снова создал два проекта.

Перед сбросом выполнены `pg_dump -Fc` и восстановление в отдельную demo_restore: все три проекта найдены. Архив хранится локально вне Git. Проверено, что сбрасываемая база содержит только данные этого эксперимента. Том материала 05 `devops-labs-lab03-pgdata` сохранен отдельно. `down -v` повторяйте только на одноразовых данных после резервного копирования; для обычного завершения достаточно `stop` или `down` без `-v`.

Подсчет ручных команд относится к минимальному развертыванию материала 05: том, БД, одна проверка готовности, сборка API, сеть, подключение БД и запуск API. Повторы ожидания, учебные ошибки и тесты исключены; [полный состав](../evidence/lab03-compose/manual-command-count.json).

## БД недоступна

```powershell
docker compose exec api getent hosts db
docker compose stop db
curl.exe -i http://localhost:8088/health/live
curl.exe -i http://localhost:8088/health/ready
curl.exe -i http://localhost:8088/api/tasks
docker compose start db
```

При остановленной БД ответы соответственно **200 / 503 / 500**. Docker healthcheck API проверяет live: процесс жив, поэтому healthy сохраняется. Ready отдельно проверяет БД. После восстановления PostgreSQL запросы снова дали 200 без перезапуска API. `depends_on: service_healthy` задает порядок запуска при `up`, а не постоянный контроль зависимостей.

Примененные ограничения API: 1 CPU, 256 MiB RAM, дополнительный swap отсутствует; logging json-file 10m × 3, restart unless-stopped. Chaos включен по методичке. Отдельно сохранены реальные HostConfig и health-состояния.

## Разработка и тесты

```powershell
docker compose stop api
$env:Storage = 'Postgres'
# Введите локальную строку с вашим паролем, не сохраняйте ее в Git.
$env:ConnectionStrings__Db = 'Host=localhost;Port=15432;Database=demo;Username=demo;Password=<локальный пароль>'
$env:Chaos__Enabled = 'false'
dotnet run --project src/DemoApi/DemoApi.csproj --launch-profile http
# Завершите dotnet (Ctrl+C), затем:
Remove-Item Env:Storage,Env:ConnectionStrings__Db,Env:Chaos__Enabled
docker compose up -d --wait
```

Контейнер API освобождает 8088, PostgreSQL остается запущенной. Ручное F5 не подтверждено: фактически использован Windows-процесс dotnet. Интеграционные тесты запускались на отдельной demo_tests через `ConnectionStrings__Db`, чтобы не очищать основную базу. Обязательные 24 случая выбраны фильтром `FullyQualifiedName!~Create_PastDueDate&FullyQualifiedName!~Create_ValidDueDate`; полный набор содержит 28. Результаты Postman получены локально с `--no-report-events`.

## Adminer

```powershell
docker compose --profile tools up -d --wait
```

Откройте [Adminer](http://localhost:8083): PostgreSQL, сервер `db`, пользователь `demo`, база `demo`, пароль из локального `.env`. `localhost` внутри Adminer указывает на сам Adminer, поэтому нужен DNS-хост db. Реально использован образ Adminer 6.1.2; digest сохранен. На снимках 5 проектов и 9 задач: после эксперимента с тремя числами Postman создал свои фикстуры. Это более позднее состояние той же базы.

Вход завершен после демонстрации. Итоговый стек из трех сервисов остановлен, оба учебных именованных тома сохранены. Возобновить можно `docker compose up -d --wait`, Adminer включается отдельно профилем tools.

## Сдача и ограничения

В PDF включены полный compose.yaml, три числа с объяснениями, коды при остановленной БД, вывод `Select-String '^\.env$' .gitignore`, результаты тестов, ответы и снимки Adminer. Все 14 технических проверок успешны. Код C# не изменялся.

Из накопительного чек-листа лабораторной 3 остаются скриншоты консоли Visual Studio и Test Explorer с 24 зелеными случаями. Консольные результаты сохранены; UI-пункты не объявляются выполненными. Ранее открытые пункты других работ перечислены в [общем статусе](README.md). Следующий материал — 07, работа с Git и защитой ветки.
