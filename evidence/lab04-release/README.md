# GitHub ережелері және шығарылым — орындалу дәлелдері

Д. Серікбаев атындағы Шығыс Қазақстан техникалық университеті · Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о.

08-материал: PUT /api/projects/{id}, 200/400/404/409; бір атауды қайталау рұқсат етілген. Екі сақтау нұсқасында RenameAsync, SQL параметрлері және бәсекелес атау қақтығысы тексерілген. Жоба ID, createdAt және тапсырмалар сақталған. Жеке demo_lab08_tests базасында және InMemory режимінде 38/38; Postman: 37 сұрау/99 тексеру. Екі параллель сұрауда біреуі 200, екіншісі 409; апострофы бар атау дәл мәтін ретінде сақталған.

Ревью ескертуі 9b1780b коммитімен түзетілген. v0.1.0 және Done/PR/release нақты суреттері бар. 19 техникалық тексеру расталған. CI келесі 09-материалға жатады; қолмен жарияланған мәртебе CI ретінде көрсетілмейді. Оқытушы, жұп және B репозиторийі бойынша шектеулер сақталған.

## Дәлел файлдары

Төмендегі файл атаулары — өзгертілмеген техникалық идентификаторлар. JSON/TXT/JSONL ішіндегі нақты сұраулар, жауаптар, уақыттар, қателер және хэштер аударылмайды. Бұл каталогқа сілтемелерді қазақшалау бұрынғы тәжірибені қайта орындау немесе жетіспейтін суретті толықтыру болып саналмайды.

- Бастапқы журнал: [board-done-ui.txt](board-done-ui.txt)

- Құрылымдық дерек: [checks.json](checks.json)

- Құрылымдық дерек: [codeowner-auto-request.json](codeowner-auto-request.json)

- Құрылымдық дерек: [codeowners-errors.json](codeowners-errors.json)

- Бастапқы журнал: [compose-build.txt](compose-build.txt)

- Құрылымдық дерек: [config-merge.json](config-merge.json)

- Құрылымдық дерек: [config-pr.json](config-pr.json)

- Құрылымдық дерек: [config-review.json](config-review.json)

- Құрылымдық дерек: [containers-final.json](containers-final.json)

- Бастапқы журнал: [containers-final.txt](containers-final.txt)

- Бастапқы журнал: [containers-stop.txt](containers-stop.txt)

- Құрылымдық дерек: [deliverables.json](deliverables.json)

- Құрылымдық дерек: [dependabot-prs.json](dependabot-prs.json)

- Құрылымдық дерек: [inline-comments-final.json](inline-comments-final.json)

- Құрылымдық дерек: [inmemory-tests.json](inmemory-tests.json)

- Бастапқы журнал: [inmemory-tests.txt](inmemory-tests.txt)

- Құрылымдық дерек: [issues-final.json](issues-final.json)

- Құрылымдық дерек: [live-http.json](live-http.json)

- Құрылымдық дерек: [manual-status.json](manual-status.json)

- Бастапқы журнал: [openapi-container-start.txt](openapi-container-start.txt)

- Бастапқы журнал: [openapi-container-stop.txt](openapi-container-stop.txt)

- Құрылымдық дерек: [openapi-rename.json](openapi-rename.json)

- Құрылымдық дерек: [postgres-tests.json](postgres-tests.json)

- Бастапқы журнал: [postgres-tests.txt](postgres-tests.txt)

- Бастапқы журнал: [postman-export-unavailable.txt](postman-export-unavailable.txt)

- Бастапқы журнал: [postman-full-run.txt](postman-full-run.txt)

- Құрылымдық дерек: [release-verification.json](release-verification.json)

- Құрылымдық дерек: [release.json](release.json)

- Құрылымдық дерек: [rename-final-review.json](rename-final-review.json)

- Құрылымдық дерек: [rename-merge.json](rename-merge.json)

- Құрылымдық дерек: [rename-pr.json](rename-pr.json)

- Құрылымдық дерек: [ruleset-codeowners.json](ruleset-codeowners.json)

- Құрылымдық дерек: [ruleset-final.json](ruleset-final.json)

- Каталог: [screenshots](screenshots/)

- Бастапқы журнал: [test-db-check.txt](test-db-check.txt)

- Бастапқы журнал: [test-db-create.txt](test-db-create.txt)

- Бастапқы журнал: [tested-commit.txt](tested-commit.txt)

## Нақты нәтижелерге бұрын берілген сілтемелер

- [Дәлел 1](../../reports/lab04-release-report.pdf)
- [Дәлел 2](../../docs/lab04-release.md)
- [Дәлел 3](checks.json)
- [Дәлел 4](inmemory-tests.json)
- [Дәлел 5](inmemory-tests.txt)
- [Дәлел 6](postgres-tests.json)
- [Дәлел 7](postgres-tests.txt)
- [Дәлел 8](postman-full-run.txt)
- [Дәлел 9](live-http.json)
- [Дәлел 10](compose-build.txt)
- [Дәлел 11](openapi-rename.json)
- [Дәлел 12](config-pr.json)
- [Дәлел 13](config-review.json)
- [Дәлел 14](rename-pr.json)
- [Дәлел 15](inline-comments-final.json)
- [Дәлел 16](rename-final-review.json)
- [Дәлел 17](issues-final.json)
- [Дәлел 18](screenshots/board-done.jpg)
- [Дәлел 19](board-done-ui.txt)
- [Дәлел 20](codeowner-auto-request.json)
- [Дәлел 21](ruleset-final.json)
- [Дәлел 22](codeowners-errors.json)
- [Дәлел 23](dependabot-prs.json)
- [Дәлел 24](release.json)
- [Дәлел 25](release-verification.json)
- [Дәлел 26](deliverables.json)
- [Дәлел 27](postman-export-unavailable.txt)

## Есеп және қабылдау шектері

[Есеп 4.2](../../reports/lab04-release-report.pdf)

[Нұсқаулық](../../docs/lab04-release.md) · [Тапсырудың ашық тармақтары](../../docs/REPORT_COMPLETENESS.md) · [Барлық есептер](../../reports/README.md).

Postman нәтижелері жергілікті тексеруден алынған; оларды бұл аударма бұлтқа жарияламайды. Екі ревью аккаунты бір иеге тиесілі. Кейінгі PDF рәсімдеуі бұрынғы checks/deliverables файлдарындағы тарихи бет саны мен хэшті алмастырмайды; түпнұсқа PDF Git тарихында сақталған.
