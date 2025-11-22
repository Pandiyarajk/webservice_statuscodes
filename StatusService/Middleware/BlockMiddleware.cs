using StatusService.Services;
using System.Text.Json;

namespace StatusService.Middleware;

public class BlockMiddleware
{
    private readonly RequestDelegate _next;

    public BlockMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context, BlocklistService blocklistService)
    {
        var ip = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";

        if (await blocklistService.IsBlockedAsync(ip))
        {
            context.Response.StatusCode = 429;
            context.Response.ContentType = "application/json";

            var error = new
            {
                error = "IP address is blocked",
                reason = "Too many requests",
                ip = ip
            };

            await context.Response.WriteAsJsonAsync(error);
            return;
        }

        await _next(context);
    }
}
