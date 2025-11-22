using System.Text.Json;
using System.Text.Json.Serialization;

namespace StatusService.Services;

public class BlocklistEntry
{
    [JsonPropertyName("blockedAt")]
    public DateTime BlockedAt { get; set; }

    [JsonPropertyName("reason")]
    public string Reason { get; set; } = string.Empty;
}

public class BlocklistService
{
    private readonly string _blocklistFile;
    private readonly SemaphoreSlim _lock = new(1, 1);
    private Dictionary<string, BlocklistEntry> _blocklist = new();

    public BlocklistService()
    {
        _blocklistFile = Path.Combine("Data", "blocklist.json");
        LoadBlocklist();
    }

    private void LoadBlocklist()
    {
        if (!File.Exists(_blocklistFile))
        {
            _blocklist = new Dictionary<string, BlocklistEntry>();
            SaveBlocklist();
            return;
        }

        try
        {
            var json = File.ReadAllText(_blocklistFile);
            _blocklist = JsonSerializer.Deserialize<Dictionary<string, BlocklistEntry>>(json) ?? new Dictionary<string, BlocklistEntry>();
        }
        catch
        {
            _blocklist = new Dictionary<string, BlocklistEntry>();
        }
    }

    private void SaveBlocklist()
    {
        var json = JsonSerializer.Serialize(_blocklist, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText(_blocklistFile, json);
    }

    public async Task<bool> IsBlockedAsync(string ip)
    {
        await _lock.WaitAsync();
        try
        {
            if (!_blocklist.ContainsKey(ip))
                return false;

            var entry = _blocklist[ip];
            var hourAgo = DateTime.UtcNow.AddHours(-1);

            if (entry.BlockedAt < hourAgo)
            {
                _blocklist.Remove(ip);
                SaveBlocklist();
                return false;
            }

            return true;
        }
        finally
        {
            _lock.Release();
        }
    }

    public async Task BlockIpAsync(string ip, string reason)
    {
        await _lock.WaitAsync();
        try
        {
            _blocklist[ip] = new BlocklistEntry
            {
                BlockedAt = DateTime.UtcNow,
                Reason = reason
            };
            SaveBlocklist();
        }
        finally
        {
            _lock.Release();
        }
    }

    public async Task<bool> UnblockIpAsync(string ip)
    {
        await _lock.WaitAsync();
        try
        {
            if (_blocklist.Remove(ip))
            {
                SaveBlocklist();
                return true;
            }
            return false;
        }
        finally
        {
            _lock.Release();
        }
    }

    public async Task<Dictionary<string, BlocklistEntry>> GetAllBlockedAsync()
    {
        await _lock.WaitAsync();
        try
        {
            return new Dictionary<string, BlocklistEntry>(_blocklist);
        }
        finally
        {
            _lock.Release();
        }
    }
}
