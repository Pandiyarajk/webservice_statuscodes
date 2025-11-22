using Microsoft.Data.Sqlite;
using System.Threading.Channels;

namespace StatusService.Services;

public class LogEntry
{
    public DateTime Timestamp { get; set; }
    public string? IP { get; set; }
    public string? Method { get; set; }
    public string? Path { get; set; }
    public int StatusCode { get; set; }
    public string? UserAgent { get; set; }
    public string? DataFileRef { get; set; }
}

public class LogService : IDisposable
{
    private readonly string _dbPath;
    private readonly Channel<LogEntry> _logChannel;
    private readonly Task _processingTask;
    private readonly CancellationTokenSource _cts = new();

    public LogService()
    {
        _dbPath = Path.Combine("Data", "logs.db");
        InitializeDatabase();

        _logChannel = Channel.CreateUnbounded<LogEntry>();
        _processingTask = Task.Run(ProcessLogsAsync);
    }

    private void InitializeDatabase()
    {
        using var connection = new SqliteConnection($"Data Source={_dbPath}");
        connection.Open();

        var command = connection.CreateCommand();
        command.CommandText = "PRAGMA journal_mode=WAL;";
        command.ExecuteNonQuery();

        command.CommandText = @"
            CREATE TABLE IF NOT EXISTS RequestLogs (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Timestamp TEXT NOT NULL,
                IP TEXT,
                Method TEXT,
                Path TEXT,
                StatusCode INTEGER,
                UserAgent TEXT,
                DataFileRef TEXT
            );
        ";
        command.ExecuteNonQuery();
    }

    public async Task LogAsync(LogEntry entry)
    {
        await _logChannel.Writer.WriteAsync(entry);
    }

    private async Task ProcessLogsAsync()
    {
        await foreach (var entry in _logChannel.Reader.ReadAllAsync(_cts.Token))
        {
            try
            {
                await using var connection = new SqliteConnection($"Data Source={_dbPath}");
                await connection.OpenAsync();

                await using var command = connection.CreateCommand();
                command.CommandText = @"
                    INSERT INTO RequestLogs (Timestamp, IP, Method, Path, StatusCode, UserAgent, DataFileRef)
                    VALUES ($timestamp, $ip, $method, $path, $statusCode, $userAgent, $dataFileRef)
                ";

                command.Parameters.AddWithValue("$timestamp", entry.Timestamp.ToString("o"));
                command.Parameters.AddWithValue("$ip", entry.IP ?? string.Empty);
                command.Parameters.AddWithValue("$method", entry.Method ?? string.Empty);
                command.Parameters.AddWithValue("$path", entry.Path ?? string.Empty);
                command.Parameters.AddWithValue("$statusCode", entry.StatusCode);
                command.Parameters.AddWithValue("$userAgent", entry.UserAgent ?? string.Empty);
                command.Parameters.AddWithValue("$dataFileRef", entry.DataFileRef ?? string.Empty);

                await command.ExecuteNonQueryAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error logging to database: {ex.Message}");
            }
        }
    }

    public async Task<List<LogEntry>> GetRecentLogsAsync(int limit = 100)
    {
        var logs = new List<LogEntry>();

        await using var connection = new SqliteConnection($"Data Source={_dbPath}");
        await connection.OpenAsync();

        await using var command = connection.CreateCommand();
        command.CommandText = "SELECT Timestamp, IP, Method, Path, StatusCode, UserAgent, DataFileRef FROM RequestLogs ORDER BY Id DESC LIMIT $limit";
        command.Parameters.AddWithValue("$limit", limit);

        await using var reader = await command.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            logs.Add(new LogEntry
            {
                Timestamp = DateTime.Parse(reader.GetString(0)),
                IP = reader.GetString(1),
                Method = reader.GetString(2),
                Path = reader.GetString(3),
                StatusCode = reader.GetInt32(4),
                UserAgent = reader.GetString(5),
                DataFileRef = reader.IsDBNull(6) ? null : reader.GetString(6)
            });
        }

        return logs;
    }

    public void Dispose()
    {
        _cts.Cancel();
        _logChannel.Writer.Complete();
        _processingTask.Wait(TimeSpan.FromSeconds(5));
        _cts.Dispose();
    }
}
