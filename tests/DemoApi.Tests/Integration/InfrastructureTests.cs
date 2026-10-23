using System.Net;
using System.Net.Http.Json;
using DemoApi.Controllers;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.Configuration;

namespace DemoApi.Tests.Integration;

[Collection(ApiCollection.Name)]
public class InfrastructureTests(WebApplicationFactory<Program> factory)
{
    [Fact]
    public async Task Info_ReturnsMessageAndConfiguredVersion()
    {
        await using var versioned = factory.WithWebHostBuilder(b => b.ConfigureAppConfiguration((_, cfg) =>
            cfg.AddInMemoryCollection(new Dictionary<string, string?> { ["APP_VERSION"] = "integration-test" })));

        var response = await versioned.CreateClient().GetFromJsonAsync<InfoResponse>("/");

        Assert.NotNull(response);
        Assert.Equal("DemoApi", response.Service);
        Assert.Equal("integration-test", response.Version);
        Assert.Equal("hello from CI/CD", response.Message);
        Assert.False(string.IsNullOrWhiteSpace(response.Host));
    }

    [Theory]
    [InlineData("/health/live")]
    [InlineData("/health/ready")]
    public async Task HealthEndpoints_ReturnOk(string url)
    {
        var response = await factory.CreateClient().GetAsync(url);

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task Metrics_AreExposed()
    {
        var client = factory.CreateClient();
        await client.GetAsync("/health/live");

        var body = await client.GetStringAsync("/metrics");

        Assert.Contains("http_requests_received_total", body);
    }

    [Fact]
    public async Task Chaos_WhenDisabled_ReturnsNotFound()
    {
        await using var disabled = factory.WithWebHostBuilder(b => b.ConfigureAppConfiguration((_, cfg) =>
            cfg.AddInMemoryCollection(new Dictionary<string, string?> { ["Chaos:Enabled"] = "false" })));

        var response = await disabled.CreateClient().GetAsync("/api/chaos/error");

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
}
