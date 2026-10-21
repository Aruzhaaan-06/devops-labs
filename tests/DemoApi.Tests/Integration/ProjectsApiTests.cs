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
