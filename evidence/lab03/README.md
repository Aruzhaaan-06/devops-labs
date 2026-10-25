# Сервиске арналған PostgreSQL — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 22 қазан, 05-материал, 3-зертханалық жұмыстың 1–2-бөлімдері. Нақты PostgreSQL 18.6, postgres:18-alpine. Алғашқы seed: 2 жоба/4 тапсырма; бесінші тапсырма қосылған соң сол атаулы томмен контейнерді қайта жасағанда 5 тапсырма сақталған. Жаңа анонимді томда notes кестесі жоқ; бұрынғы анонимді том автоматты қосылмайды. PostgreSQL 18 томы /var/lib/postgresql жолына жалғанған.

Windows API: 8091; контейнер API: 8092; БД: localhost:15432. Windows жобасы id=3, контейнер жобасы id=4 қайта іске қосылғанда сақталған. Жеке demo_tests базасында міндетті 24/24 (7+17), толық 28/28 (7+21). Сүзгі төрт қосымша DueDate жағдайын бөледі; тест саны өзгертіліп көрсетілмеген. HTTP: 26 сұрау; Postman: 24/73/0.

Алғашқы контейнерде ConnectionStrings__Db жоқ; келесісінде Host=localhost API контейнерінің өзіне бағытталған. DNS атауы бар ортақ желіде ready=200. Стандартты пул таусылғандықтан тексерілген 10.254.53.0/24 желісі қолданылған. Соңында API/БД тоқтатылған, атаулы том сақталған. Windows процесі dotnet арқылы іске қосылған; F5 және Visual Studio/Test Explorer суреттері расталмаған. CP866 журналы мазмұны сақталып UTF-8 пішіміне ауыстырылған; жеке жолдар жасырылған.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Каталог: [20261022T005458521Z-all-3eba0a05](20261022T005458521Z-all-3eba0a05/)

- Бастапқы журнал: [api-build.txt](api-build.txt)

- Құрылымдық дерек: [api-health.json](api-health.json)

- Бастапқы журнал: [api-postgres-logs.txt](api-postgres-logs.txt)

- Құрылымдық дерек: [api-ready.json](api-ready.json)

- Құрылымдық дерек: [attempt-localhost.json](attempt-localhost.json)

- Бастапқы журнал: [attempt-localhost.txt](attempt-localhost.txt)

- Құрылымдық дерек: [attempt-missing.json](attempt-missing.json)

- Бастапқы журнал: [attempt-missing.txt](attempt-missing.txt)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [container-after-restart.json](container-after-restart.json)

- Құрылымдық дерек: [container-before-restart.json](container-before-restart.json)

- Бастапқы журнал: [database-final-logs.txt](database-final-logs.txt)

- Бастапқы журнал: [database-first-start.txt](database-first-start.txt)

- Құрылымдық дерек: [database-image.json](database-image.json)

- Бастапқы журнал: [database-recreated.txt](database-recreated.txt)

- Құрылымдық дерек: [database-version.json](database-version.json)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [docker-dns.txt](docker-dns.txt)

- Оқиғалар тізбегі: [final-containers.jsonl](final-containers.jsonl)

- Каталог: [full-28](full-28/)

- Бастапқы журнал: [full-28-console.txt](full-28-console.txt)

- Құрылымдық дерек: [host-after-restart.json](host-after-restart.json)

- Құрылымдық дерек: [host-before-restart.json](host-before-restart.json)

- Бастапқы журнал: [host-build.txt](host-build.txt)

- Бастапқы журнал: [host-first-start.txt](host-first-start.txt)

- Бастапқы журнал: [host-second-start.txt](host-second-start.txt)

- Құрылымдық дерек: [host-seed-projects.json](host-seed-projects.json)

- Бастапқы журнал: [http-console.txt](http-console.txt)

- Құрылымдық дерек: [kit-check.json](kit-check.json)

- Құрылымдық дерек: [network-selection.json](network-selection.json)

- Бастапқы журнал: [postgres-pull.txt](postgres-pull.txt)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Бастапқы журнал: [postman-exit-code.txt](postman-exit-code.txt)

- Каталог: [required-24](required-24/)

- Бастапқы журнал: [required-24-console.txt](required-24-console.txt)

- Құрылымдық дерек: [retained-volume.json](retained-volume.json)

- Каталог: [screenshots](screenshots/)

- Құрылымдық дерек: [seed-data.json](seed-data.json)

- Құрылымдық дерек: [sql-stats.json](sql-stats.json)

- Бастапқы журнал: [tests-database-proof.txt](tests-database-proof.txt)

- Құрылымдық дерек: [volume-after-recreate.json](volume-after-recreate.json)

- Құрылымдық дерек: [volume-insert.json](volume-insert.json)

- Құрылымдық дерек: [without-named-volume.json](without-named-volume.json)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](checks.json)
- [Дәлел 2](../../reports/lab03-postgres-report.pdf)
- [Дәлел 3](../../docs/lab03-postgres.md)
- [Дәлел 4](kit-check.json)
- [Дәлел 5](postgres-pull.txt)
- [Дәлел 6](database-image.json)
- [Дәлел 7](database-version.json)
- [Дәлел 8](without-named-volume.json)
- [Дәлел 9](database-first-start.txt)
- [Дәлел 10](seed-data.json)
- [Дәлел 11](volume-insert.json)
- [Дәлел 12](volume-after-recreate.json)
- [Дәлел 13](database-recreated.txt)
- [Дәлел 14](host-build.txt)
- [Дәлел 15](host-first-start.txt)
- [Дәлел 16](host-second-start.txt)
- [Дәлел 17](host-seed-projects.json)
- [Дәлел 18](host-before-restart.json)
- [Дәлел 19](host-after-restart.json)
- [Дәлел 20](screenshots/swagger-postgres-projects.jpg)
- [Дәлел 21](required-24/summary.json)
- [Дәлел 22](required-24-console.txt)
- [Дәлел 23](full-28/summary.json)
- [Дәлел 24](full-28-console.txt)
- [Дәлел 25](tests-database-proof.txt)
- [Дәлел 26](sql-stats.json)
- [Дәлел 27](api-build.txt)
- [Дәлел 28](attempt-missing.json)
- [Дәлел 29](attempt-missing.txt)
- [Дәлел 30](attempt-localhost.json)
- [Дәлел 31](attempt-localhost.txt)
- [Дәлел 32](network-selection.json)
- [Дәлел 33](docker-dns.txt)
- [Дәлел 34](api-health.json)
- [Дәлел 35](api-ready.json)
- [Дәлел 36](api-postgres-logs.txt)
- [Дәлел 37](container-before-restart.json)
- [Дәлел 38](container-after-restart.json)
- [Дәлел 39](20261022T005458521Z-all-3eba0a05/http-evidence.json)
- [Дәлел 40](postman-console.txt)
- [Дәлел 41](postman-exit-code.txt)
- [Дәлел 42](final-containers.jsonl)
- [Дәлел 43](retained-volume.json)
- [Дәлел 44](database-final-logs.txt)
- [Дәлел 45](../lab03-compose/README.md)
- [Дәлел 46](../../reports/README.md)
- [Дәлел 47](../../README.md)

## Есеп және қабылдау шектері

[Есеп 3.1-3.2](../../reports/lab03-postgres-report.pdf)

[Нұсқаулық](../../docs/lab03-postgres.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
