# Материал 15 / лабораторная 8: доказательства

ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

[Инцидент #27](https://github.com/Aruzhaaan-06/devops-labs/issues/27) · [постмортем](https://github.com/Aruzhaaan-06/devops-labs/issues/27#issuecomment-6387899631) · [PR #26](https://github.com/Aruzhaaan-06/devops-labs/pull/26) · [GitHub Revert PR #28](https://github.com/Aruzhaaan-06/devops-labs/pull/28) · [отчёт](../../reports/lab08-incident-report.pdf) · [runbook](../../docs/lab08-incident.md).

Это реальные измерения localhost стенда 24 октября 2026, UTC (местное UTC+5). Нет подставленных состояний, фальшивых screenshots или обещания преподавательской оценки.

- `baseline.json`: исходный main/версия, 3 UP, inactive slow rule; сохранён `sha-cf768be`.
- `T0/T1/T2.json`, `incident-metrics.json`: определения и реальные timestamps. T1-T0 204,726 с включает pipeline; T2-T1 100,149 с включает восстановление и подтверждение. Опрос около 1 с, это наблюдаемые границы.
- `alerts-timeline.jsonl`, `first-firing.json`: полный реальный rule stream. Детектор не опрашивал приложение вручную, T1 записан раньше диагностических HTTP запросов.
- `diagnosis.json`: action/controller PromQL, Tasks/List p95 1,9968 с, version `sha-4e49041`, исходная строка 15 и HTTP 200 после алерта за 1,512 с. Histogram и wall-clock не смешиваются.
- `p95-global-range.json`, `p95-actions-range.json`, `alert-range.json`, `up-range.json`: сохранённые ответы Prometheus query_range. График PDF строится из них; NaN не заменяется нулём.
- `ci-summary.json`: bad PR/main и Revert PR/main, четыре настоящих PostgreSQL CI с 40/40. Полные публичные runs доступны по сохранённым ссылкам; исходные archives проверены на `Passed40/Total40`.
- `revert-operation.json`, `source-proof.json`, `revert-recovered.json`: GitHub **сам сгенерировал Revert PR** через официальный API; src/tests точно восстановлены, p95 Tasks/List около 1,76 мс. Permanent Compose/alerts/scrape не менялись.
- `latency-guard.json`, `bad-latency-guard.txt`, `good-latency-guard.txt`: тот же PowerShell smoke отклонил 1615,960 мс (exit 1) и пропустил 98,281 / 4,096 / 2,590 мс (exit 0). Локальный путь в ошибке заменён на `<work>`, лишние пустые строки в конце текстовых журналов убраны; значения не редактировались.
- `github-links.json`, `postmortem.json`: фактические issue/PR/rollback links и опубликованный postmortem comment. Каждому действию соответствует отдельный issue 29/30/31.
- `retained-data.json`, `load-tasks.json`: старые объекты и серии сохранены; 1771 InProgress задачи проекта 37, хеш точного набора. Пять ошибок транспорта при deploy не выданы за успешные запросы.
- `load-console.txt`, `load-stderr.txt`, `owned-load.json`, `observer-final.json`: bounded load и наблюдатель остановлены; предел 20 000 не означает 20 000 завершённых циклов. Напечатанные итерации — прогресс, не точный счётчик successes.
- `postman-console.txt`, `postman-results.json`: реальный read-only API/Prometheus, 6 запросов / 13 assertions / 0 failures, явный expectedVersion, все пять правил inactive; без Postman cloud.
- `snapshot-after-revert.json`, `fixed-api-logs.txt`: исправленная версия, health, targets/rules и сохранённый stdout текущего исправленного контейнера. Это не журнал удалённого плохого контейнера.
- `ui-status.json`: браузерная блокировка и отсутствие UI снимков объявлены явно. PDF содержит собственный график по API данным, не якобы снятый экран.
- `checks.json`, `report-validation.json`, `deliverables.json`: проверка фактов, PDF и общего архива; прошлые 13 PDF сохраняются без изменений.

В новом релизе v1.1.0 размещается `lab15-final-verification.json`: последний main/runtime, фактически выполненный deploy latency gate, 40/40, read-only Postman, все пять правил inactive, 3 UP, 7 панелей, сохранность данных, SHA256 PDF/ZIP и соответствие GitHub assets. Измерения инцидента в PDF относятся к более ранним bad/rollback/Revert этапам; manifest проверяет итоговый deploy, это разные моменты.

Остаются реальные ручные условия: UI screenshots, онлайн защита/слот в форуме/СДО, прежний чек-лист и неизвестный GitHub преподавателя. Второй аккаунт принадлежит тому же владельцу; reviews и assistant approvals не независимая человеческая работа. Issue #30 остаётся открытым расширением performance baseline.
