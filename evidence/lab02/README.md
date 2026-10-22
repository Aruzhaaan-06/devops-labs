# Результаты лабораторной 2 · Docker · часть 1

Запуски от 22 октября 2026 года. Материал 03, неделя 3, контрольная точка 2, разделы 1–5. Проверяется настоящий Linux-контейнер DemoApi с хранилищем InMemory.

## Обязательная часть

| Требование | Результат | Доказательство |
|---|---|---|
| Docker Desktop и PowerShell 7 | Docker 29.8.0, PowerShell 7.6.5 | [Docker version](docker-version.txt), [PowerShell](powershell-version.txt) |
| WSL 2 и не менее 4 ГБ памяти | WSL engine включен, docker-desktop WSL 2; 7,62 ГиБ | [Параметры среды](environment.json), [WSL](wsl-distributions.txt) |
| Первый контейнер | Hello from Docker, код завершения 0 | [hello-world](hello-world.txt) |
| Базовый образ и слои | aspnet:10.0 скачан, история записана | [Pull](base-pull.txt), [history](base-history.txt), [размер](base-size.json) |
| Multi-stage Dockerfile и исключения | Сборка и статическая проверка успешны | [Dockerfile](../../Dockerfile), [.dockerignore](../../.dockerignore), [проверка](dockerfile-check.txt) |
| Первая сборка | Образ lab02-1.0 собран | [Полный вывод](build-first.txt) |
| Повторная сборка после изменения кода | restore CACHED, COPY src и publish выполнены заново | [Полный вывод](build-second.txt), [проверка шагов и SHA-256](cache-check.json) |
| Скриншот Settings → General | Пока отсутствует: захват окна вернул тайм-аут | [Состояние и ошибка захвата](environment.json) |

Скриншот WSL 2 явно требуется для сдачи. Конфигурация и команды подтверждают настройку, но не заменяют изображение интерфейса. Поэтому техническая часть выполнена, полный комплект оформления пока требует этого скриншота.

## Дополнительная проверка собранного контейнера

| Проверка | Результат | Материал |
|---|---|---|
| Runtime, здоровье, пользователь, API | 14 проверок, все успешны | [Итог](runtime-checks.json) |
| Образ | Linux/amd64, UID 1654; размер 354 253 942 байта (337,8 МиБ) | [Inspect](image.json), [теги и размеры](image-sizes.jsonl) |
| SDK и исходники | SDK отсутствует; в /app нет C#/csproj/решения | [Итог](runtime-checks.json), [файлы /app](runtime-files.txt) |
| Здоровье | healthy; live и ready возвращают 200 | [Healthcheck](health-production.json), [HTTP](health-http.json) |
| Production / Development | Swagger 404 / 200, тот же образ | [Production](swagger-production.json), [Development](swagger-development.json) |
| OpenAPI / учебные сбои | Контракт доступен, stats есть; Chaos отключен | [OpenAPI](openapi-development.json), [Chaos 404](chaos-development.json) |
| InMemory после stop/start | 1 проект → 0, тот же контейнер | [До](restart-before.json), [после](restart-after.json) |
| HTTP-сценарии | 26 запросов: 23 сценария и 3 удаления тестовых проектов | [Запросы и ответы](20261022T004046371Z-all-346370bd/http-evidence.json) |
| Postman CLI | 24 запроса, 73 проверки, 0 ошибок | [Журнал](postman-console.txt), [код завершения](postman-exit-code.txt) |
| .NET Release | 28/28 тестов; 0 failed и skipped | [Обезличенная сводка](tests/summary.json), [консоль](tests-console.txt) |
| Завершение демонстрации | Оба учебных контейнера остановлены | [Состояние](container-final-state.jsonl) |

Журналы приложения: [Production](api-logs.txt), [Development](swagger-logs.txt). Приложение слушало 8080 внутри контейнера; на Windows использовались только localhost:8089 и localhost:8090. Данные тестовой коллекции после остановки процесса не сохраняются.

Postman запускался с `--no-report-events`, авторизация для локального запуска не требуется. Предупреждение CLI об отсутствии входа относится к облачной публикации; фактический код завершения 0 и таблица показывают успешный локальный запуск. Облачная публикация результатов Postman не выполнялась. Оригинальный TRX с локальными метаданными исключен из Git; опубликована сводка.

[Отчет PDF](../../reports/lab02-part1-report.pdf) · [Инструкции и ответы](../../docs/lab02.md) · [На главную](../../README.md)
