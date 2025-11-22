using Microsoft.Extensions.Caching.Memory;
using StatusService.Middleware;
using StatusService.Services;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddMemoryCache();
builder.Services.AddSingleton<CounterService>();
builder.Services.AddSingleton<LargeJsonWriter>();
builder.Services.AddSingleton<BlocklistService>();
builder.Services.AddSingleton<LogService>();

var app = builder.Build();

// Ensure directories and files exist
EnsureDirectoriesAndFiles();

// Add middleware in order
app.UseMiddleware<BlockMiddleware>();
app.UseMiddleware<RateLimitMiddleware>();
app.UseMiddleware<LoggingMiddleware>();

// Health endpoint
app.MapGet("/health", () =>
{
    return Results.Ok(new
    {
        status = "OK",
        time = DateTime.UtcNow.ToString("o")
    });
});

// Status testing endpoint
app.MapGet("/status/{code}", async (
    int code,
    string? message,
    int? delay,
    int? size) =>
{
    // Apply delay if specified
    if (delay.HasValue && delay.Value > 0)
    {
        await Task.Delay(delay.Value);
    }

    // Validate status code range
    if (code < 100 || code > 599)
    {
        return Results.BadRequest(new { error = "Status code must be between 100 and 599" });
    }

    var response = new Dictionary<string, object>
    {
        ["requestedCode"] = code,
        ["returnedCode"] = code,
        ["timestamp"] = DateTime.UtcNow.ToString("o")
    };

    if (!string.IsNullOrEmpty(message))
    {
        response["message"] = message;
    }

    // Generate dummy body if size is specified
    if (size.HasValue && size.Value > 0)
    {
        var dummyData = new string('X', size.Value);
        response["dummyBody"] = dummyData;
    }

    return Results.Json(response, statusCode: code);
});

// Logs endpoint
app.MapGet("/logs", async (LogService logService, int limit = 100) =>
{
    var logs = await logService.GetRecentLogsAsync(limit);
    return Results.Ok(logs);
});

// Blocklist endpoint
app.MapGet("/blocklist", async (BlocklistService blocklistService) =>
{
    var blocked = await blocklistService.GetAllBlockedAsync();
    return Results.Ok(blocked);
});

// Unblock endpoint
app.MapGet("/unblock", async (BlocklistService blocklistService, string? ip) =>
{
    if (string.IsNullOrEmpty(ip))
    {
        return Results.BadRequest(new { error = "IP parameter is required" });
    }

    var success = await blocklistService.UnblockIpAsync(ip);
    if (success)
    {
        return Results.Ok(new { message = $"IP {ip} has been unblocked", ip });
    }

    return Results.NotFound(new { error = $"IP {ip} was not found in blocklist", ip });
});

app.Run();

void EnsureDirectoriesAndFiles()
{
    // Create directories
    Directory.CreateDirectory("Data");
    Directory.CreateDirectory("data");

    // Create counter.txt if it doesn't exist
    var counterFile = Path.Combine("Data", "counter.txt");
    if (!File.Exists(counterFile))
    {
        File.WriteAllText(counterFile, "0");
    }

    // Create blocklist.json if it doesn't exist
    var blocklistFile = Path.Combine("Data", "blocklist.json");
    if (!File.Exists(blocklistFile))
    {
        File.WriteAllText(blocklistFile, "{}");
    }
}
