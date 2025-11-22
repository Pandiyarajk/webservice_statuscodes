# Quick Start Guide - Educational API & Python Examples

This guide will get you up and running with the StatusService educational features in 5 minutes.

## Step 1: Start the Service

```bash
cd StatusService
dotnet run
```

The service will start on `http://localhost:5000`

## Step 2: Test the Educational Endpoints

Open a new terminal and try these commands:

### Get Sample Users
```bash
curl http://localhost:5000/api/users?count=5
```

You'll get JSON response with 5 random users including names, emails, ages, cities, etc.

### Get Sample Products
```bash
curl http://localhost:5000/api/products?count=3
```

Returns 3 random products with prices, categories, ratings, and inventory.

### Get Sample Orders
```bash
curl http://localhost:5000/api/orders?count=2
```

Returns 2 random orders with items, totals, and shipping information.

### Batch Request
```bash
curl "http://localhost:5000/api/batch?users=5&products=5&orders=2"
```

Get all three types of data in one request!

## Step 3: Run Python Examples

### Install Dependencies
```bash
pip install requests
# or
pip install -r python_examples/requirements.txt
```

### Run Basic Example
```bash
python python_examples/basic_request.py
```

This will demonstrate:
- Health check
- Fetching users, products, and orders
- Batch requests
- Status code testing

### Run Integration Tests
```bash
python python_examples/integration_test.py
```

This will run automated tests covering:
- All API endpoints
- Error handling
- Data consistency
- Performance

## Step 4: Process and Analyze Data

```bash
python python_examples/data_processing.py
```

This will:
- Fetch 50 users, products, and orders
- Perform statistical analysis
- Display insights (age distribution, price stats, order patterns)
- Export sample data to JSON files

## Step 5: Test Error Handling

```bash
python python_examples/error_handling.py
```

Learn how to:
- Handle HTTP errors
- Implement retry logic
- Use exponential backoff
- Build robust API clients

## Common Use Cases

### 1. Learning API Integration

Start with `basic_request.py` to understand:
- Making HTTP requests
- Working with JSON
- Using query parameters
- Handling responses

### 2. Building an Integration Test Suite

Use `integration_test.py` as a template:
- Write test assertions
- Validate data structures
- Test error conditions
- Measure performance

### 3. Service-to-Service Integration

Study `service_integration.py` for:
- Data pipeline patterns
- Data transformation
- Batch processing
- ETL workflows

### 4. Testing Rate Limiting

Run `rate_limit_test.py` to understand:
- Rate limiting behavior
- Handling 429 responses
- Exponential backoff
- Exempt endpoints

## Real-World Scenarios

### Scenario 1: Mock Data for Frontend Development

```bash
# Get data and save to file
curl "http://localhost:5000/api/batch?users=20&products=30&orders=15" > test_data.json
```

Use this data in your frontend application during development.

### Scenario 2: Integration Testing Pipeline

```python
# In your test suite
import requests

def test_user_integration():
    # Get test users from StatusService
    response = requests.get("http://localhost:5000/api/users?count=10")
    users = response.json()["data"]
    
    # Send to your actual service
    for user in users:
        response = requests.post("http://your-service/users", json=user)
        assert response.status_code == 200
```

### Scenario 3: Data Migration Testing

```python
# Test your ETL pipeline
from python_examples.service_integration import DataPipeline

pipeline = DataPipeline("http://localhost:5000")
pipeline.run_full_pipeline(
    users_count=100,
    products_count=100,
    orders_count=50,
    send_to_service=True  # When your service is ready
)
```

### Scenario 4: Load Testing

```bash
# Use Apache Bench or similar
ab -n 1000 -c 10 http://localhost:5000/api/users?count=10
```

## Tips & Best Practices

1. **Start Simple**: Begin with `basic_request.py` before moving to complex examples

2. **Use Sessions**: For multiple requests, use `requests.Session()` for better performance

3. **Handle Errors**: Always wrap API calls in try-except blocks

4. **Respect Rate Limits**: The service has rate limits - use them to practice handling throttling

5. **Test Integration**: Use the generated data to test your own services

6. **Export Fixtures**: Save generated data as test fixtures for your CI/CD pipeline

## Troubleshooting

### Service Not Running
```bash
# Check if service is running
curl http://localhost:5000/health

# If not, start it
cd StatusService && dotnet run
```

### Python Module Not Found
```bash
# Install dependencies
pip install requests
```

### Rate Limited
```bash
# Wait 60 seconds or use exempt endpoints
curl http://localhost:5000/health  # Not rate limited
```

## Next Steps

1. **Explore the Documentation**
   - Read [StatusService/README.md](StatusService/README.md)
   - Study [python_examples/README.md](python_examples/README.md)

2. **Customize for Your Needs**
   - Modify the Python scripts
   - Adjust data generation parameters
   - Create your own integration tests

3. **Integrate with Your Services**
   - Use as mock data source
   - Build integration test suites
   - Create data pipelines

4. **Share Your Learnings**
   - Create your own examples
   - Contribute improvements
   - Help others learn

## Resources

- [REST API Best Practices](https://restfulapi.net/)
- [Python Requests Documentation](https://requests.readthedocs.io/)
- [Integration Testing Guide](https://martinfowler.com/articles/microservice-testing/)
- [.NET 8 Documentation](https://learn.microsoft.com/en-us/dotnet/)

## Support

For questions or issues:
1. Check the README files
2. Review the example scripts
3. Look at the CHANGE_LOG.md for latest updates

Happy Learning! 🚀
