# Material14 / lab7 part2 evidence

ВКТУ · Есімханова Аружан Түсіпханқызы ·25-ИСТК-2о.

[PR #23](https://github.com/Aruzhaaan-06/devops-labs/pull/23) · [PDF на казахском](../../reports/lab07-alerts-report.pdf) · [сценарии, ответы и повторение](../../docs/lab07-alerts.md).

Реальный запуск24октября2026, APIlocal `lab14-7d78755`. ДатыUTC, местноеUTC+5. Никаких подставленных состояний или синтетических UI-скриншотов.

- `scenario-table.json`:6ожидаемых firing в5сценариях; observed pending/firing, server activeAt/lastEvaluation, точные delay/for. У ContainerRestarted pending отсутствует, for=0.
- `alerts-timeline.jsonl`:полные реальные rule snapshots приблизительно1раз/с. a–c сохранены с первого запуска; первоначальная d помечена `d-initial-premature-oom`; d–e взяты из успешного продолжения. Это не один непрерывный запуск процесса-наблюдателя; есть документированный перерыв.
- `a-errors.json`, `b-slow.json`, `c-crash.json`, `d-memory.json`, `e-down.json`:параметры, запросы/ответы/время, before/after, firing snapshots и PromQL.
- `*-logs.txt`:настоящие application logs каждого сценария. `docker-events.jsonl` — успешный d/e; `initial-attempt-docker-events.jsonl` — c и преждевременный OOM первой d.
- `initial-attempt-final.json`, `initial-attempt-phases.json`:неудачная фиксированная утечка80+100MiB, итоговый timeout ожидания high memory и восстановленный API. Ее нельзя считать успешной warning→OOM последовательностью.
- `initial-attempt-load-console.txt` и `load-console.txt`:два разных load проекта, включая ожидаемые transport ошибки при fault injection. Скрипты остановлены; это не1200безошибочных итераций из предыдущей работы.
- `business-counter.json`, `business-after-restarts.json`, `business-range.json`, `http-range.json`:счетчик1успешного persistence, отклоненные400/404, reset/restart, сравнение range. Во время фоновой нагрузки счетчики процессные, не строкиБД.
- `grafana-provisioned.json`, `dashboard-provisioning.json`:реальная загруженная Grafana спецификация, UIDdemo-api,7панелей, file targets совпали. Classic JSON редактировался непосредственно, UIэкспорт был недоступен из-за запрета Work.
- `polling-reload.json`:было5панелей, после исправления20s polling стало7; последующий description edit появился через19.429s без второго restart. Watch черезWindowsbind mount не сработал.
- `local-tests.json`:TRX summaries focused1/1 и InMemory40/40 без путей/имени машины. Полный PostgreSQLCI выполняется на PR/main.
- `postman-console.txt`, `postman-results.json`:реальный API/Prometheus,10запросов/17assertions/0failures/exit0; load остановлен,cloudPublished=false.
- `retained-data.json`, `final.json`:старые объекты10–12 и1200задач13сохранены; новые load задачи2231/531; ready/live200 и3UP после восстановления.
- `unchanged-config.json`:исходные application Compose, alerts/scrape и deploy workflow сохранены.

Скриншот3UP и4собственных PromQL изпервойчасти хранятся в `../lab07-metrics` и честно датированы в новом PDF. UIAdd/Export и визуальный просмотрGrafana/Dozzle в текущих сценариях не заявляются; сохранены эквивалентные API/CLIрезультаты.

После публикации соответствие новогоmain/runtime,40/40CI,файловыехеши и данных фиксируется отдельным asset`lab14-final-verification.json` вv1.0.0. Релизный тег и предыдущие12PDF не перезаписываются. Материал15 здесь не выполнен.
