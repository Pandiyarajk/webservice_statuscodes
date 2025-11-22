# Python Examples for StatusService

This directory contains Python scripts demonstrating how to interact with the StatusService API for educational and training purposes.

## Prerequisites

- Python 3.7 or higher
- StatusService running on `http://localhost:5000`

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install requests
```

## Available Scripts

### 1. basic_request.py
**Purpose**: Introduction to making API requests

Demonstrates:
- Health check
- Fetching users, products, and orders
- Using query parameters
- Batch requests

**Usage**:
```bash
python basic_request.py
```

**Learning Outcomes**:
- Understanding REST API basics
- Working with JSON responses
- Using query parameters
- Handling different endpoints

---

### 2. error_handling.py
**Purpose**: Proper error handling with APIs

Demonstrates:
- HTTP error codes (400, 404, 500)
- Connection errors
- Timeout handling
- Retry logic with exponential backoff
- Custom API client class

**Usage**:
```bash
python error_handling.py
```

**Learning Outcomes**:
- Handling API errors gracefully
- Implementing retry strategies
- Building robust API clients
- Error recovery patterns

---

### 3. data_processing.py
**Purpose**: Fetching and analyzing data

Demonstrates:
- Fetching large datasets
- Data aggregation and statistics
- Data transformation
- Exporting to JSON files
- Statistical analysis

**Usage**:
```bash
python data_processing.py
```

**Learning Outcomes**:
- Processing API responses
- Data analysis with Python
- Working with collections
- File I/O operations

**Output Files**:
- `sample_users.json`
- `sample_products.json`
- `sample_orders.json`
- `sample_combined_data.json`

---

### 4. integration_test.py
**Purpose**: Automated integration testing

Demonstrates:
- Writing integration tests
- Test assertions
- Data validation
- Performance testing
- Test reporting

**Usage**:
```bash
python integration_test.py
```

**Test Suites**:
1. **API Endpoints Test**: Validates all endpoints return correct data
2. **Error Handling Test**: Validates error responses
3. **Data Consistency Test**: Validates data structure and types
4. **Performance Test**: Validates response times

**Learning Outcomes**:
- Writing automated tests
- API testing strategies
- Test organization
- Performance benchmarking

---

### 5. service_integration.py
**Purpose**: Service-to-service integration

Demonstrates:
- Data pipeline creation
- Data transformation for other services
- Batch processing
- Continuous synchronization
- Test fixture generation

**Usage**:
```bash
python service_integration.py
```

**Use Cases**:
- Integrating with external services
- Data migration
- ETL pipelines
- Test data generation
- Continuous sync

**Learning Outcomes**:
- Service integration patterns
- Data transformation
- Pipeline architecture
- Test fixture management

---

### 6. rate_limit_test.py
**Purpose**: Understanding and handling rate limits

Demonstrates:
- Rate limiting behavior
- Exempt endpoints
- Rate limit recovery
- Exponential backoff strategy
- Handling 429 responses

**Usage**:
```bash
python rate_limit_test.py
```

**⚠ Warning**: This script intentionally triggers rate limits!

**Learning Outcomes**:
- Rate limiting concepts
- Handling throttling
- Implementing backoff strategies
- Respecting API limits

---

## Quick Start

1. **Start the StatusService**:
   ```bash
   cd ../StatusService
   dotnet run
   ```

2. **Run any example**:
   ```bash
   python basic_request.py
   ```

## Common Patterns

### Making a Simple Request

```python
import requests

response = requests.get("http://localhost:5000/api/users", params={"count": 10})
data = response.json()
print(data)
```

### Error Handling

```python
import requests

try:
    response = requests.get("http://localhost:5000/api/users")
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### Using Sessions for Multiple Requests

```python
import requests

session = requests.Session()
users = session.get("http://localhost:5000/api/users").json()
products = session.get("http://localhost:5000/api/products").json()
```

## API Endpoints Reference

### Educational Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/users` | GET | `count` (1-100), `id` (optional) | Get random users |
| `/api/products` | GET | `count` (1-100), `id` (optional) | Get random products |
| `/api/orders` | GET | `count` (1-100), `id`, `userId` (optional) | Get random orders |
| `/api/random` | GET | `type` (user/product/order), `count` | Get random data |
| `/api/batch` | GET | `users`, `products`, `orders` (0-50) | Get multiple types |

### Utility Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/health` | GET | None | Health check |
| `/status/{code}` | GET | `message`, `delay`, `size` | Test status codes |
| `/logs` | GET | `limit` (default 100) | View logs |

## Response Format

All educational endpoints return data in this format:

```json
{
  "success": true,
  "count": 10,
  "data": [...],
  "timestamp": "2025-11-22T12:34:56.789Z"
}
```

## Sample Data Structures

### User
```json
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
```

### Product
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

### Order
```json
{
  "id": 100234,
  "userId": 12345,
  "status": "Delivered",
  "items": [...],
  "subtotal": 299.98,
  "tax": 23.99,
  "shipping": 12.50,
  "total": 336.47,
  "orderDate": "2025-11-15T09:20:00Z",
  "shippingAddress": {...}
}
```

## Tips for Learning

1. **Start Simple**: Begin with `basic_request.py` to understand the basics
2. **Add Error Handling**: Move to `error_handling.py` to write robust code
3. **Process Data**: Use `data_processing.py` to learn data manipulation
4. **Test Integration**: Use `integration_test.py` for automated testing
5. **Build Pipelines**: Use `service_integration.py` for real-world scenarios

## Troubleshooting

### Connection Refused
**Problem**: `ConnectionError: [Errno 111] Connection refused`

**Solution**: Make sure StatusService is running:
```bash
cd ../StatusService
dotnet run
```

### Import Error
**Problem**: `ModuleNotFoundError: No module named 'requests'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Rate Limited
**Problem**: Getting 429 errors

**Solution**: Wait 60 seconds or check exempt endpoints (health, logs, blocklist)

## Next Steps

After working through these examples, you can:

1. **Integrate with your own services**: Use the patterns from `service_integration.py`
2. **Build a dashboard**: Create a web UI that displays the data
3. **Automate testing**: Use `integration_test.py` as a template for CI/CD
4. **Create data pipelines**: Build ETL processes for data migration
5. **Learn API design**: Study the API patterns and implement your own

## Resources

- [Requests Documentation](https://requests.readthedocs.io/)
- [REST API Tutorial](https://restfulapi.net/)
- [Python JSON](https://docs.python.org/3/library/json.html)
- [Integration Testing Guide](https://martinfowler.com/articles/microservice-testing/)

## Contributing

Feel free to add your own examples and improve existing ones!

## License

These examples are provided for educational purposes.
