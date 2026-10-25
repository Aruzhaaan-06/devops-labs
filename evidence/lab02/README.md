# Dockerfile және құрастыру кэші — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

2026 жылғы 22 қазан, 03-материал, 3-апта, 2-бақылау нүктесі. Docker 29.8.0, PowerShell 7.6.5, WSL 2 және 7,62 GiB жады расталған. Бірінші құрастыру мен код өзгергеннен кейінгі екінші құрастыру сақталған: restore — CACHED, COPY src және publish қайта орындалған.

Нақты Linux/amd64 контейнерінде 14 қосымша тексеру өтті. UID 1654; бейне көлемі 354 253 942 байт (337,8 MiB). Соңғы бейнеде SDK және C# бастапқы файлдары жоқ. live/ready — 200, Production Swagger — 404, Development Swagger — 200. InMemory stop/start нәтижесі: 1 → 0. HTTP: 26 сұрау; Postman: 24 сұрау/73 тексеру/0 қате; Release: 28/28. Жергілікті порттар: 8089 және 8090. Соңында оқу контейнерлері тоқтатылған. Settings → General ішіндегі WSL 2 суреті жоқ; пәрмен нәтижесі UI дәлелін алмастырмайды.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Каталог: [20261022T004046371Z-all-346370bd](20261022T004046371Z-all-346370bd/)

- Бастапқы журнал: [api-logs.txt](api-logs.txt)

- Бастапқы журнал: [base-history.txt](base-history.txt)

- Бастапқы журнал: [base-pull.txt](base-pull.txt)

- Құрылымдық дерек: [base-size.json](base-size.json)

- Бастапқы журнал: [build-first.txt](build-first.txt)

- Бастапқы журнал: [build-second.txt](build-second.txt)

- Құрылымдық дерек: [cache-change.json](cache-change.json)

- Құрылымдық дерек: [cache-check.json](cache-check.json)

- Құрылымдық дерек: [chaos-development.json](chaos-development.json)

- Оқиғалар тізбегі: [container-final-state.jsonl](container-final-state.jsonl)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Бастапқы журнал: [docker-version.txt](docker-version.txt)

- Бастапқы журнал: [dockerfile-check.txt](dockerfile-check.txt)

- Құрылымдық дерек: [environment.json](environment.json)

- Құрылымдық дерек: [health-http.json](health-http.json)

- Құрылымдық дерек: [health-production.json](health-production.json)

- Бастапқы журнал: [hello-world.txt](hello-world.txt)

- Бастапқы журнал: [http-check-console.txt](http-check-console.txt)

- Оқиғалар тізбегі: [image-sizes.jsonl](image-sizes.jsonl)

- Құрылымдық дерек: [image.json](image.json)

- Құрылымдық дерек: [openapi-development.json](openapi-development.json)

- Бастапқы журнал: [postman-console.txt](postman-console.txt)

- Бастапқы журнал: [postman-exit-code.txt](postman-exit-code.txt)

- Бастапқы журнал: [powershell-version.txt](powershell-version.txt)

- Құрылымдық дерек: [restart-after.json](restart-after.json)

- Құрылымдық дерек: [restart-before.json](restart-before.json)

- Құрылымдық дерек: [runtime-checks.json](runtime-checks.json)

- Бастапқы журнал: [runtime-files.txt](runtime-files.txt)

- Құрылымдық дерек: [swagger-development.json](swagger-development.json)

- Бастапқы журнал: [swagger-logs.txt](swagger-logs.txt)

- Құрылымдық дерек: [swagger-production.json](swagger-production.json)

- Каталог: [tests](tests/)

- Бастапқы журнал: [tests-console.txt](tests-console.txt)

- Бастапқы журнал: [wsl-distributions.txt](wsl-distributions.txt)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](docker-version.txt)
- [Дәлел 2](powershell-version.txt)
- [Дәлел 3](environment.json)
- [Дәлел 4](wsl-distributions.txt)
- [Дәлел 5](hello-world.txt)
- [Дәлел 6](base-pull.txt)
- [Дәлел 7](base-history.txt)
- [Дәлел 8](base-size.json)
- [Дәлел 9](../../Dockerfile)
- [Дәлел 10](../../.dockerignore)
- [Дәлел 11](dockerfile-check.txt)
- [Дәлел 12](build-first.txt)
- [Дәлел 13](build-second.txt)
- [Дәлел 14](cache-check.json)
- [Дәлел 15](runtime-checks.json)
- [Дәлел 16](image.json)
- [Дәлел 17](image-sizes.jsonl)
- [Дәлел 18](runtime-files.txt)
- [Дәлел 19](health-production.json)
- [Дәлел 20](health-http.json)
- [Дәлел 21](swagger-production.json)
- [Дәлел 22](swagger-development.json)
- [Дәлел 23](openapi-development.json)
- [Дәлел 24](chaos-development.json)
- [Дәлел 25](restart-before.json)
- [Дәлел 26](restart-after.json)
- [Дәлел 27](20261022T004046371Z-all-346370bd/http-evidence.json)
- [Дәлел 28](postman-console.txt)
- [Дәлел 29](postman-exit-code.txt)
- [Дәлел 30](tests/summary.json)
- [Дәлел 31](tests-console.txt)
- [Дәлел 32](container-final-state.jsonl)
- [Дәлел 33](api-logs.txt)
- [Дәлел 34](swagger-logs.txt)
- [Дәлел 35](../../reports/lab02-part1-report.pdf)
- [Дәлел 36](../../docs/lab02.md)
- [Дәлел 37](../../README.md)

## Есеп және қабылдау шектері

[Есеп 2.1](../../reports/lab02-part1-report.pdf)

[Нұсқаулық](../../docs/lab02.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
