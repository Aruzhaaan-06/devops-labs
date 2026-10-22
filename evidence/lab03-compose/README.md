# Docker Compose · материал 06 · результаты

22 октября 2026 года. [PDF](../../reports/lab03-compose-report.pdf) · [Команды и ответы](../../docs/lab03-compose.md) · [14 успешных проверок](checks.json).

| Проверка | Доказательства |
|---|---|
| Конфигурация и запуск | [Обезличенный config](compose-config-redacted.json), [up --build --wait](up-build.txt), [healthy-сервисы](healthy-services.json) |
| Ручное развертывание: 7 команд / 21 опция | [Команды и границы подсчета](manual-command-count.json) |
| Свободная подсеть | [Выбор](network-selection.json) |
| Резервная копия и восстановление | [Размер, SHA256 и три восстановленных проекта](backup-restore.json) |
| Три числа 3 → 3 → 2 | [Сводка](three-counts.json), [до](projects-before-down.json), [после down](projects-after-down.json), [после down -v](projects-after-down-volumes.json) |
| Жизненный цикл | [down](down.txt), [up](up-after-down.txt), [down -v](down-volumes.txt), [новый up](up-after-volume-reset.txt), [инициализация](database-new-volume.txt) |
| DNS db | [getent](dns-db.txt) |
| Остановка БД: live 200 / ready 503 / tasks 500 | [HTTP](database-stopped-http.json), [stop](stop-db.txt), [API остался healthy](api-health-database-stopped.json) |
| Восстановление без рестарта API | [start db](start-db.txt), [HTTP](database-recovered-http.json), [сводка проверок](checks.json) |
| CPU, RAM, swap, логи, restart, USER | [Реальная конфигурация контейнера](runtime-configuration.json) |
| .env игнорируется | [Точный вывод Select-String](gitignore-check.txt) |
| Windows API + БД Compose | [Сборка](host-build.txt), [HTTP](host-development-http.json), [журнал процесса](host-development-console.txt), [возврат API Compose](restore-compose-api.txt) |
| Тесты на отдельной demo_tests | [24 обязательных](required-24/summary.json), [консоль 24](required-24-console.txt), [28 полных](full-28/summary.json), [консоль 28](full-28-console.txt) |
| HTTP, 26 запросов с очисткой | [Запросы, ответы, assertions](20261022T134617368Z-all-d2305b12/http-evidence.json), [консоль](http-console.txt) |
| Postman, 24 запроса / 73 assertions / 0 ошибок | [Журнал](postman-console.txt), [код 0](postman-exit-code.txt) |
| Adminer 6.1.2, подключение к db | [Версия, digest, таблицы](adminer.json), [projects](screenshots/adminer-projects.jpg), [tasks](screenshots/adminer-tasks.jpg) |
| Завершение | [Логи](services-logs.txt), [остановка](stop-final.txt), [три сервиса остановлены и тома сохранены](final-state.json) |

Снимки Adminer настоящие: 5 проектов и 9 задач показаны после запуска Postman, добавившего фикстуры. Эксперимент 3 → 3 → 2 выполнен раньше. Старый том материала 05 не удалялся. Перед удалением отдельного тома Compose проверены резервная копия и ее восстановление; сам архив остается вне Git.

Обязательные 24 теста исключают четыре дополнительных случая DueDate; полный запуск содержит 28. C# не менялся. Raw TRX с локальными метаданными игнорируются Git. Абсолютные пути заменены на `[REPO]`/`[WORK]`, пароль удален. Предупреждение Postman об облачной авторизации не является ошибкой коллекции: запуск локальный, `--no-report-events`, exit 0.

Windows-процесс запускался через dotnet. Скриншоты консоли Visual Studio и Test Explorer из накопительной сдачи лабораторной 3 отсутствуют; ручной F5 не подтвержден. Новые пункты материала 06 допускают вывод команд и текстовые объяснения. Ограничения явно указаны в отчете.
