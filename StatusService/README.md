# StatusService

A production-ready C# .NET 8 minimal API for HTTP status code testing, rate limiting, and request logging with SQLite persistence and large JSON file rotation.

## 📋 Features

- **Status Code Testing**: Return any HTTP status code (100-599) with customizable responses
- **Rate Limiting**: IP-based rate limiting with automatic blocking
- **Request Logging**: Async SQLite logging with WAL mode
- **Large JSON Handling**: Automatic file rotation for large request bodies (>200KB)
- **IP Blocking**: Auto-expire blocklist with JSON persistence
- **Admin Endpoints**: Health checks, log viewing, and blocklist management

## 🏗️ Project Structure

```
StatusService/
├── Program.cs                    # Application entry point and endpoint definitions
├── appsettings.json              # Configuration file
├── StatusService.csproj          # Project file with dependencies
├── Middleware/
│   ├── BlockMiddleware.cs        # IP blocking middleware
│   ├── RateLimitMiddleware.cs    # Rate limiting middleware
│   └── LoggingMiddleware.cs      # Request logging middleware
├── Services/
│   ├── CounterService.cs         # Thread-safe counter for file naming
│   ├── LargeJsonWriter.cs        # Large JSON file writer with daily rotation
│   ├── BlocklistService.cs       # IP blocklist management
│   └── LogService.cs             # Async SQLite logging service
├── Data/
│   ├── logs.db                   # SQLite database (auto-created)
│   ├── blocklist.json            # IP blocklist (auto-created)
│   └── counter.txt               # File counter (auto-created)
└── data/                         # Generated JSON files (daily folders)
    └── 2025-11-22/
        ├── data_000001.json
        └── data_000002.json
```

## 🚀 Setup Instructions

### Prerequisites

- .NET 8 SDK or later
- Windows, Linux, or macOS

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd StatusService
   ```

2. **Restore dependencies:**
   ```bash
   dotnet restore
   ```

3. **Build the project:**
   ```bash
   dotnet build
   ```

4. **Run the application:**
   ```bash
   dotnet run
   ```

The service will start on `http://localhost:5000`

### Windows Quick Start

```cmd
cd StatusService
dotnet run
```

## 📡 API Endpoints

### Educational API Endpoints (New!)

The service now includes educational endpoints that generate realistic test data for learning API integration and testing.

#### 1. Get Users

**Endpoint:** `GET /api/users`

**Parameters:**
- `count` (optional): Number of users to generate (1-100, default: 10)
- `id` (optional): Generate specific user with this ID

**Examples:**

```bash
# Get 10 random users
curl http://localhost:5000/api/users

# Get 25 users
curl "http://localhost:5000/api/users?count=25"

# Get specific user
curl "http://localhost:5000/api/users?id=12345"
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 12345,
      "username": "john.smith42",
      "email": "john.smith@example.com",
      "firstName": "John",
      "lastName": "Smith",
      "age": 32,
      "city": "New York",
      "phone": "+1-555-123-4567",
      "registeredAt": "2024-05-15T10:30:00Z",
      "isActive": true,
      "credits": 250.50
    }
  ],
  "timestamp": "2025-11-22T12:34:56.789Z"
}
```

#### 2. Get Products

**Endpoint:** `GET /api/products`

**Parameters:**
- `count` (optional): Number of products to generate (1-100, default: 10)
- `id` (optional): Generate specific product with this ID

**Examples:**

```bash
# Get 10 random products
curl http://localhost:5000/api/products

# Get 15 products
curl "http://localhost:5000/api/products?count=15"
```

**Sample Product:**
```json
{
  "id": 54321,
  "name": "Premium Widget",
  "category": "Electronics",
  "price": 149.99,
  "description": "High-quality premium widget...",
  "inStock": 45,
  "rating": 4.5,
  "reviews": 128,
  "sku": "ELE-5432",
  "weight": 2.5,
  "createdAt": "2023-08-20T15:45:00Z"
}
```

#### 3. Get Orders

**Endpoint:** `GET /api/orders`

**Parameters:**
- `count` (optional): Number of orders to generate (1-100, default: 10)
- `id` (optional): Generate specific order with this ID
- `userId` (optional): Generate order for specific user

**Examples:**

```bash
# Get 10 random orders
curl http://localhost:5000/api/orders

# Get order for specific user
curl "http://localhost:5000/api/orders?userId=12345&count=5"
```

#### 4. Get Random Data

**Endpoint:** `GET /api/random`

**Parameters:**
- `type` (required): Type of data (user, product, order)
- `count` (optional): Number of items (1-100, default: 1)

**Examples:**

```bash
# Get 5 random users
curl "http://localhost:5000/api/random?type=user&count=5"

# Get 3 random products
curl "http://localhost:5000/api/random?type=product&count=3"
```

#### 5. Batch Request

**Endpoint:** `GET /api/batch`

**Parameters:**
- `users` (optional): Number of users (0-50, default: 5)
- `products` (optional): Number of products (0-50, default: 5)
- `orders` (optional): Number of orders (0-50, default: 5)

**Examples:**

```bash
# Get mixed data
curl "http://localhost:5000/api/batch?users=10&products=10&orders=5"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": [...],
    "products": [...],
    "orders": [...]
  },
  "counts": {
    "users": 10,
    "products": 10,
    "orders": 5
  },
  "timestamp": "2025-11-22T12:34:56.789Z"
}
```

---

### Status Testing Endpoints

### 1. Status Testing Endpoint

Test any HTTP status code with optional parameters.

**Endpoint:** `GET /status/{code}`

**Parameters:**
- `code` (required): HTTP status code (100-599)
- `message` (optional): Custom message text
- `delay` (optional): Delay in milliseconds before responding
- `size` (optional): Generate dummy body of specified size

**Examples:**

```bash
# Simple 404 response
curl http://localhost:5000/status/404

# 200 with custom message
curl "http://localhost:5000/status/200?message=Success"

# 500 with 2-second delay
curl "http://localhost:5000/status/500?delay=2000"

# 200 with 1KB dummy body
curl "http://localhost:5000/status/200?size=1024"

# Combined parameters
curl "http://localhost:5000/status/201?message=Created&delay=500&size=512"
```

**Response Format:**
```json
{
  "requestedCode": 404,
  "returnedCode": 404,
  "timestamp": "2025-11-22T12:34:56.789Z",
  "message": "Optional message"
}
```

### 2. Health Check

Check service health and current time.

**Endpoint:** `GET /health`

**Example:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "OK",
  "time": "2025-11-22T12:34:56.789Z"
}
```

### 3. View Logs

Retrieve recent request logs from SQLite database.

**Endpoint:** `GET /logs?limit={count}`

**Parameters:**
- `limit` (optional): Number of logs to retrieve (default: 100)

**Example:**
```bash
curl http://localhost:5000/logs?limit=50
```

**Response:**
```json
[
  {
    "timestamp": "2025-11-22T12:34:56.789Z",
    "ip": "127.0.0.1",
    "method": "GET",
    "path": "/status/404",
    "statusCode": 404,
    "userAgent": "curl/7.68.0",
    "dataFileRef": null
  }
]
```

### 4. View Blocklist

View all currently blocked IP addresses.

**Endpoint:** `GET /blocklist`

**Example:**
```bash
curl http://localhost:5000/blocklist
```

**Response:**
```json
{
  "192.168.0.22": {
    "blockedAt": "2025-11-22T12:00:00Z",
    "reason": "Exceeded 200 requests in 10 minutes"
  }
}
```

### 5. Unblock IP

Remove an IP address from the blocklist.

**Endpoint:** `GET /unblock?ip={ip_address}`

**Parameters:**
- `ip` (required): IP address to unblock

**Example:**
```bash
curl "http://localhost:5000/unblock?ip=192.168.0.22"
```

**Response:**
```json
{
  "message": "IP 192.168.0.22 has been unblocked",
  "ip": "192.168.0.22"
}
```

## ⚡ Rate Limiting

The service implements a two-tier rate limiting system:

### Tier 1: Throttling (429 Response)
- **Limit**: 30 requests per minute per IP
- **Window**: 1-minute sliding window
- **Action**: Returns `429 Too Many Requests` with JSON error

### Tier 2: Automatic Blocking (Permanent Block)
- **Limit**: 200 requests in 10 minutes per IP
- **Window**: 10-minute sliding window
- **Action**: 
  - IP is added to blocklist
  - All subsequent requests return `429 Blocked`
  - Block auto-expires after 1 hour

### Rate Limit Response

```json
{
  "error": "Rate limit exceeded"
}
```

### Block Response

```json
{
  "error": "IP address is blocked",
  "reason": "Too many requests",
  "ip": "192.168.0.22"
}
```

### Exempt Endpoints

The following endpoints are **not** rate-limited:
- `/health`
- `/logs`
- `/blocklist`
- `/unblock`

## 📦 Large JSON File Handling

### Threshold
- Request bodies **< 200 KB**: Logged inline (not stored)
- Request bodies **≥ 200 KB**: Saved to external files

### File Storage

Large JSON bodies are stored with the following structure:

```
data/
├── 2025-11-22/
│   ├── data_000001.json
│   ├── data_000002.json
│   └── data_000003.json
├── 2025-11-23/
│   ├── data_000004.json
│   └── data_000005.json
```

### Features

- **Daily Rotation**: Files are organized by date (YYYY-MM-DD)
- **Auto-Increment**: Files use 6-digit padded counter (`data_NNNNNN.json`)
- **Thread-Safe**: Counter managed via semaphore lock
- **Async I/O**: Files written asynchronously to avoid blocking requests

### File Reference

When a large JSON is stored, the log entry includes a `DataFileRef` field:

```json
{
  "dataFileRef": "data/2025-11-22/data_000001.json"
}
```

## 🗄️ SQLite Database

### Database File
- **Location**: `Data/logs.db`
- **Mode**: WAL (Write-Ahead Logging) for better concurrency

### Schema

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

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `Id` | INTEGER | Auto-incrementing primary key |
| `Timestamp` | TEXT | ISO 8601 timestamp |
| `IP` | TEXT | Client IP address |
| `Method` | TEXT | HTTP method (GET, POST, etc.) |
| `Path` | TEXT | Request path |
| `StatusCode` | INTEGER | HTTP status code returned |
| `UserAgent` | TEXT | Client user agent string |
| `DataFileRef` | TEXT | Path to external JSON file (if applicable) |

### Async Logging

Logs are written asynchronously using .NET Channels:
- Non-blocking: Requests are not delayed by database writes
- Queue-based: Logs are queued and processed in background
- Reliable: Channels ensure all logs are written before shutdown

## 🛠️ Services

### CounterService
- **Purpose**: Thread-safe file counter management
- **File**: `Data/counter.txt`
- **Features**:
  - Atomic increment operations
  - Semaphore-based locking
  - 6-digit zero-padded formatting

### LargeJsonWriter
- **Purpose**: Write large JSON bodies to disk
- **Features**:
  - Daily folder creation
  - Async file I/O
  - UTF-8 encoding

### BlocklistService
- **Purpose**: Manage IP blocklist
- **File**: `Data/blocklist.json`
- **Features**:
  - Auto-expire after 1 hour
  - Thread-safe read/write
  - JSON persistence

### LogService
- **Purpose**: Async SQLite logging
- **Features**:
  - Channel-based queue
  - Background processing
  - WAL mode for performance
  - Graceful shutdown

## 🧪 Testing

### Test Rate Limiting

```bash
# Send 35 requests quickly (should hit rate limit)
for i in {1..35}; do
  curl http://localhost:5000/status/200
done
```

### Test Large JSON

```bash
# Generate 250KB JSON and POST it
dd if=/dev/zero bs=1024 count=250 | base64 | \
curl -X POST http://localhost:5000/status/200 \
  -H "Content-Type: application/json" \
  -d @-
```

### Test Delay

```bash
# 3-second delayed response
time curl "http://localhost:5000/status/200?delay=3000"
```

### Test Custom Status

```bash
# Return 418 I'm a teapot
curl -i "http://localhost:5000/status/418?message=I'm+a+teapot"
```

## 🔧 Configuration

### Port Configuration

Edit `appsettings.json`:

```json
{
  "Kestrel": {
    "Endpoints": {
      "Http": {
        "Url": "http://localhost:5000"
      }
    }
  }
}
```

### Rate Limit Configuration

Edit `Middleware/RateLimitMiddleware.cs`:

```csharp
// Line ~41: 1-minute limit
if (minuteRequests.Count > 30)  // Change 30 to your limit

// Line ~34: 10-minute block threshold
if (tenMinRequests.Count > 200)  // Change 200 to your threshold
```

### Large JSON Threshold

Edit `Middleware/LoggingMiddleware.cs`:

```csharp
// Line 11
private const int LargeJsonThreshold = 200 * 1024; // Change 200 to KB threshold
```

## 📊 Monitoring

### View Recent Activity
```bash
curl http://localhost:5000/logs?limit=20
```

### Check Blocked IPs
```bash
curl http://localhost:5000/blocklist
```

### Monitor Health
```bash
watch -n 5 curl -s http://localhost:5000/health
```

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Change the port in `appsettings.json` or kill the process using port 5000:

```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Locked

**Error:** `Database is locked`

**Solution:** Ensure only one instance is running. WAL mode should prevent most locking issues.

### Permission Denied

**Error:** `Access to the path is denied`

**Solution:** Ensure the application has write permissions to the `Data/` and `data/` directories.

## 🐍 Python Examples

The `python_examples/` directory contains comprehensive Python scripts for educational purposes and API integration training.

### Available Scripts

| Script | Purpose | Learning Focus |
|--------|---------|----------------|
| `basic_request.py` | Introduction to API requests | REST basics, JSON handling |
| `error_handling.py` | Proper error handling | Retries, exceptions, robustness |
| `data_processing.py` | Data analysis and export | Statistics, transformation, I/O |
| `integration_test.py` | Automated testing | Testing strategies, assertions |
| `service_integration.py` | Service-to-service integration | Pipelines, ETL, data sync |
| `rate_limit_test.py` | Rate limiting behavior | Throttling, backoff strategies |

### Quick Start with Python

1. **Install dependencies:**
   ```bash
   pip install -r python_examples/requirements.txt
   ```

2. **Run an example:**
   ```bash
   python python_examples/basic_request.py
   ```

3. **Run integration tests:**
   ```bash
   python python_examples/integration_test.py
   ```

### Use Cases

- **API Learning**: Understand REST API concepts and best practices
- **Integration Testing**: Test your services against generated data
- **Training**: Educational tool for teaching API integration
- **Development**: Generate test data for development
- **ETL Pipelines**: Example patterns for data transformation

See [python_examples/README.md](python_examples/README.md) for detailed documentation.

## 🎓 Educational Use Cases

This service is designed for:

1. **API Integration Training**
   - Learn how to consume REST APIs
   - Practice error handling and retry logic
   - Understand rate limiting

2. **Testing & QA**
   - Generate realistic test data
   - Test service integrations
   - Validate data pipelines

3. **Development & Prototyping**
   - Mock data for frontend development
   - Test API client libraries
   - Validate integration scenarios

4. **CI/CD & Automation**
   - Automated integration testing
   - Performance testing
   - Health check monitoring

## 📝 License

This project is provided as-is for educational and production use.

## 🤝 Contributing

This is a standalone service. Modify as needed for your requirements.

## 📞 Support

For issues or questions, refer to the SQLite and .NET 8 documentation:
- [.NET 8 Documentation](https://learn.microsoft.com/en-us/dotnet/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Microsoft.Data.Sqlite](https://learn.microsoft.com/en-us/dotnet/standard/data/sqlite/)
- [Requests Library](https://requests.readthedocs.io/) (for Python examples)
