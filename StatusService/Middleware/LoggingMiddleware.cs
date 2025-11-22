using StatusService.Services;
using System.Text;

namespace StatusService.Middleware;

public class LoggingMiddleware
{
    private readonly RequestDelegate _next;
    private const int LargeJsonThreshold = 200 * 1024; // 200 KB

    public LoggingMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(
        HttpContext context,
        LogService logService,
        LargeJsonWriter largeJsonWriter)
    {
        var originalBodyStream = context.Response.Body;
        using var responseBody = new MemoryStream();
        context.Response.Body = responseBody;

        var statusCode = 0;
        string? dataFileRef = null;

        try
        {
            // Read request body if present
            if (context.Request.ContentLength > 0)
            {
                context.Request.EnableBuffering();
                
                using var reader = new StreamReader(
                    context.Request.Body,
                    encoding: Encoding.UTF8,
                    detectEncodingFromByteOrderMarks: false,
                    leaveOpen: true);

                var body = await reader.ReadToEndAsync();
                context.Request.Body.Position = 0;

                // Check if body exceeds threshold
                var bodySize = Encoding.UTF8.GetByteCount(body);
                if (bodySize >= LargeJsonThreshold)
                {
                    dataFileRef = await largeJsonWriter.WriteJsonAsync(body);
                }
            }

            await _next(context);
            statusCode = context.Response.StatusCode;
        }
        catch (Exception)
        {
            statusCode = 500;
            throw;
        }
        finally
        {
            // Log the request
            var logEntry = new LogEntry
            {
                Timestamp = DateTime.UtcNow,
                IP = context.Connection.RemoteIpAddress?.ToString(),
                Method = context.Request.Method,
                Path = context.Request.Path,
                StatusCode = statusCode > 0 ? statusCode : context.Response.StatusCode,
                UserAgent = context.Request.Headers.UserAgent.ToString(),
                DataFileRef = dataFileRef
            };

            await logService.LogAsync(logEntry);

            // Copy response back
            responseBody.Seek(0, SeekOrigin.Begin);
            await responseBody.CopyToAsync(originalBodyStream);
        }
    }
}
