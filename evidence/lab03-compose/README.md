# Docker Compose және деректердің өмірлік циклі — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 22 қазан, 06-материал. Compose API, PostgreSQL және қосымша Adminer қызметтерін біріктірген. Деректердің өмірлік циклі: 3 → 3 → 2. down томды сақтаған; down -v тек жеке оқу томын жойған. Жоюдан бұрын pg_dump -Fc және жеке demo_restore базасына қалпына келтіру орындалған; үш жоба табылған. Бұрынғы lab03 атаулы томы сақталған.

БД тоқтағанда live/ready/tasks: 200/503/500; БД қосылған соң API қайта іске қосылмай 200 қайтарған. service_healthy іске қосу ретін белгілейді, үздіксіз тәуелділік бақылауын жасамайды. API шегі: 1 CPU/256 MiB; swap жоқ, журнал 10m × 3, restart unless-stopped. PostgreSQL: 24/24 және 28/28; HTTP: 26; Postman: 24/73. Adminer-дің екі нақты суреті бар; ондағы 5 жоба/9 тапсырма Postman деректері қосылған кейінгі күйді көрсетеді. 14 техникалық тексеру өтті. Visual Studio/Test Explorer UI тармақтары ашық.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Каталог: [20261022T134617368Z-all-d2305b12](20261022T134617368Z-all-d2305b12/)

- Бастапқы журнал: [adminer-pull.txt](adminer-pull.txt)

- Бастапқы журнал: [adminer-start.txt](adminer-start.txt)

- Құрылымдық дерек: [adminer.json](adminer.json)

- Құрылымдық дерек: [api-health-database-stopped.json](api-health-database-stopped.json)

- Құрылымдық дерек: [backup-restore.json](backup-restore.json)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [compose-config-redacted.json](compose-config-redacted.json)

- Бастапқы журнал: [database-new-volume.txt](database-new-volume.txt)

- Құрылымдық дерек: [database-recovered-http.json](database-recovered-http.json)

- Құрылымдық дерек: [database-stopped-http.json](database-stopped-http.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [dns-db.txt](dns-db.txt)

- Бастапқы журнал: [down-volumes.txt](down-volumes.txt)

- Бастапқы журнал: [down.txt](down.txt)

- Құрылымдық дерек: [final-state.json](final-state.json)

- Каталог: [full-28](full-28/)

- Бастапқы журнал: [full-28-console.txt](full-28-console.txt)

- Бастапқы журнал: [gitignore-check.txt](gitignore-check.txt)

- Құрылымдық дерек: [healthy-services.json](healthy-services.json)

- Бастапқы журнал: [host-build.txt](host-build.txt)

- Бастапқы журнал: [host-development-console.txt](host-development-console.txt)

- Құрылымдық дерек: [host-development-http.json](host-development-http.json)

- Бастапқы журнал: [http-console.txt](http-console.txt)

- Құрылымдық дерек: [initial-projects.json](initial-projects.json)

- Құрылымдық дерек: [manual-command-count.json](manual-command-count.json)

- Құрылымдық дерек: [network-selection.json](network-selection.json)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Бастапқы журнал: [postman-exit-code.txt](postman-exit-code.txt)

- Құрылымдық дерек: [projects-after-down-volumes.json](projects-after-down-volumes.json)

- Құрылымдық дерек: [projects-after-down.json](projects-after-down.json)

- Құрылымдық дерек: [projects-before-down.json](projects-before-down.json)

- Каталог: [required-24](required-24/)

- Бастапқы журнал: [required-24-console.txt](required-24-console.txt)

- Бастапқы журнал: [restore-compose-api.txt](restore-compose-api.txt)

- Құрылымдық дерек: [runtime-configuration.json](runtime-configuration.json)

- Каталог: [screenshots](screenshots/)

- Бастапқы журнал: [services-logs.txt](services-logs.txt)

- Бастапқы журнал: [start-db.txt](start-db.txt)

- Бастапқы журнал: [stop-api-for-development.txt](stop-api-for-development.txt)

- Бастапқы журнал: [stop-db.txt](stop-db.txt)

- Бастапқы журнал: [stop-final.txt](stop-final.txt)

- Құрылымдық дерек: [three-counts.json](three-counts.json)

- Бастапқы журнал: [up-after-down.txt](up-after-down.txt)

- Бастапқы журнал: [up-after-volume-reset.txt](up-after-volume-reset.txt)

- Бастапқы журнал: [up-build.txt](up-build.txt)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](../../reports/lab03-compose-report.pdf)
- [Дәлел 2](../../docs/lab03-compose.md)
- [Дәлел 3](checks.json)
- [Дәлел 4](compose-config-redacted.json)
- [Дәлел 5](up-build.txt)
- [Дәлел 6](healthy-services.json)
- [Дәлел 7](manual-command-count.json)
- [Дәлел 8](network-selection.json)
- [Дәлел 9](backup-restore.json)
- [Дәлел 10](three-counts.json)
- [Дәлел 11](projects-before-down.json)
- [Дәлел 12](projects-after-down.json)
- [Дәлел 13](projects-after-down-volumes.json)
- [Дәлел 14](down.txt)
- [Дәлел 15](up-after-down.txt)
- [Дәлел 16](down-volumes.txt)
- [Дәлел 17](up-after-volume-reset.txt)
- [Дәлел 18](database-new-volume.txt)
- [Дәлел 19](dns-db.txt)
- [Дәлел 20](database-stopped-http.json)
- [Дәлел 21](stop-db.txt)
- [Дәлел 22](api-health-database-stopped.json)
- [Дәлел 23](start-db.txt)
- [Дәлел 24](database-recovered-http.json)
- [Дәлел 25](runtime-configuration.json)
- [Дәлел 26](gitignore-check.txt)
- [Дәлел 27](host-build.txt)
- [Дәлел 28](host-development-http.json)
- [Дәлел 29](host-development-console.txt)
- [Дәлел 30](restore-compose-api.txt)
- [Дәлел 31](required-24/summary.json)
- [Дәлел 32](required-24-console.txt)
- [Дәлел 33](full-28/summary.json)
- [Дәлел 34](full-28-console.txt)
- [Дәлел 35](20261022T134617368Z-all-d2305b12/http-evidence.json)
- [Дәлел 36](http-console.txt)
- [Дәлел 37](postman-console.txt)
- [Дәлел 38](postman-exit-code.txt)
- [Дәлел 39](adminer.json)
- [Дәлел 40](screenshots/adminer-projects.jpg)
- [Дәлел 41](screenshots/adminer-tasks.jpg)
- [Дәлел 42](services-logs.txt)
- [Дәлел 43](stop-final.txt)
- [Дәлел 44](final-state.json)

## Есеп және қабылдау шектері

[Есеп 3.3](../../reports/lab03-compose-report.pdf)

[Нұсқаулық](../../docs/lab03-compose.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
