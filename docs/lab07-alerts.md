# Материал 14: дашборд и алерты

ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

Лабораторная7, часть2, разделы5–7 и дополнение. [PR #23](https://github.com/Aruzhaaan-06/devops-labs/pull/23) · [казахский отчет](../reports/lab07-alerts-report.pdf) · [исходные доказательства](../evidence/lab07-alerts/README.md).

## Изменения

В Classic JSON `monitoring/grafana/dashboards/demo-api.json` добавлены панели **Tasks created per minute** (`increase` HTTP201 Tasks/Create за1m) и **Business tasks created per minute** (`increase(demo_tasks_created_total[1m])`). UID `demo-api`, папка DevOps course и прежние5панелей сохранены. Теперь7панелей.

`TaskService.CreateAsync` увеличивает `demo_tasks_created_total` только после успешного `tasks.CreateAsync`. Нет taskId/email лейблов, новых зависимостей или изменений HTTP-контракта. Счетчик сбрасывается при новом процессе, считает события сохранения, не все строки БД. HTTP201 может отличаться: persistence уже произошло, а сериализация/доставка ответа еще может не состояться; будущий не-HTTP вызов сервиса тоже посчитается. Такая ошибка доставки здесь намеренно не создавалась. В штатном пути показатели близки; raw и range сравнения сохранены.

Новый интеграционный тест проверяет экспортируемый `/metrics`: одна успешная задача +1,400/404 не увеличивают. Локально новый тест1/1, полный InMemory40/40. Обязательный PostgreSQL CI выполняет полный набор перед merge и при main deploy.

## Исправление file provisioning

Windows Docker Desktop показал настоящий сбой: JSON с7панелями виден в контейнере, а API Grafana все еще5панелей. Значение `updateIntervalSeconds` по умолчанию использует filesystem watch, события которого могут не пройти через bind mount. В provider установлен **20** (>10), чтобы включить polling, и перезапущена только Grafana. Затем новая description в файле появилась в API через **19.429с без второго restart**. [Результат](../evidence/lab07-alerts/polling-reload.json). Это следует [официальной документации](https://grafana.com/docs/grafana/latest/administration/provisioning/#detect-updates-to-provisioned-dashboards-files).

Панели внесены напрямую в Classic JSON и сверены с реальной загруженной Grafana спецификацией. Управление браузером в Work возвращало `Local browser use is disabled in Work settings`, в том числе после свежего подключения. Поэтому шаги Add/Export/Copy to clipboard в UI и визуальный просмотр Grafana/Dozzle во время каждого сбоя **не заявляются выполненными**. Сохранены API-ответы Grafana/Prometheus и настоящие Docker logs. В PDF включен честно датированный снимок3UP из материала13, а новый3UP подтвержден targets JSON/Postman. Файловые/терминальные права не использовались для обхода браузерного запрета.

## Реальные опыты a–e

Функциональная сборка7d78755, local tag `lab14-7d78755`, API256MiB, RAM+swap256MiB, unchanged unless-stopped. Основной Compose, alert rules, prometheus scrape config и CI/CD workflow не менялись. Нагрузка — исходный load.ps1 с пределом6000циклов на каждом запуске; эксперимент завершает только свой процесс. Ошибки при crash/stop/OOM сохранены, не засчитаны как успешные запросы.

| Сценарий | pending наблюдался UTC | firing наблюдался UTC | От старта опыта до firing |
|---|---|---|---|
| a · ApiHighErrorRate | 17:15:33.861 | 17:16:03.627 | 69.814с |
| b · ApiSlowRequests | 17:17:23.571 | 17:17:53.189 | 79.495с |
| c · ContainerRestarted | нет, for отсутствует | 17:18:24.770 | 15.925с |
| d · ContainerHighMemory | 17:28:55.460 | 17:29:09.804 | 34.372с |
| d · ContainerRestarted | нет, for отсутствует | 17:29:40.476 | 65.043с от начала d |
| e · ApiDown | 17:30:08.123 | 17:30:38.877 | 42.776с |

Дата24октября2026; местное время UTC+5. Это первые **наблюденные** состояния при poll≈1с, а не обещание точности субсекунд. Rule `activeAt`, `lastEvaluation` и периоды `for` сохранены в [scenario-table.json](../evidence/lab07-alerts/scenario-table.json); activeAt в этом запуске был на≈5с раньше первого наблюдения. Не подменять одно время другим.

- a:60реальных500, Error/InvalidOperationException; процесс жив, restart не было. После цикла дождались inactive.
- b:40последовательных slow1500ms,200, p95>1s; после цикла дождались inactive. Медленные запросы должны составлять достаточную долю общего трафика.
- c:202 → die1 → start → healthy; тот же ID, RestartCount0→1, Critical/startup. ApiDown в сохраненном c интервале inactive. После c дождались полного5m окна ContainerRestarted inactive.
- d первая попытка:80+100MiB привели к OOM до15s выдержки high memory. Первоначальный результат сохранен отдельно, wait завершился timeout, finally восстановил API/остановил своих наблюдателей. Он не представлен успешным high-memory опытом.
- d повтор: после нового inactive,80MiB затем20MiB шаги по **измеренному** working set до≥84%; ContainerHighMemory firing. Затем60MiB, oom/die137/start/healthy, RestartCount2→3, ContainerRestarted firing. Точные порции/проценты — d-memory.json. Исходные a–c не повторялись и не переписывались; их timeline объединен с новым d–e, первая неудачная d фаза помечена отдельно.
- e:stop толькоapi; дождались ApiDown firing, затемstart, ready/live200, healthy и ApiDown inactive. DB/monitoring не останавливались.

Логи a — server Error, b — без обязательного Error, c — Critical/startup, d — Docker OOM и новый startup, e — штатное завершение/новый startup. Эквивалентные панели: RPS500, p95, start-time/restart, working set/limit, API up. Raw данные/логи получены через CLI/API; автоматический визуальный просмотр этих UI был недоступен.

Контрольные объекты10–12 точно совпали после опытов; прежние1200InProgress задач13сохранены. Жүктеме-проекты30/32содержали2231/531сохраненную задачу при сверке; transport errors3/18оставлены в журналах. Это числа снимка после эксперимента, а не обещание полных успешных циклов. Учебные записи не удалены.

## Повторение

Нужны поднятые API/DB, monitoring с3UP, Docker Desktop Linux containers, PowerShell7, Python3. Полный запуск занимает минимум несколько минут ожидания: нельзя укорачивать окно5m ради результата. Только отдельный локальный стенд, не запускать одновременно с deploy.

```powershell
# .env содержит прежний DB_PASSWORD; не выводить его в журнал.
$env:API_IMAGE='devops-labs-demo-api'
$env:API_TAG='lab14-<выбранный-коммит>'
docker compose up -d --build --wait
docker compose -f monitoring/compose.yaml up -d
python scripts/verify-lab14.py --tag $env:API_TAG --output <new-directory>
# Лишь если первая попытка d OOMнулась слишком рано и a-c сохранены:
python scripts/verify-lab14.py --tag $env:API_TAG --output <another-new-directory> --resume-after-crash <prior-directory>
```

Скрипт проверяет фиксированное имя, образ/тег,256MiB/no-extra-swap/healthy и restart policy. `--resume-after-crash` переносит завершенные a–c и сохраняет первоначальную попытку с отдельной маркировкой. Существующий каталог не перезаписывается. Скрипт специально вызывает500,slow,exit1,OOM137 и stop; его finally только поднимает api и закрывает собственные subprocess. DB/Compose не меняются. Chaos включен исключительно в прежнем локальном стенде; в обычной конфигурации выключен.

После завершения нагрузки и восстановления:

```powershell
postman collection run postman/lab07-alerts.postman_collection.json --no-report-events
python scripts/check-lab14-evidence.py
```

Коллекция создает один проект/задачу, проверяет бизнес-счетчик до/после201/400/404, ready200,3UP,5здоровых rules и ApiDown inactive. Повторные запуски используют уникальное имя проекта. **10запросов/17assertions/0failures/exit0**, реальные API и Prometheus, без mock или облачной публикации. Не выполнять ее во время другой нагрузки: тест изменения счетчика требует отсутствия конкурентных созданий.

## Три ответа

1. Задержка до firing: ожидание scrape (5s), накопление достаточной доли плохих запросов в окне1m, evaluation(5s), выдержкаfor30s/15s и задержка наблюдения. Это не фиксированная сумма60s: rolling-окно уже содержит историю, а for сбрасывается при исчезновении условия.
2. При c авария короткая; API восстановился раньше непрерывных30s up=0. Poll журнала показал ApiDown inactive; очень короткую паузу scrape может вообще пропустить. ContainerRestarted фиксирует событие без for.
3. Slow200 излабы6п.9 теперь виден по latency histogram/p95 и алерту, хотя Docker healthy и Error-log нет. p95 по controller/action выделяет Chaos/Slow.

Ревью выполняется вторым аккаунтом того же владельца — не независимым напарником; local approval ассистент выполняет по поручению пользователя. После merge основной CI/CD и финальная сверка связывают main с runtime. `lab14-final-verification.json`, новый PDF и архив всех13отчетов публикуются отдельными assets в прежнем [v1.0.0](https://github.com/Aruzhaaan-06/devops-labs/releases/tag/v1.0.0), не меняя тег и прошлые assets. Материал15 еще не выполнялся; условия04 и старый ручной чек-лист остаются открытыми.

## Проверка после холодного запуска

При финальном main deploy обнаружено, что до первого создания задачи статический счётчик TaskService может ещё не зарегистрироваться в prometheus-net. Первоначальная коллекция требовала строку метрики заранее и завершилась ошибкой. Исправлена только начальная точка: отсутствие строки до первого события означает ноль. После успешного создания и после отклонённых 400/404 строка по-прежнему обязательна, а значение должно быть ровно initial+1. Это не заменяет отсутствующую метрику после записи нулём. Итоговый запуск выполняется на свежем процессе нового main; прежний неудачный результат сохраняется отдельно в финальной проверке релиза.
