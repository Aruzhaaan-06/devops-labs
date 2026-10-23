using System.ComponentModel.DataAnnotations;
using DemoApi.Domain;
using DemoApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace DemoApi.Controllers;

/// <summary>Операции с проектами.</summary>
[ApiController]
[Route("api/projects")]
[Produces("application/json")]
[Tags("Проекты")]
public sealed class ProjectsController(ProjectService projects) : ControllerBase
{
    /// <summary>Список проектов</summary>
    /// <response code="200">Все проекты по порядку создания</response>
    [HttpGet]
    public Task<IReadOnlyList<Project>> List(CancellationToken ct) => projects.ListAsync(ct);

    /// <summary>Проект по идентификатору</summary>
    /// <param name="id">Идентификатор проекта</param>
    /// <response code="200">Проект найден</response>
    /// <response code="404">Проекта с таким id нет</response>
    [HttpGet("{id:int}")]
    [ProducesResponseType<Project>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<Project>> Get(int id, CancellationToken ct)
    {
        var project = await projects.GetAsync(id, ct);
        if (project is null)
        {
            return NotFound();
        }
        return project;
    }

    /// <summary>Статистика задач проекта</summary>
    /// <remarks>Просрочены задачи со сроком раньше текущей даты UTC и статусом не Done. Для пустого проекта все счётчики равны нулю.</remarks>
    /// <param name="id">Идентификатор проекта</param>
    /// <response code="200">Статистика проекта</response>
    /// <response code="404">Проекта с таким id нет</response>
    [HttpGet("{id:int}/stats")]
    [ProducesResponseType<ProjectStats>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProjectStats>> GetStats(int id, CancellationToken ct)
    {
        var project = await projects.GetAsync(id, ct);
        if (project is null)
        {
            return NotFound();
        }
        return await projects.GetStatsAsync(id, ct);
    }

    /// <summary>Создать проект</summary>
    /// <response code="201">Проект создан; его адрес — в заголовке Location</response>
    /// <response code="400">Название пустое или длиннее 100 символов</response>
    /// <response code="409">Проект с таким названием уже есть</response>
    [HttpPost]
    [ProducesResponseType<Project>(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<Project>> Create(CreateProjectRequest request, CancellationToken ct)
    {
        if (await projects.NameExistsAsync(request.Name, ct))
        {
            return Problem($"Проект «{request.Name}» уже существует", statusCode: StatusCodes.Status409Conflict);
        }

        var project = await projects.CreateAsync(request.Name, ct);
        return CreatedAtAction(nameof(Get), new { id = project.Id }, project);
    }

    /// <summary>Переименовать проект</summary>
    /// <param name="id">Идентификатор проекта</param>
    /// <param name="request">Новое уникальное имя, до 100 символов</param>
    /// <response code="200">Проект переименован; прежнее имя также допустимо</response>
    /// <response code="400">Название пустое или длиннее 100 символов</response>
    /// <response code="404">Проекта с таким id нет</response>
    /// <response code="409">Имя занято другим проектом</response>
    [HttpPut("{id:int}")]
    [ProducesResponseType<Project>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<Project>> Rename(int id, RenameProjectRequest request, CancellationToken ct)
    {
        var existing = await projects.GetAsync(id, ct);
        if (existing is null)
        {
            return NotFound();
        }
        if (existing.Name != request.Name && await projects.NameExistsAsync(request.Name, ct))
        {
            return Problem("Имя занято другим проектом", statusCode: StatusCodes.Status409Conflict);
        }
        try
        {
            var renamed = await projects.RenameAsync(id, request.Name, ct);
            return renamed is null ? NotFound() : renamed;
        }
        catch (ProjectNameConflictException)
        {
            return Problem("Имя занято другим проектом", statusCode: StatusCodes.Status409Conflict);
        }
    }

    /// <summary>Удалить проект вместе с его задачами</summary>
    /// <param name="id">Идентификатор проекта</param>
    /// <response code="204">Проект удалён</response>
    /// <response code="404">Проекта с таким id нет</response>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id, CancellationToken ct)
    {
        if (!await projects.DeleteAsync(id, ct))
        {
            return NotFound();
        }
        return NoContent();
    }
}

// Что клиент присылает в теле запроса. Атрибуты — правила проверки: нарушение → 400 автоматически

/// <summary>Создание проекта</summary>
/// <param name="Name">Название проекта: уникальное, до 100 символов</param>
public sealed record CreateProjectRequest(
    [Required, StringLength(100)] string Name);

/// <summary>Переименование проекта</summary>
/// <param name="Name">Новое название: уникальное, до 100 символов</param>
public sealed record RenameProjectRequest(
    [Required, StringLength(100)] string Name);
