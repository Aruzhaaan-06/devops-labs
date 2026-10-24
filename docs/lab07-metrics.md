# Материал 13: метрики и PromQL

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о**

Лабораторная 7, часть 1, разделы 1–4. [PR #22](https://github.com/Aruzhaaan-06/devops-labs/pull/22), [казахский PDF](../reports/lab07-metrics-report.pdf), [результаты](../evidence/lab07-metrics/README.md).

Отдельный Compose `monitoring` запускает Prometheus v3.14.0, Grafana 13.2.1, cAdvisor v0.60.5, Dozzle v11.0.1. API, основной Compose и бизнес-логика не меняются. Данные Prometheus (retention 7 дней) и Grafana лежат в именованных томах. Provisioning и дашборд — в Git.

## Запуск и повторение

Сначала запустите основной стек согласно [инструкции CD](lab05-cd.md); `/health/ready` на localhost:8088 должен вернуть 200. Нужны Docker Desktop в режиме Linux containers, PowerShell 7, браузер; для скрипта сохранения результатов — Python 3, для коллекции — Postman CLI. Свободные порты: 9090, 3000, 8081, 8888.

```powershell
docker compose -f monitoring/compose.yaml config --quiet
docker compose -f monitoring/compose.yaml up -d
docker compose -f monitoring/compose.yaml exec -T prometheus promtool check config /etc/prometheus/prometheus.yml
pwsh ./scripts/load.ps1 -BaseUrl http://localhost:8088 -DelayMs 300 -Iterations 1200
```

Нагрузку запускайте в отдельном терминале. После минимум минуты под нагрузкой, в другом терминале:

```powershell
python scripts/verify-lab13.py --output ./tmp/lab13-new-run
postman collection run postman/lab07-metrics.postman_collection.json --env-var queryTime=<epoch-из-own-created.json> --no-report-events
```

Каталог результатов должен быть новым. Epoch находится в `instant.body.data.result[0].value[0]`. Коллекция по умолчанию использует сохраненный момент измерения 24 октября; он работает, пока соответствующая история хранится в локальном Prometheus. Для нового запуска обязательно передайте новый `queryTime`. Это 5 read-only запросов к **реальному** Prometheus, 15 assertions; ни мок, ни нагрузочный benchmark. Данные в облако Postman не публикуются.

`load.ps1`: создает один проект, в каждой итерации создает задачу, меняет статус на InProgress и читает Todo список; пауза 300 мс, счетчик каждые 20 циклов. `-Iterations 0` (по умолчанию) работает до Ctrl+C; положительное значение ограничивает запуск. При ошибках финальный exit code — 1. Проект/задачи остаются в учебной БД, чужие данные не удаляются. `verify-lab13.py` создает отдельный маленький проект для реальных 400/409 и тоже сохраняет его.

## Что проверено в UI

| UI | Проверка |
|---|---|
| [Prometheus](http://localhost:9090/targets) | Status → Target health: demo-api, cadvisor, prometheus UP; девять запросов в Query → Graph |
| [Grafana](http://localhost:3000) | admin/admin на новом локальном томе; Dashboards → DevOps course → DemoApi; пять панелей с данными |
| [cAdvisor](http://localhost:8081/docker/) | devops-labs-api-1; CPU/память и лимит 256 MiB |
| [Dozzle](http://localhost:8888) | devops-labs-api-1; создание задач и Todo → InProgress, JSON Information |

`prometheus.yml` собирает `/metrics` раз в 5 с: host.docker.internal:8088, cadvisor:8080 и localhost:9090. Хостовый порт API 8088 сохраняет прежнюю привязку 127.0.0.1, реальный scrape из Docker Desktop прошел. Имя контейнера во всех запросах/правилах/дашборде — `devops-labs-api-1`; CPU regex — `devops-labs-.*`.

Docker вернул `all predefined address pools have been fully subnetted`. Проверка существующих подсетей показала свободную `10.254.55.0/24`, она задана для monitoring. Для другой среды задайте `MONITORING_SUBNET`; при конфликте сначала проверьте `docker network inspect`. Существующие сети не удалялись. Другой контейнер PostgreSQL на порту 5433 не менялся.

## Запросы и смысл результатов

Все точные выражения и исходные API-ответы — в [доказательствах](../evidence/lab07-metrics). Короткие объяснения и 4 обязательных графика — в PDF.

| Запрос | Значение в основном срезе 16:40:13 UTC |
|---|---|
| up | Три цели, каждое значение 1 |
| RPS по controller/action | Tasks/Create 3.0365, ChangeStatus 3.0547, List 3.0183 запроса/с |
| Общий p95 | 0.0077956 с; приблизительная интерполяция histogram |
| Working set / 1024 / 1024 | 73.2461 MiB |
| CPU по name | API 0.02268 ядра; DB 0.01203 ядра |
| Свой: increase Tasks/Create/201 за 1m | 182.1918 задачи; дробное значение из-за экстраполяции |
| Свой: working set / limit ×100 | 28.6118%; лимит268435456 байт, нулевые лимиты исключены |
| Свой: p95 по controller/action | Tasks/Create 13.680 мс, ChangeStatus 3.970 мс, List 1.078 мс |
| Свой: 4xx по controller/action/code | Projects/Create/400 и Tasks/ChangeStatus/409, каждый 0.03637 запроса/с |

Без запросов за окно p95 отдельного действия — NaN, а не ноль. Первоначально проверяющий скрипт ошибочно требовал конечное значение для всех старых действий; после наблюдения NaN он исправлен и повторно выполнен. Итоговые JSON сохранены без подмены NaN. Пустые controller/action соответствуют также маршрутам вне MVC. HTTP counter считает ответы, не отдельные бизнес-события. Два одинаковых графика 400/409 накладываются; оба ряда сохранены.

Controller/action сопоставлены с реальными `ProjectsController.Create`, `TasksController.Create`, `TasksController.ChangeStatus`, `TasksController.List`. Raw `/metrics` сохранены отдельно. Код400 получен пустым name; код409 — попыткой Todo → Done. Для появления измеримого rate ошибки повторены после двух scrapes.

Правила прочитаны: ApiDown — up=0/30s; ApiHighErrorRate — 5xx>5%/30s; ApiSlowRequests — p95>1s/30s; ContainerHighMemory — >80%/15s; ContainerRestarted — изменение max start_time за5m. Promtool подтвердил 5 правил. Их намеренное срабатывание относится к материалу14.

## Границы и результат

Стек предназначен для локальной лабораторной. Все опубликованные порты привязаны к 127.0.0.1. cAdvisor privileged и host mounts, Dozzle Docker socket дают широкие возможности внутри Docker; `:ro` socket не делает Docker API безопасным по правам. Dozzle actions/shell не включены, фильтр показывает только devops-labs. Grafana admin/admin — локальный старт из методички; для внешнего размещения эта схема не подходит. DB_PASSWORD и GitHub credentials в файлы не включены.

Итог: 9 instant и 9 range ответов; 13 настоящих снимков Chrome, Postman5/15; нагрузка1200/0, 1200 InProgress; старые контрольные данные10–12 сохранены. Нагрузка остановилась сама, мониторинг оставлен работающим. Измерения относятся к API sha-e8be38f, PDF10страниц. Снимки и JSON сделаны в разные моменты: разница значений ожидаема; Prometheus графики UTC, Grafana использует время браузера UTC+5.

PR проходит обязательный PostgreSQL CI; после merge основной deploy обновляет только devops-labs. Отдельный monitoring должен пережить его без замены ID. Последний main/runtime, три цели UP, хеши файлов и сохранность данных проверяются в `lab13-final-verification.json` в [релизе v1.0.0](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0). Релизный тег и старые assets не заменяются. Два аккаунта для Approve принадлежат одному владельцу; approval local выполняет ассистент по поручению пользователя. Это не независимое человеческое ревью.

Официальные источники: [Prometheus functions](https://prometheus.io/docs/prometheus/3.12/querying/functions/), [cAdvisor](https://github.com/google/cadvisor), [Dozzle](https://dozzle.dev/guide/getting-started).
