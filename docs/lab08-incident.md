# Материал 15: инцидент в сервисе задач

ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

Итоговая лабораторная 8, все разделы 1-7. [Инцидент #27](https://github.com/Aruzhaaan-06/devops-labs/issues/27) · [постмортем](https://github.com/Aruzhaaan-06/devops-labs/issues/27#issuecomment-6387899631) · [казахский отчёт](../reports/lab08-incident-report.pdf) · [доказательства](../evidence/lab08-incident/README.md) · [релиз v1.1.0](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.1.0).

## Реальный цикл инцидента

Базовый main `cf768be` работал как `sha-cf768be`. Нагрузка `load.ps1` и Prometheus были включены, runner online. По [issue #25](https://github.com/Aruzhaaan-06/devops-labs/issues/25) в `TaskService.ListAsync` намеренно добавлен `await Task.Delay(1500, ct)`. [PR #26](https://github.com/Aruzhaaan-06/devops-labs/pull/26) и его main прошли PostgreSQL 40/40: функциональные проверки не имели бюджета задержки.

До алерта приложение вручную не проверялось. Работали штатные CI health checks, автоматическая нагрузка и наблюдатель `/api/v1/rules?type=alert`. Первое firing записано независимо от последующей диагностики. После него PromQL по controller/action показал Tasks/List, root version подтвердил `sha-4e49041`, а исходный код указал строку 15 с задержкой. Контрольный HTTP после алерта дал 200 за 1,512 с; histogram p95 был 1,9968 с. Это разные способы измерения: p95 интерполируется внутри bucket.

| Метка | UTC, 24 октября 2026 | Определение |
|---|---|---|
| T0 | 18:10:54.000 | GitHub merged_at PR #26; сборка/deploy идут после этого |
| T1 | 18:14:18.726 | Первый snapshot наблюдателя с ApiSlowRequests firing |
| T2 | 18:15:58.875 | После rollback подтверждены старая версия и inactive |

T1-T0 = **204,726 с**, включая CI/image/queue/deploy и мониторинг. T2-T1 = **100,149 с**, включая диагностику, dispatch/approval/runner, замену API и подтверждение восстановления. Это наблюдаемые интервалы, а не точные границы влияния на каждого клиента. Точность наблюдателя около 1 с; десятичные разряды не устраняют задержку опроса. Местное время UTC+5.

Кнопочный workflow rollback восстановил `sha-cf768be`. Затем **GitHub сам создал [Revert PR #28](https://github.com/Aruzhaaan-06/devops-labs/pull/28)** через официальную серверную операцию [revertPullRequest](https://docs.github.com/en/graphql/reference/pulls#revertpullrequest), эквивалент кнопки Revert. В нём `Refs #27`; это не вручную переписанный похожий метод. PR и main снова прошли 40/40, `sha-21b953a` задеплоен поверх отката. `src/tests` точно совпали с baseline; наблюдённый Tasks/List p95 стал 0,001758824 с.

## Действия после постмортема

- [#29](https://github.com/Aruzhaaan-06/devops-labs/issues/29): deploy теперь выполняет `scripts/smoke-tasks-latency.ps1`. Три read-only GET с заведомо отсутствующим projectId: каждый HTTP 200 и <1000 мс, timeout 5 с. Проверенный плохой образ: 1615,960 мс и exit 1; исправленный: 98,281 / 4,096 / 2,590 мс, exit 0. Изменён только deploy job, после readiness и перед Job summary.
- [#30](https://github.com/Aruzhaaan-06/devops-labs/issues/30): расширенный performance baseline с PostgreSQL и обоснованной нагрузкой остаётся открытым follow-up.
- [#31](https://github.com/Aruzhaaan-06/devops-labs/issues/31): runbook и план защиты представлены здесь и в PDF.

Smoke измеряет время клиентского HTTP обмена, включая локальные накладные расходы; это быстрый gate, а не статистический SLO-тест. Он делает такую регрессию видимой в deploy и не даёт ей завершиться незаметно зелёным job. Он запускается после замены образа, поэтому **не выполняет автоматический rollback**: при ошибке следует восстановить предыдущий sha по runbook. Пороги алертов, Compose, секреты, permissions и защита main не ослаблялись. Новых зависимостей/слоёв приложения нет.

## Повторение только на локальном учебном стенде

Нужны прежний `.env` с сохранённым DB_PASSWORD, Docker Linux containers, PowerShell 7, Python 3, работающий runner и monitoring. Не выводить `.env` или полный `docker compose config` в публикуемые журналы. Не удалять PostgreSQL volume.

1. Подтвердить чистый свежий main, version, готовность и 3 UP. Запомнить **существующий** прошлый sha-tag. Нагрузка должна работать, ApiSlowRequests быть inactive.
2. Для записи состояния запустить отдельный наблюдатель:

   ```powershell
   python scripts/observe-lab15.py --repo . --output ../lab15-new-observation --with-load --seconds 3600
   ```

   Он создаёт новый каталог, пишет rules JSONL и управляет только своим bounded load. Для остановки создать файл `STOP` внутри его output. Опциональный `--with-load` создаёт новый проект и задачи на localhost:8088; без него наблюдатель только читает Prometheus.

3. Issue → ветка `feat/<N>-audit` → задержка в ListAsync → обычный CI/review/merge. Записать T0 из merged_at. В output/phase.txt записать `bad-deploy`, чтобы наблюдатель сохранил первый firing отдельно. До алерта не делать ручных application probes.
4. После firing T1 выполнить PromQL из раздела ниже, затем GET `/`, связать version с commit и строкой кода. Не задерживать восстановление ради дополнительного анализа.
5. Запустить `gh workflow run ci-cd.yml --ref main -f tag=sha-<previous>` и подтвердить **выбранный** local environment run. После success проверить прежнюю version и снятие ApiSlowRequests; записать T2.
6. Создать issue инцидента и настоящий GitHub Revert PR с `Refs #incident`. Проверить CI/review/merge и новый main deploy. Сравнить данные и дождаться нормального p95. ContainerRestarted может сохраняться 5 минут после deploy; это окно не сокращать.
7. Постмортем комментарием, отдельный issue на каждое действие, закрытие инцидента после восстановления. Добавить release notes и ссылку на постмортем в новый релиз. **С новым latency gate намеренная задержка теперь провалит deploy smoke**, поэтому буквальное повторение уже не покажет прежний незаметно зелёный deploy; это ожидаемое предотвращение регрессии. Не отключать gate ради демонстрации.

ПромQL для локализации:

```promql
histogram_quantile(0.95,
  sum by (le, controller, action) (
    rate(http_request_duration_seconds_bucket{job="demo-api"}[1m])
  )
)
```

Проверка после восстановления (все пять alert rules должны стать inactive):

```powershell
./scripts/smoke-tasks-latency.ps1
postman collection run postman/lab08-incident.postman_collection.json --env-var expectedVersion=sha-<current-main> --no-report-events
python scripts/check-lab15-evidence.py
```

Коллекция **read-only: 6 запросов / 13 assertions / 0 failures**. Версия задаётся явно; неверный expectedVersion провалит проверку. В облако Postman результаты не публикуются. `check-lab15-evidence.py` проверяет сохранённые факты, не повторяя инцидент.

## Данные и ограничения

Нагрузка проекта 37 остановлена после здорового Revert deploy: **1771 InProgress** сохранены; 5 ошибок связи при замене контейнера не скрыты. Последняя напечатанная итерация 1760 — лишь прогресс каждые 20 циклов, не точное число успешных запросов. Старые контрольные объекты 10-12, 1200 задач материала 13, серии 2231/531 и бизнес-объекты материала 14 сохранены. Хеш полного набора задач проекта 37 проверяется после финального deploy.

Work продолжал возвращать `Local browser use is disabled in Work settings`. **Скриншоты алерта/Grafana не выполнены.** График PDF построен из реальных query_range данных и явно подписан как график, а не UI снимок. API/файловые инструменты не использовались для обхода browser denial. Если пользователь включит доступ и снимки будут добавлены позднее, это нужно оформить отдельным честно датированным дополнением.

Два GitHub аккаунта принадлежат одному владельцу, техническое CODEOWNER Approve не независимое peer review. Local approvals ассистент выполнил по поручению владельца, без обхода защиты. Приглашение преподавателя, отсутствующие условия материала 04 и прежние ручные пункты остаются в общем чек-листе. Оценку 70+ не гарантируем: итоговый балл выставляет преподаватель.

Защита 10 минут: 0-2 репозиторий/CI/release; 2-4 alert/action/version/code; 4-6 rollback/T0-T2/данные; 6-8 Revert/postmortem/actions; 8-10 два вопроса преподавателя. Шесть развёрнутых ответов на примеры вопросов есть в PDF. Запись на слот через форум курса, экранная демонстрация в Teams/Zoom/Meet и загрузка отчёта в СДО выполняются студентом.
