namespace DemoApi.Domain;

/// <summary>Проект</summary>
/// <param name="Id">Идентификатор</param>
/// <param name="Name">Название, уникальное</param>
/// <param name="CreatedAt">Когда создан</param>
public sealed record Project(int Id, string Name, DateTimeOffset CreatedAt);

/// <summary>Количество задач проекта по статусам и срокам.</summary>
/// <param name="ProjectId">Идентификатор проекта</param>
/// <param name="Total">Всего задач</param>
/// <param name="Todo">Задачи в статусе Todo</param>
/// <param name="InProgress">Задачи в статусе InProgress</param>
/// <param name="Done">Задачи в статусе Done</param>
/// <param name="Overdue">Незавершённые задачи со сроком раньше текущей даты UTC</param>
public sealed record ProjectStats(int ProjectId, int Total, int Todo, int InProgress, int Done, int Overdue);
