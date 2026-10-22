# Лабораторная 2 · Docker · часть 1

**Есімханова Аружан Түсіпханқызы · 25-ИСТК-2о**

Материал 03 относится к неделе 3, контрольной точке 2: разделы 1–5 лабораторной 2. В полученном архиве есть первая часть; отдельного материала 04 с продолжением нет.

Состояние проекта для этой работы сохраняет [тег lab02-docker](https://github.com/Aruzhaaan-06/devops-labs/tree/lab02-docker).

## Требования сдачи

Один отчет PDF/DOCX с ФИО, группой, номером задания, подписями результатов и кликабельными ссылками на GitHub. В нем требуются:

1. Dockerfile и `.dockerignore` полностью текстом.
2. Вывод второй сборки после изменения сообщения журнала в `TaskService.cs`: шаг `dotnet restore` должен иметь `CACHED`.
3. Настоящий скриншот Docker Desktop → Settings → General с включенным `Use the WSL 2 based engine`.

Подготовка включает Docker Desktop с Linux-контейнерами на WSL 2, не менее 4 ГБ памяти Docker и PowerShell 7. Команды проверки: `docker version`, `docker run --rm hello-world`, `pwsh --version`. Базовый образ `mcr.microsoft.com/dotnet/aspnet:10.0` нужно скачать и изучить командами `docker image ls` и `docker image history`.

## Сборка и проверка кэша

Команды выполняются из корня репозитория. Для совместной работы с другими проектами локальные образы и контейнеры используют префикс `devops-labs`.

```powershell
docker build --progress=plain -t devops-labs-demo-api:lab02-1.0 .
# Измените текст сообщения лога в src/DemoApi/Services/TaskService.cs.
docker build --progress=plain --build-arg APP_VERSION=lab02-1.1 -t devops-labs-demo-api:lab02-1.1 .
docker image ls devops-labs-demo-api
docker image history mcr.microsoft.com/dotnet/aspnet:10.0
```

Вторую сборку выполняют после изменения содержимого C#-файла. Простого изменения времени файла недостаточно. В репозитории эта учебная правка сохранена в сообщении создания задачи. Для повторения эксперимента можно снова изменить только текст этого сообщения.

Файл проекта копируется до исходников. Поэтому изменение C#-кода пересобирает `COPY src/` и `dotnet publish`, но сохраняет кэш `dotnet restore`, пока файл проекта, базовый образ и предшествующие слои не меняются. Подробности: [правила кэша Docker](https://docs.docker.com/build/cache/invalidation/).

## Устройство образа

[Dockerfile](../Dockerfile) содержит два этапа. SDK 10.0 восстанавливает зависимости и публикует приложение Release в `/app`. Итоговый этап использует ASP.NET runtime 10.0 и получает только результат публикации. В нем установлен curl для `HEALTHCHECK`; списки apt удаляются в том же слое.

`ARG APP_VERSION=dev` задает версию при сборке, `ENV APP_VERSION` передает ее приложению, а `GET /` показывает выбранное значение. Это публичная версия сборки; секреты через ARG/ENV не передаются.

`USER $APP_UID` запускает приложение от встроенного пользователя `app`, а не root. `EXPOSE 8080` описывает внутренний порт. Healthcheck каждые 10 секунд обращается к `/health/live`, с тайм-аутом 3 секунды, стартовым периодом 15 секунд и тремя попытками. Главный процесс задается `ENTRYPOINT ["dotnet", "DemoApi.dll"]`.

[.dockerignore](../.dockerignore) исключает локальные bin/obj, тестовые результаты, историю Git, IDE, отчеты, доказательства, документацию, тесты и вспомогательные файлы. Дополнительно исключены `.env`/`.env.*` во вложенных каталогах и файлы сертификатов. Эти материалы не нужны для публикации приложения. Описание multi-stage: [Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/docker/building-net-docker-images?view=aspnetcore-10.0).

Теги базовых образов `10.0` обновляются поставщиком. Журнал сборки фиксирует фактически использованные digest; повторная сборка позднее может скачать другую патч-версию.

## Проверка контейнера

Дополнительно к разделам 1–5 проверяется работа собранного приложения. Свободный порт Windows 8089 направляется на порт 8080 контейнера; публикация ограничена localhost. Порт 8080 Windows в исходной среде занят Oracle, а 8088 используется для запуска первой лабораторной.

```powershell
docker run -d --name devops-labs-lab02-api -p 127.0.0.1:8089:8080 -e Storage=InMemory devops-labs-demo-api:lab02-1.1
docker inspect --format '{{.State.Health.Status}}' devops-labs-lab02-api
Invoke-RestMethod http://localhost:8089/
Invoke-RestMethod http://localhost:8089/health/live
docker logs devops-labs-lab02-api
docker exec devops-labs-lab02-api id
docker exec devops-labs-lab02-api dotnet --list-sdks
pwsh -File scripts/verify-lab01.ps1 -Phase All -BaseUrl http://localhost:8089 -EvidenceDirectory evidence/lab02 -IncludePastDueValidation
```

По умолчанию окружение Production, поэтому Swagger отсутствует. Для локальной демонстрации можно запустить отдельный контейнер без пересборки:

```powershell
docker run -d --name devops-labs-lab02-swagger -p 127.0.0.1:8090:8080 -e Storage=InMemory -e ASPNETCORE_ENVIRONMENT=Development -e Chaos__Enabled=false devops-labs-demo-api:lab02-1.1
```

Swagger доступен по адресу `http://localhost:8090/swagger`. В Development исходная настройка включает учебные сбои, поэтому команда явно отключает их через `Chaos__Enabled=false`.

Проверка жизненного цикла: создать проект через POST, убедиться, что он есть, выполнить `docker stop devops-labs-lab02-api`, затем `docker start devops-labs-lab02-api` и снова получить список. InMemory после нового запуска процесса пуст; файловый слой контейнера этого не меняет.

По завершении демонстрации остановите только учебные контейнеры:

```powershell
docker stop devops-labs-lab02-api devops-labs-lab02-swagger
```

## Ответы на вопросы лекции

1. **Почему контейнер стартует быстрее VM?** Ему не нужно загружать отдельное ядро и полноценную ОС: ядро Linux уже работает в WSL 2. Docker создает изоляцию процесса и монтирует готовые слои.
2. **Почему сначала копируется csproj?** Он меняется реже исходников. Зависимости восстанавливаются в отдельном слое, который можно повторно использовать после изменения кода.
3. **Что остается после multi-stage?** Итоговый образ содержит runtime, опубликованные DLL, зависимости приложения, конфигурацию и curl. SDK, исходники и промежуточные obj остаются на этапе build.
4. **Почему нет Swagger и как включить?** В `Program.cs` маршруты Swagger/OpenAPI регистрируются только в Development. Переменная `ASPNETCORE_ENVIRONMENT=Development` при создании контейнера включает их без пересборки; для учебного просмотра также отключаются Chaos-endpoints.
5. **Что происходит с проектами после stop/start?** Остановка завершает процесс и уничтожает его оперативную память. Тот же контейнер стартует с новым процессом и пустым InMemoryStore. Для сохранения данных нужна база; это следующая лабораторная.

[Результаты выполнения](../evidence/lab02/README.md) · [Каталог отчетов](../reports/README.md) · [Список работ](README.md)
