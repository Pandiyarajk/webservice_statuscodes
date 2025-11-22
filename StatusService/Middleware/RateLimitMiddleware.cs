using Microsoft.Extensions.Caching.Memory;
using StatusService.Services;
using System.Collections.Concurrent;

namespace StatusService.Middleware;

public class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private readonly IMemoryCache _cache;

    public RateLimitMiddleware(RequestDelegate next, IMemoryCache cache)
    {
        _next = next;
        _cache = cache;
    }

    public async Task InvokeAsync(HttpContext context, BlocklistService blocklistService)
    {
        var ip = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";

        // Skip rate limiting for health and admin endpoints
        if (context.Request.Path.StartsWithSegments("/health") ||
            context.Request.Path.StartsWithSegments("/logs") ||
            context.Request.Path.StartsWithSegments("/blocklist") ||
            context.Request.Path.StartsWithSegments("/unblock"))
        {
            await _next(context);
            return;
        }

        // Get or create request timestamps for this IP
        var minuteKey = $"rate_1min_{ip}";
        var tenMinKey = $"rate_10min_{ip}";

        var minuteRequests = _cache.GetOrCreate(minuteKey, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(1);
            return new ConcurrentBag<DateTime>();
        }) ?? new ConcurrentBag<DateTime>();

        var tenMinRequests = _cache.GetOrCreate(tenMinKey, entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10);
            return new ConcurrentBag<DateTime>();
        }) ?? new ConcurrentBag<DateTime>();

        var now = DateTime.UtcNow;

        // Add current request
        minuteRequests.Add(now);
        tenMinRequests.Add(now);

        // Clean old entries
        var oneMinuteAgo = now.AddMinutes(-1);
        var tenMinutesAgo = now.AddMinutes(-10);

        minuteRequests = new ConcurrentBag<DateTime>(minuteRequests.Where(t => t > oneMinuteAgo));
        tenMinRequests = new ConcurrentBag<DateTime>(tenMinRequests.Where(t => t > tenMinutesAgo));

        // Update cache
        _cache.Set(minuteKey, minuteRequests, TimeSpan.FromMinutes(1));
        _cache.Set(tenMinKey, tenMinRequests, TimeSpan.FromMinutes(10));

        // Check 10-minute threshold for blocking
        if (tenMinRequests.Count > 200)
        {
            await blocklistService.BlockIpAsync(ip, "Exceeded 200 requests in 10 minutes");
            context.Response.StatusCode = 429;
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsJsonAsync(new { error = "Rate limit exceeded - IP blocked" });
            return;
        }

        // Check 1-minute threshold for throttling
        if (minuteRequests.Count > 30)
        {
            context.Response.StatusCode = 429;
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsJsonAsync(new { error = "Rate limit exceeded" });
            return;
        }

        await _next(context);
    }
}
