using System.Net;
using System.Net.Http.Json;
using DemoApi.Domain;
using Microsoft.AspNetCore.Mvc.Testing;

namespace DemoApi.Tests.Integration;

[Collection(ApiCollection.Name)]
public class ProjectsApiTests(WebApplicationFactory<Program> factory)
{
    private readonly HttpClient _client = factory.CreateClient();

    [Fact]
    public async Task Create_ReturnsCreatedWithLocation()
    {
        var response = await _client.PostAsJsonAsync("/api/projects", new { name = TestApi.Unique("project") });

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        Assert.NotNull(response.Headers.Location);
    }

    [Fact]
    public async Task Create_DuplicateName_ReturnsConflict()
    {
        var name = TestApi.Unique("duplicate");
        (await _client.PostAsJsonAsync("/api/projects", new { name })).EnsureSuccessStatusCode();

        var response = await _client.PostAsJsonAsync("/api/projects", new { name });

        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
    }

    [Fact]
    public async Task Create_EmptyName_ReturnsBadRequest()
    {
        var response = await _client.PostAsJsonAsync("/api/projects", new { name = "" });

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }

    [Fact]
    public async Task Get_Unknown_ReturnsNotFound()
    {
        var response = await _client.GetAsync($"/api/projects/{int.MaxValue}");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Rename_PreservesIdentityCreatedAtAndTasks()
    {
        var project = await _client.CreateProjectAsync();
        var task = await _client.CreateTaskAsync(project.Id);
        var name = TestApi.Unique("renamed");

        var response = await _client.PutAsJsonAsync($"/api/projects/{project.Id}", new { name });

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var renamed = await response.Content.ReadFromJsonAsync<Project>(TestApi.Json);
        Assert.Equal(project with { Name = name }, renamed);
        Assert.Equal(renamed, await _client.GetFromJsonAsync<Project>($"/api/projects/{project.Id}", TestApi.Json));
        var preserved = await _client.GetFromJsonAsync<TaskItem>($"/api/tasks/{task.Id}", TestApi.Json);
        Assert.Equal(task, preserved);
    }

    [Fact]
    public async Task Rename_DuplicateName_ReturnsConflictWithoutChangingProject()
    {
        var project = await _client.CreateProjectAsync();
        var other = await _client.CreateProjectAsync();

        var response = await _client.PutAsJsonAsync($"/api/projects/{project.Id}", new { name = other.Name });

        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
        Assert.Equal(project, await _client.GetFromJsonAsync<Project>($"/api/projects/{project.Id}", TestApi.Json));
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData(null)]
    [InlineData("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")]
    public async Task Rename_InvalidName_ReturnsBadRequest(string? name)
    {
        var project = await _client.CreateProjectAsync();

        var response = await _client.PutAsJsonAsync($"/api/projects/{project.Id}", new { name });

        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
        Assert.Equal(project, await _client.GetFromJsonAsync<Project>($"/api/projects/{project.Id}", TestApi.Json));
    }

    [Fact]
    public async Task Rename_UnknownProject_ReturnsNotFoundEvenIfNameIsTaken()
    {
        var project = await _client.CreateProjectAsync();

        var response = await _client.PutAsJsonAsync($"/api/projects/{int.MaxValue}", new { name = project.Name });

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Rename_CurrentName_CanBeRepeated()
    {
        var project = await _client.CreateProjectAsync();
        for (var attempt = 0; attempt < 2; attempt++)
        {
            var response = await _client.PutAsJsonAsync($"/api/projects/{project.Id}", new { name = project.Name });
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.Equal(project, await response.Content.ReadFromJsonAsync<Project>(TestApi.Json));
        }
    }

    [Fact]
    public async Task Rename_ConcurrentRequests_OnlyOneProjectGetsName()
    {
        var first = await _client.CreateProjectAsync();
        var second = await _client.CreateProjectAsync();
        var name = TestApi.Unique("shared");

        var responses = await Task.WhenAll(
            _client.PutAsJsonAsync($"/api/projects/{first.Id}", new { name }),
            _client.PutAsJsonAsync($"/api/projects/{second.Id}", new { name }));

        Assert.Single(responses, r => r.StatusCode == HttpStatusCode.OK);
        Assert.Single(responses, r => r.StatusCode == HttpStatusCode.Conflict);
        var projects = await _client.GetFromJsonAsync<Project[]>("/api/projects", TestApi.Json);
        Assert.Single(projects!, p => p.Name == name);
        var loser = responses[0].StatusCode == HttpStatusCode.Conflict ? first : second;
        Assert.Equal(loser, await _client.GetFromJsonAsync<Project>($"/api/projects/{loser.Id}", TestApi.Json));
    }

    [Fact]
    public async Task Rename_QuotedName_IsStoredAsLiteralText()
    {
        var project = await _client.CreateProjectAsync();
        var name = TestApi.Unique("O'Brien'; DROP TABLE projects;--");

        var response = await _client.PutAsJsonAsync($"/api/projects/{project.Id}", new { name });

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        Assert.Equal(project with { Name = name }, await response.Content.ReadFromJsonAsync<Project>(TestApi.Json));
        Assert.Equal(name, (await _client.GetFromJsonAsync<Project>($"/api/projects/{project.Id}", TestApi.Json))!.Name);
        Assert.NotNull(await _client.GetFromJsonAsync<Project[]>("/api/projects", TestApi.Json));
    }

    [Fact]
    public async Task Stats_ReturnsProjectCountsAndOverdueTasks()
    {
        var project = await _client.CreateProjectAsync();
        var statsUrl = $"/api/projects/{project.Id}/stats";
        var empty = await _client.GetFromJsonAsync<ProjectStats>(statsUrl, TestApi.Json);
        Assert.Equal(new ProjectStats(project.Id, 0, 0, 0, 0, 0), empty);

        var overdue = await _client.CreateTaskAsync(project.Id, "Просроченная");
        var dueToday = await _client.CreateTaskAsync(project.Id, "На сегодня");
        var inProgress = await _client.CreateTaskAsync(project.Id, "В работе без срока");
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        (await _client.PutAsJsonAsync($"/api/tasks/{overdue.Id}",
            new { title = overdue.Title, dueDate = today.AddDays(-1) })).EnsureSuccessStatusCode();
        (await _client.PutAsJsonAsync($"/api/tasks/{dueToday.Id}",
            new { title = dueToday.Title, dueDate = today })).EnsureSuccessStatusCode();
        (await _client.ChangeStatusAsync(inProgress.Id, TaskItemStatus.InProgress)).EnsureSuccessStatusCode();

        // Задачи другого проекта не должны попадать в агрегаты.
        await _client.CreateTaskAsync((await _client.CreateProjectAsync()).Id);

        var response = await _client.GetAsync(statsUrl);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var stats = await response.Content.ReadFromJsonAsync<ProjectStats>(TestApi.Json);
        Assert.Equal(new ProjectStats(project.Id, 3, 2, 1, 0, 1), stats);

        (await _client.ChangeStatusAsync(overdue.Id, TaskItemStatus.InProgress)).EnsureSuccessStatusCode();
        (await _client.ChangeStatusAsync(overdue.Id, TaskItemStatus.Done)).EnsureSuccessStatusCode();
        var afterCompletion = await _client.GetFromJsonAsync<ProjectStats>(statsUrl, TestApi.Json);
        Assert.Equal(new ProjectStats(project.Id, 3, 1, 1, 1, 0), afterCompletion);
    }

    [Fact]
    public async Task Stats_UnknownProject_ReturnsNotFound()
    {
        var response = await _client.GetAsync($"/api/projects/{int.MaxValue}/stats");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
