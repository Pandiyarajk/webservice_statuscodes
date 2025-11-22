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
builder.Services.AddSingleton<DataGenerationService>();

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

// Educational API Endpoints - Generate sample data for training/testing

// Get random users
app.MapGet("/api/users", (DataGenerationService dataService, int count = 10, int? id = null) =>
{
    if (count < 1 || count > 100)
    {
        return Results.BadRequest(new { error = "Count must be between 1 and 100" });
    }
    
    if (id.HasValue)
    {
        return Results.Ok(new
        {
            success = true,
            count = 1,
            data = dataService.GenerateUser(id.Value),
            timestamp = DateTime.UtcNow.ToString("o")
        });
    }
    
    return Results.Ok(new
    {
        success = true,
        count = count,
        data = dataService.GenerateUsers(count),
        timestamp = DateTime.UtcNow.ToString("o")
    });
});

// Get random products
app.MapGet("/api/products", (DataGenerationService dataService, int count = 10, int? id = null) =>
{
    if (count < 1 || count > 100)
    {
        return Results.BadRequest(new { error = "Count must be between 1 and 100" });
    }
    
    if (id.HasValue)
    {
        return Results.Ok(new
        {
            success = true,
            count = 1,
            data = dataService.GenerateProduct(id.Value),
            timestamp = DateTime.UtcNow.ToString("o")
        });
    }
    
    return Results.Ok(new
    {
        success = true,
        count = count,
        data = dataService.GenerateProducts(count),
        timestamp = DateTime.UtcNow.ToString("o")
    });
});

// Get random orders
app.MapGet("/api/orders", (DataGenerationService dataService, int count = 10, int? id = null, int? userId = null) =>
{
    if (count < 1 || count > 100)
    {
        return Results.BadRequest(new { error = "Count must be between 1 and 100" });
    }
    
    if (id.HasValue)
    {
        return Results.Ok(new
        {
            success = true,
            count = 1,
            data = dataService.GenerateOrder(id.Value, userId),
            timestamp = DateTime.UtcNow.ToString("o")
        });
    }
    
    return Results.Ok(new
    {
        success = true,
        count = count,
        data = dataService.GenerateOrders(count),
        timestamp = DateTime.UtcNow.ToString("o")
    });
});

// Get random data of any type
app.MapGet("/api/random", (DataGenerationService dataService, string type = "user", int count = 1) =>
{
    if (count < 1 || count > 100)
    {
        return Results.BadRequest(new { error = "Count must be between 1 and 100" });
    }
    
    var validTypes = new[] { "user", "product", "order" };
    if (!validTypes.Contains(type.ToLower()))
    {
        return Results.BadRequest(new 
        { 
            error = $"Invalid type '{type}'. Valid types are: {string.Join(", ", validTypes)}",
            validTypes = validTypes
        });
    }
    
    return Results.Ok(new
    {
        success = true,
        type = type,
        count = count,
        data = dataService.GenerateRandomData(type, count),
        timestamp = DateTime.UtcNow.ToString("o")
    });
});

// Batch endpoint - get multiple types of data in one request
app.MapGet("/api/batch", (DataGenerationService dataService, int users = 5, int products = 5, int orders = 5) =>
{
    if (users < 0 || users > 50 || products < 0 || products > 50 || orders < 0 || orders > 50)
    {
        return Results.BadRequest(new { error = "Each count must be between 0 and 50" });
    }
    
    return Results.Ok(new
    {
        success = true,
        data = new
        {
            users = users > 0 ? dataService.GenerateUsers(users) : new List<object>(),
            products = products > 0 ? dataService.GenerateProducts(products) : new List<object>(),
            orders = orders > 0 ? dataService.GenerateOrders(orders) : new List<object>()
        },
        counts = new
        {
            users = users,
            products = products,
            orders = orders
        },
        timestamp = DateTime.UtcNow.ToString("o")
    });
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
