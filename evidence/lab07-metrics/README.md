# Material13 / lab7 part1 evidence

ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

Реальный локальный запуск 2026-10-24. API версия **sha-e8be38f**, Storage PostgreSQL. Основная числовая точка **16:40:13 UTC (21:40:13 UTC+5)**. Моменты остальных скриншотов/ответов отличаются. [PR #22](https://github.com/Aruzhaaan-06/devops-labs/pull/22), [PDF](../../reports/lab07-metrics-report.pdf), [инструкция и интерпретация](../../docs/lab07-metrics.md).

- `targets.json`: три activeTargets, все UP.
- `required-*.json`: пять заданных выражений, raw instant и query_range.
- `own-*.json`: четыре собственных выражения и результаты. p95 у действий без трафика — NaN, сохранено как есть.
- `api-metrics.txt`, `cadvisor-metrics.txt`: настоящие строки raw /metrics; cAdvisor ограничен нашим API.
- `error-requests.json`, `repeated-errors.json`: реальные тела/коды400/409, отдельная задача остается Todo.
- `containers.json`: только ID/image/state/ports/privileged/limit, без Config.Env.
- `promtool.txt`, `rules.json`: синтаксис конфигурации и пять загруженных правил.
- `load-console.txt`, `load-results.json`:1200итераций,0ошибок,1200InProgress, project26, процесс завершен.
- `retained-markers.json`: старые project/task10–12 совпали с исходными объектами.
- `postman-console.txt`, `postman-results.json`:5read-only запросов /15assertions/0failures,exit0. Точный queryTime; no-report-events, cloudPublished=false.
- `screenshots.json`:13PNG и их SHA-256. Снимки реального Chrome через CUA, графики не перерисованы.

Обязательные снимки: [все UP](screenshots/targets-up.png), [число созданных задач](screenshots/own-created.png), [память %](screenshots/own-memory.png), [p95 по действиям](screenshots/own-p95.png), [клиентские ошибки](screenshots/own-4xx.png). Дополнительно: пять required Graph, Grafana, cAdvisor и Dozzle.

Состояние API во время опыта и окончательный SHA после публикации различаются из-за новых коммитов с отчетом. Итоговая проверка CI/CD/main/runtime размещается отдельным asset `lab13-final-verification.json` в существующем v1.0.0. Материалы14–15 здесь не заявляются выполненными; прежний формальный чек-лист сохраняется.
