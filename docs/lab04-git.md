# Лабораторная 4, часть 1 · материал 07 · Git и GitHub

**Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о · 22 октября 2026 года.**

[Репозиторий](https://github.com/Aruzhaaan-06/devops-labs) · [Доска](https://github.com/users/Aruzhaaan-06/projects/1) · [Отчет](../reports/lab04-git-report.pdf) · [Доказательства](../evidence/lab04-git/README.md).

Подготовка и технические действия разделов 1–6 выполнены в существующем публичном репозитории A. По решению владельца использованы два его аккаунта: Aruzhaaan-06 и temirkhanerbolatovich-coder. Это проверка механики GitHub; она не подтверждает работу с одногруппником и смену ролей в отдельном репозитории B. Преподаватель пока не приглашен, поскольку его GitHub-ник не предоставлен. Полная формальная сдача не объявляется завершенной.

## Подготовка и защита

Git, PowerShell 7, .NET 10 и GitHub CLI доступны; каталог `.github` учебного kit найден. Сервис уже опубликован предыдущими работами, поэтому повторная инициализация и новый репозиторий не создавались. GitHub CLI авторизован для обоих аккаунтов, второй получил write-доступ. Имена и email коммитов настроены локально; глобальная личность Git не менялась.

`.env`, bin, obj и .vs игнорируются; такие файлы не отслеживаются. Пароли и токены в отчет не включены. В публичном репозитории включено одобрение workflow всех внешних участников: `all_external_contributors`. Workflow CI в материале 07 еще не добавлялся.

Активный [ruleset main](https://github.com/Aruzhaaan-06/devops-labs/rules/25644144) применяется к default branch:

- Restrict deletions;
- Require a pull request before merging, Required approvals = 1;
- Block force pushes;
- bypass-список пуст, владелец также проходит через PR.

Проверочный пустой коммит с сообщением `test: direct push` создан через `git commit-tree HEAD^{tree} -p HEAD`. Такой коммит имеет тот же снимок файлов, что и main; рабочая ветка не передвигалась. Его push прямо в main отклонен с GH013 и `Changes must be made through a pull request`. Удалять локальный коммит через reset --hard не потребовалось. [Точный вывод](../evidence/lab04-git/direct-push-rejected.txt) сохранен; отдельного снимка окна терминала нет. Настоящие снимки ruleset включены в отчет.

## Три issue и Board

Созданы задачи:

1. [#1 — README с инструкцией запуска](https://github.com/Aruzhaaan-06/devops-labs/issues/1).
2. [#2 — шаблон Pull Request и Dependabot](https://github.com/Aruzhaaan-06/devops-labs/issues/2).
3. [#3 — переименование проекта](https://github.com/Aruzhaaan-06/devops-labs/issues/3).

Все три добавлены в публичный Board «DevOps Labs — лабораторная 4». После привязки PR #4 задача #1 перешла в In Progress; после squash-merge автоматически закрылась. При обновлении доски ее Status еще оставался In Progress. Для проверки включенного workflow Item closed ту же задачу повторно открыли и закрыли: она автоматически перешла в Done, без ручного изменения Status. Причина первоначальной задержки/порядка обработки событий не установлена. Все действия и снимок Done сохранены. #2 и #3 остаются Todo для следующей части лабораторной.

## README через ревью

[PR #4](https://github.com/Aruzhaaan-06/devops-labs/pull/4), ветка `docs/1-readme`, автор Aruzhaaan-06:

1. Коммит e1742a0 добавил команды Compose, .env, разработку с PostgreSQL и F5, возврат к InMemory. Основные маршруты и команды тестов уже были в README.
2. Для локального хранения конфигурации вне Git добавлен только `UserSecretsId` в csproj. Код API и бизнес-правила не менялись. Этот идентификатор не является секретом; `dotnet user-secrets` хранит значения локально, но не шифрует их.
3. temirkhanerbolatovich-coder оставил [комментарий к строке](https://github.com/Aruzhaaan-06/devops-labs/pull/4#discussion_r4349438594): Copy-Item мог перезаписать существующий .env при копировании блока команд.
4. Автор исправил это отдельным коммитом c1e3b46: `if (-not (Test-Path .env)) { Copy-Item .env.example .env }`. Реальное выполнение команды сохранило существующий файл без изменений.
5. Второй аккаунт одобрил исправленный SHA, владелец выполнил Squash and merge. Issue #1 автоматически закрыт через `Closes #1`.

Сборка `dotnet build DemoApi.slnx --no-restore --nologo` успешна, 0 предупреждений и ошибок. F5 в Visual Studio не проверялся; инструкция подготовлена. Полные API-тесты в этой работе повторно не запускались: изменения затрагивают документацию и идентификатор локальной конфигурации. Результаты API-тестов относятся к предыдущему материалу 06.

## Настоящий конфликт первой строки

Обе ветки созданы от b80b32f, из двух разных локальных копий:

| Ветка / PR | Аккаунт | Заголовок |
|---|---|---|
| docs/title-a · [#5](https://github.com/Aruzhaaan-06/devops-labs/pull/5) | Aruzhaaan-06 | DevOps Labs — DemoApi: сервис задач |
| docs/title-b · [#6](https://github.com/Aruzhaaan-06/devops-labs/pull/6) | temirkhanerbolatovich-coder | DevOps Labs — проекты и задачи |

После ревью и squash-merge #5 GitHub показал для #6 `This branch has conflicts that must be resolved`, API вернул mergeable=false / dirty. В копии второго аккаунта:

```powershell
git fetch origin
git merge origin/main
# CONFLICT (content): Merge conflict in README.md
# Оставлен общий заголовок: DevOps Labs — DemoApi: проекты и задачи
git add README.md
git commit -m "docs: resolve title conflict"
git push
```

Коммит **02d593b** имеет двух родителей, автор — второй аккаунт. Он прошел ревью владельца и попал в main через merge commit PR #6, поэтому сохранен в истории. `git merge-base --is-ancestor 02d593b HEAD` успешен. [Вывод git log --oneline --graph](../evidence/lab04-git/git-log-graph.txt) включен в отчет. Запрет force-push и обязательное ревью не отключались.

## Что остается для формальной сдачи

- Добавить преподавателя в collaborators, когда будет известен его GitHub-ник.
- Согласовать с преподавателем замену работы с одногруппником двумя аккаунтами одного владельца; отдельный этап в репозитории B не проводился.
- При буквальном требовании скриншота отклоненного push приложить снимок терминала: сейчас сохранен точный вывод команды.

Технический сценарий репозитория A подтвержден 13 проверками. Все изменения после включения защиты публикуются через PR. Следующий материал 08 использует оставшиеся issue; шаблоны, Dependabot, изменение API и релиз здесь еще не выполнялись.

Справка: [правила GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [локальный User Secrets в ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets?view=aspnetcore-10.0).
