# Change Log

All notable changes to the StatusService project will be documented in this file.

## [1.1.0] - 2025-11-22

### Added - Educational Features

- **Educational API Endpoints** - New data generation endpoints for training and testing
  - `/api/users`: Generate random user data (1-100 items)
  - `/api/products`: Generate random product data (1-100 items)
  - `/api/orders`: Generate random order data (1-100 items)
  - `/api/random`: Generate any type of random data with type parameter
  - `/api/batch`: Batch endpoint to fetch multiple data types in one request
  - All endpoints support optional `id` parameter for specific item generation
  - Orders endpoint supports `userId` parameter for user-specific orders

- **DataGenerationService** - New service for generating realistic test data
  - Generates users with realistic names, emails, cities, phone numbers
  - Generates products with categories, prices, ratings, inventory
  - Generates orders with items, totals, shipping addresses
  - Thread-safe random data generation
  - Realistic data relationships (e.g., order items reference products)

- **Python Integration Examples** - Comprehensive Python scripts for education
  - `basic_request.py`: Introduction to API requests and JSON handling
  - `error_handling.py`: Error handling, retries, and exponential backoff
  - `data_processing.py`: Data fetching, analysis, statistics, and export
  - `integration_test.py`: Automated integration testing with assertions
  - `service_integration.py`: Service-to-service integration patterns
  - `rate_limit_test.py`: Rate limiting behavior and handling strategies
  - `requirements.txt`: Python dependencies (requests library)
  - Detailed `README.md` with examples and learning outcomes

### Use Cases

- **API Training**: Educational tool for teaching REST API integration
- **Integration Testing**: Generate realistic test data for service validation
- **Development**: Mock data for frontend and backend development
- **Testing**: Test fixtures and data for automated testing
- **ETL Pipelines**: Example patterns for data transformation and migration

### Technical Details

#### Data Structures

**User Object:**
- id, username, email, firstName, lastName
- age, city, phone, registeredAt
- isActive, credits

**Product Object:**
- id, name, category, price, description
- inStock, rating, reviews, sku
- weight, createdAt

**Order Object:**
- id, userId, status, items[], orderDate
- subtotal, tax, shipping, total
- shippingAddress (street, city, state, zipCode)

#### Response Format

All educational endpoints return standardized responses:
```json
{
  "success": true,
  "count": 10,
  "data": [...],
  "timestamp": "2025-11-22T12:34:56.789Z"
}
```

### Documentation

- Updated `StatusService/README.md` with educational endpoints section
- Added Python examples documentation in `python_examples/README.md`
- Added educational use cases section
- Updated troubleshooting and support resources

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
- Additional data types (transactions, reviews, categories)
- GraphQL endpoint for flexible data queries
- WebSocket support for real-time data streams
- Authentication examples for educational purposes

---

## Version History

- **1.1.0** (2025-11-22) - Educational features and Python examples
- **1.0.0** (2025-11-22) - Initial release with full feature set
