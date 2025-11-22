using System.Globalization;

namespace StatusService.Services;

public class CounterService
{
    private readonly string _counterFile;
    private readonly SemaphoreSlim _lock = new(1, 1);

    public CounterService()
    {
        _counterFile = Path.Combine("Data", "counter.txt");
        EnsureCounterFileExists();
    }

    private void EnsureCounterFileExists()
    {
        if (!File.Exists(_counterFile))
        {
            File.WriteAllText(_counterFile, "0");
        }
    }

    public async Task<int> GetNextIdAsync()
    {
        await _lock.WaitAsync();
        try
        {
            var content = await File.ReadAllTextAsync(_counterFile);
            if (!int.TryParse(content.Trim(), out var currentId))
            {
                currentId = 0;
            }

            var nextId = currentId + 1;
            await File.WriteAllTextAsync(_counterFile, nextId.ToString());
            return nextId;
        }
        finally
        {
            _lock.Release();
        }
    }

    public string FormatId(int id)
    {
        return $"data_{id:D6}.json";
    }
}
