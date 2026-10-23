# 11-материалдың нақты дәлелдері

**ВКТУ · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 2026-10-23**

[35 шарт сәтті](checks.json), қате 0. 1-5-тармақтар, сценарийлер 2-5, тапсырудағы сұрақтар 1-2 орындалды. OOM, ready/БД және unhealthy тәжірибелері бұл жинақта жасалған жоқ.

| Дәлел | Файл |
|---|---|
| Бастапқы healthy, restart, log rotation, ресурстар, ENTRYPOINT | [initial-inspection.json](initial-inspection.json) |
| Бақылау жобасы мен тапсырмасы | [marker.json](marker.json) |
| T1: пәрмендер және HTTP жауаптары | [t1-commands.txt](t1-commands.txt) |
| T2: үздіксіз сүзілген оқиғалар | [t2-events.jsonl](t2-events.jsonl), [stderr бос](t2-stderr.txt) |
| T3: қатар орындалған ресурс өлшемдері | [t3-stats.jsonl](t3-stats.jsonl), [25 топтама/24 API үлгісі](resource-summary.json) |
| Арналардың нақты іске қосылу режимі | [observation-streams.json](observation-streams.json) |
| 2: HTTP 500, процесс тірі | [before/after, HTTP, events](scenario-2-request-error.json), [Error және толық стек](scenario-2-request-error-logs.txt) |
| 3: exit1 және авторестарт | [before/after, die → start → healthy](scenario-3-auto-restart.json), [Critical және startup](scenario-3-auto-restart-logs.txt) |
| 4: restart no, Exited(1) | [күй, ps -a және die1](scenario-4-no-restart.json), [Critical](scenario-4-no-restart-logs.txt) |
| no параметрін қайтару | [unless-stopped және сақталған жоба/тапсырма](restored-after-no.json) |
| 5: graceful shutdown | [SIGTERM15, stop, die0](scenario-5-graceful-stop.json), [Information log](scenario-5-graceful-stop-logs.txt) |
| start-тен кейінгі healthy және деректер | [final-local.json](final-local.json) |
| Compose бастапқы байттары және SHA-256 | [compose-restored.json](compose-restored.json) |
| Docker Desktop қойындылары | [Пайдаланушының растауы](docker-desktop-inspection.json); ассистент суреті жоқ |
| Нақты Postman | [4 сұрау / 10 assertion / exit0](postman-results.json), [толық CLI шығысы](postman-failure-checks.txt) |
| Әдістеме және ресми анықтамалар | [source-references.json](source-references.json) |

Үш CLI арнасы параллель орындалды; үш бөлек көрінетін терминалдың суреті ретінде көрсетілмейді. T3 жаңа контейнер ID-лерін табу үшін `stats --no-stream` пәрменін қайталады. Контейнер қайта жасалған аралықта бір stats өлшемі exit1/EOF берді; қате мен уақыты толық JSONL және resource-summary ішінде сақталған, келесі өлшемдер жалғасты. T2-де healthcheck exec_* оқиғалары сүзілді. JSON файлдарындағы scenario уақыттары толық T2 ағынындағы дәл сол аралыққа сәйкес келеді; Compose recreation оқиғалары басқа аралықтарда сақталған.

Штаттық stop кезінде нақты жеткізілген рет: kill(signal15) → stop → die(exit0). Бұл рет өзгертілмеді. HTTP 500 процестің exit code-ы емес; 2-де lifecycle аяқталуы болған жоқ. 3-де қайта іске қосылған State.ExitCode=0 бұрынғы exit1-ді жоққа шығармайды: ол die оқиғасында сақталған.

Негізгі src/tests/Dockerfile және тұрақты Compose мінез-құлқы өзгертілмеді. Crash пен stop тек оқу API контейнеріне бағытталды; DB томы жойылған жоқ. DB_PASSWORD, Config.Env және runner credential файлдары жарияланбады. Postman CLI соңындағы login ескертуі cloud-қа жариялауға қатысты; жергілікті 4/10 тексеруі exit0-мен аяқталды.

[Қазақша PDF](../../reports/lab06-failures-report.pdf) · [Тәртібі және екі жауап](../../docs/lab06-failures.md) · [Офлайн тексеру скрипті](../../scripts/check-lab11-evidence.py)
