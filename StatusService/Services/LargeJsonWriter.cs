using System.Text;

namespace StatusService.Services;

public class LargeJsonWriter
{
    private readonly CounterService _counterService;
    private readonly string _baseDataPath = "data";

    public LargeJsonWriter(CounterService counterService)
    {
        _counterService = counterService;
    }

    public async Task<string> WriteJsonAsync(string jsonContent)
    {
        var today = DateTime.UtcNow.ToString("yyyy-MM-dd");
        var dailyPath = Path.Combine(_baseDataPath, today);

        if (!Directory.Exists(dailyPath))
        {
            Directory.CreateDirectory(dailyPath);
        }

        var id = await _counterService.GetNextIdAsync();
        var filename = _counterService.FormatId(id);
        var fullPath = Path.Combine(dailyPath, filename);

        await using var fileStream = new FileStream(fullPath, FileMode.Create, FileAccess.Write, FileShare.None, 4096, useAsync: true);
        var bytes = Encoding.UTF8.GetBytes(jsonContent);
        await fileStream.WriteAsync(bytes);
        await fileStream.FlushAsync();

        return fullPath;
    }
}
