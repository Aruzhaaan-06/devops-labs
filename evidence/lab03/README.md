# Результаты лабораторной 3 · PostgreSQL · материал 05

22 октября 2026 года. Части 1 и 2, разделы 1–5. Запуски выполнены на настоящей PostgreSQL 18.6 в Linux-контейнере; API проверен с Windows и из отдельного контейнера.

[Общая сводка: 15 успешных проверок](checks.json) · [Отчет PDF](../../reports/lab03-postgres-report.pdf) · [Инструкция и ответы](../../docs/lab03-postgres.md).

## База и сохранение данных

| Эксперимент | Фактический результат | Доказательство |
|---|---|---|
| Подготовка kit.zip | Распакован локально, .env.example найден | [Сводка](kit-check.json) |
| Образ и версия PostgreSQL | postgres:18-alpine; PostgreSQL 18.6 | [Pull](postgres-pull.txt), [образ/digest](database-image.json), [SQL-версия и PGDATA](database-version.json) |
| Без именованного тома | Новый контейнер получил другой анонимный том, таблицы notes нет | [ID, тома, SQL и ошибка](without-named-volume.json) |
| Первая инициализация | seed.sql создал 2 проекта и 4 задачи | [Журнал](database-first-start.txt), [SELECT](seed-data.json) |
| Добавление задачи | Через SQL добавлена «Задача из лабы 3» | [INSERT](volume-insert.json) |
| Пересоздание с тем же томом | Сохранились все 5 задач | [Новые ID контейнеров и SELECT](volume-after-recreate.json) |
| Повторный старт БД | Skipping initialization, seed.sql не повторялся | [Журнал](database-recreated.txt) |

Анонимные тома одноразового эксперимента удалены после проверки. Именованный том `devops-labs-lab03-pgdata` с основной базой сохранен. Старый анонимный том сам по себе не подключается к новому контейнеру — именно это проверяет первый эксперимент.

## Сервис Windows, SQL и тесты

| Проверка | Фактический результат | Доказательство |
|---|---|---|
| Сборка Windows | Release, успешна | [Журнал](host-build.txt) |
| Выбор хранилища | «Хранилище: PostgreSQL» | [Первый процесс](host-first-start.txt), [новый процесс](host-second-start.txt) |
| Учебные проекты | Видны в API Windows | [GET](host-seed-projects.json) |
| Перезапуск процесса Windows | Проект id=3 сохранился | [До](host-before-restart.json), [после](host-after-restart.json) |
| Swagger после перезапуска | 200, учебные проекты, проекты Windows и контейнера | [Настоящий скриншот](screenshots/swagger-postgres-projects.jpg) |
| Обязательные случаи | 24/24: 7 юнит + 17 интеграционных | [Сводка](required-24/summary.json), [консоль](required-24-console.txt) |
| Полный текущий набор | 28/28: 7 юнит + 21 интеграционный | [Сводка](full-28/summary.json), [консоль](full-28-console.txt) |
| Реальная тестовая БД | demo_tests содержит данные тестовых фикстур | [SQL-подтверждение](tests-database-proof.txt) |
| Статистика SQL | Проверки пройдены; учебный проект: 4/2/1/1/0 | [Ответ stats](sql-stats.json), [тесты](full-28/summary.json) |

24 обязательных случая выбраны из текущей версии фильтром, исключающим четыре дополнительных случая DueDate. Полный запуск содержит все 28. Оба выполнены с `Storage=Postgres` на отдельной базе `demo_tests`; исходный код приложения и тестов не менялся. Оригинальные TRX с локальными метаданными исключены из Git; сводки сохраняют реальные имена и результаты тестов.

Windows-процесс запущен через dotnet, с Development и конфигурацией из окружения. Ручной F5 в Visual Studio не подтвержден. Журнал перенаправленного Windows-процесса получен в CP866 и переведен в UTF-8 с сохранением содержания; локальные пути заменены на `[REPO]`/`[WORK]`.

## Контейнеры и подключение

| Попытка / проверка | Результат | Доказательство |
|---|---|---|
| Образ API | Собран с APP_VERSION=lab03-postgres | [Вывод сборки](api-build.txt) |
| Только Storage=Postgres | Ожидаемое падение: строка подключения не задана | [Ошибка](attempt-missing.json), [журнал](attempt-missing.txt) |
| Host=localhost | Ожидаемое падение: 127.0.0.1:5432, Connection refused | [Ошибка](attempt-localhost.json), [журнал](attempt-localhost.txt) |
| Пользовательская сеть | Выбрана свободная явная подсеть при исчерпании стандартного пула | [Выбор подсети](network-selection.json), [DNS](docker-dns.txt) |
| Общая сеть и имя БД | API healthy, ready 200 | [Health](api-health.json), [ready](api-ready.json), [журнал](api-postgres-logs.txt) |
| Общие данные | Контейнер видит проект Windows id=3 | [GET](container-before-restart.json) |
| Перезапуск API-контейнера | Его проект id=4 сохранился | [После stop/start](container-after-restart.json) |
| HTTP-сценарии | 26 запросов: 23 сценария и 3 удаления тестовых проектов | [Запросы/ответы](20261022T005458521Z-all-3eba0a05/http-evidence.json) |
| Postman CLI | 24 запроса, 73 проверки, 0 ошибок | [Журнал](postman-console.txt), [exit code 0](postman-exit-code.txt) |
| Завершение работы | API Windows, API-контейнер и БД остановлены; том сохранен | [Контейнеры](final-containers.jsonl), [том](retained-volume.json), [финальный журнал БД](database-final-logs.txt) |

Первый сбой вызван отсутствием ConnectionStrings__Db в Production. Второй — тем, что localhost относится к самому API-контейнеру. Успешный запуск использует DNS-имя БД и внутренний порт 5432 общей сети. Windows подключался через опубликованный localhost:15432. Пароль в материалах не публикуется; локальный `.env` игнорируется Git.

Postman запускался локально с `--no-report-events`. Сообщение CLI об авторизации относится к облачной публикации и не означает сбой коллекции; код завершения 0 и 73 успешных assertions сохранены.

## Открытые пункты сдачи

Остаются скриншот консоли Visual Studio со строкой «Хранилище: PostgreSQL» и скриншот Test Explorer с 24 зелеными случаями. Настоящий Swagger-снимок, текст журналов и сводки TRX подтверждают свои проверки; они не объявляются выполнением недоступных UI-пунктов. Compose выполнен отдельно в [материале 06](../lab03-compose/README.md).

[Инструкция](../../docs/lab03-postgres.md) · [Все отчеты](../../reports/README.md) · [На главную](../../README.md)
