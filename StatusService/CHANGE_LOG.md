# Change Log

All notable changes to the StatusService project will be documented in this file.

## [1.0.0] - 2025-11-22

### Added
- Initial release of StatusService
- **Status Testing Endpoint** (`/status/{code}`)
  - Support for HTTP status codes 100-599
  - Optional query parameters: `message`, `delay`, `size`
  - Customizable response bodies and delays
  
- **Rate Limiting System**
  - Two-tier rate limiting (throttling + blocking)
  - 30 requests per minute per IP (Tier 1)
  - 200 requests per 10 minutes blocks IP (Tier 2)
  - Sliding window implementation using `IMemoryCache`
  - Automatic IP blocking with 1-hour auto-expire
  
- **IP Blocking Middleware**
  - JSON-based blocklist (`Data/blocklist.json`)
  - Auto-expire blocked IPs after 1 hour
  - Thread-safe blocklist operations
  
- **Request Logging**
  - Async SQLite logging with WAL mode
  - Channel-based queue for non-blocking writes
  - Automatic database initialization
  - Schema includes: timestamp, IP, method, path, status code, user agent, data file reference
  
- **Large JSON Handling**
  - 200 KB threshold for external file storage
  - Daily folder rotation (`data/YYYY-MM-DD/`)
  - Auto-incrementing file names with 6-digit padding (`data_NNNNNN.json`)
  - Thread-safe counter service
  - Async file I/O
  
- **Services**
  - `CounterService`: Thread-safe file counter with semaphore locking
  - `LargeJsonWriter`: Async large JSON file writer with daily rotation
  - `BlocklistService`: IP blocklist management with JSON persistence
  - `LogService`: Async SQLite logging with channel-based queue
  
- **Admin Endpoints**
  - `/health`: Health check endpoint
  - `/logs?limit=N`: Retrieve recent logs from SQLite (default 100)
  - `/blocklist`: View all blocked IP addresses
  - `/unblock?ip=X.X.X.X`: Remove IP from blocklist
  
- **Middleware Pipeline**
  - `BlockMiddleware`: IP blocking check (first)
  - `RateLimitMiddleware`: Rate limiting enforcement (second)
  - `LoggingMiddleware`: Request logging (third)
  
- **Auto-Initialization**
  - Automatic creation of `Data/` and `data/` directories
  - Auto-generation of `counter.txt`, `blocklist.json`
  - SQLite database auto-creation with WAL mode
  
- **Configuration**
  - `appsettings.json` with Kestrel configuration
  - Default port: 5000
  - Configurable logging levels
  
- **Documentation**
  - Comprehensive `README.md` with setup instructions
  - API endpoint documentation with examples
  - Rate limiting explanation
  - Large JSON handling details
  - SQLite schema documentation
  - Testing examples
  - Troubleshooting guide
  
- **Dependencies**
  - .NET 8.0
  - Microsoft.Data.Sqlite 8.0.0
  - Microsoft.Extensions.Caching.Memory 8.0.0

### Technical Details

#### Middleware Order
1. BlockMiddleware - Checks IP blocklist first
2. RateLimitMiddleware - Enforces rate limits
3. LoggingMiddleware - Logs all requests

#### Rate Limiting Algorithm
- Uses `IMemoryCache` with `ConcurrentBag<DateTime>` per IP
- Sliding window with timestamp buckets
- Automatic cleanup of expired entries
- Exempt endpoints: `/health`, `/logs`, `/blocklist`, `/unblock`

#### Logging Architecture
- Non-blocking async logging via .NET Channels
- Background processing task
- Graceful shutdown with 5-second timeout
- Large bodies (≥200KB) stored externally with file reference

#### File Storage Pattern
```
data/
└── YYYY-MM-DD/
    ├── data_000001.json
    ├── data_000002.json
    └── ...
```

#### Database Schema
```sql
CREATE TABLE RequestLogs (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Timestamp TEXT NOT NULL,
    IP TEXT,
    Method TEXT,
    Path TEXT,
    StatusCode INTEGER,
    UserAgent TEXT,
    DataFileRef TEXT
);
```

### Project Structure
```
StatusService/
├── Program.cs
├── appsettings.json
├── StatusService.csproj
├── Middleware/
│   ├── BlockMiddleware.cs
│   ├── RateLimitMiddleware.cs
│   └── LoggingMiddleware.cs
├── Services/
│   ├── CounterService.cs
│   ├── LargeJsonWriter.cs
│   ├── BlocklistService.cs
│   └── LogService.cs
├── Data/
│   ├── logs.db
│   ├── blocklist.json
│   └── counter.txt
└── data/ (generated)
```

### Known Limitations
- Rate limiting is per-instance (not distributed)
- Blocklist is file-based (not shared across instances)
- SQLite WAL mode requires file system locking support

### Future Considerations
- Distributed rate limiting (Redis)
- Centralized blocklist management
- Metrics and Prometheus integration
- Structured logging (Serilog)
- Docker containerization
- Health checks for dependencies

---

## Version History

- **1.0.0** (2025-11-22) - Initial release with full feature set
