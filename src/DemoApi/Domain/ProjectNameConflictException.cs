namespace DemoApi.Domain;

/// <summary>Имя проекта уже занято; включая конфликт конкурентных изменений.</summary>
public sealed class ProjectNameConflictException : Exception
{
    public ProjectNameConflictException() : base("Имя проекта уже занято.") { }
}
