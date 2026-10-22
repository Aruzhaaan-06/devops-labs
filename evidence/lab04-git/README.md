# Материал 07 · Git / GitHub · доказательства

22 октября 2026 года. [13 технических проверок и ограничения](checks.json) · [Отчет](../../reports/lab04-git-report.pdf) · [Подробное описание](../../docs/lab04-git.md).

| Проверка | Фактические материалы |
|---|---|
| Подготовка, инструменты, kit | [Окружение](environment.json), [игнорирование файлов](ignored-files.txt) |
| Второй аккаунт с write | [Приглашение](partner-invitation.json), [доступ подтвержден](partner-invitation-accepted.json) |
| main: active, 1 approval, deletion/force-push запрещены | [Ruleset](main-ruleset.json), [снимок настройки](screenshots/main-ruleset.jpg), [публичное представление](screenshots/main-ruleset-public.jpg) |
| Прямой push отклонен | [GH013, точный вывод](direct-push-rejected.txt), [SHA и неизменность main](direct-push-check.json) |
| Actions: все внешние workflow требуют одобрения | [До](fork-workflow-approval-before.json), [после](fork-workflow-approval.json) |
| Три issue | [Список](issues.json), [исходная доска](screenshots/board-three-issues.jpg) |
| Board и workflow Item closed | [Финальные статусы](board-final.json), [workflow включен](screenshots/item-closed-done.jpg), [Done](screenshots/board-readme-done.jpg), [повторная проверка события закрытия](board-workflow-recheck.json) |
| README PR #4 | [Создание PR](readme-pr.json), [комментарий](readme-review-comment.json), [inline-текст](readme-inline-comments.json), [Approve](readme-review-approved.json), [squash](readme-merge.json), [автозакрытие #1](issue-1-closed.json), [финал PR](pr-4-final.json) |
| Сборка и сохранение .env | [Успешный результат](build-summary.json) |
| Конфликт двух веток | [Общий base](conflict-common-base.json), [GitHub dirty](github-conflicting-pr.json), [ошибка merge](merge-conflict.txt), [маркеры](readme-conflict-fragment.txt), [настоящий снимок PR #6](screenshots/pr6-conflict.jpg) |
| Разрешение и сохранение истории | [Два родителя коммита](conflict-resolution.json), [git log --oneline --graph](git-log-graph.txt), [слияние A](title-a-merge.json), [слияние B](title-b-merge.json), [финал #5](pr-5-final.json), [финал #6](pr-6-final.json) |

При squash-merge #4 issue #1 закрылся автоматически, но Status на доске оставался In Progress после обновления. Повторное открытие/закрытие той же задачи подтвердило автоматический Done через Item closed; Status вручную не редактировался. Первоначальная причина не установлена.

Два аккаунта принадлежат одному владельцу; это явно указано в PR и отчете. Работа с одногруппником и второй отдельный репозиторий B не подтверждены. Преподаватель не добавлен: ник пока неизвестен. Для отклоненного push сохранен текст вместо снимка терминала. F5 в Visual Studio не проверялся. Формальная готовность к сдаче остается частичной, несмотря на выполненный технический сценарий A.

Секреты не публикуются. Проверочный пустой commit-tree не передвигал рабочую ветку; отвергнутый коммит не попал в main. Реальные текстовые журналы нормализованы в UTF-8, конечные пробелы удалены; снимки интерфейса не изменялись.
