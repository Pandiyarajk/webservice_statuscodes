#!/usr/bin/env python3
"""
Integration Testing Example
Demonstrates how to use the StatusService for integration testing
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional

BASE_URL = "http://localhost:5000"

class IntegrationTest:
    """Base class for integration tests"""
    
    def __init__(self, name: str):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.results: List[Dict[str, Any]] = []
    
    def assert_equals(self, actual: Any, expected: Any, description: str = "") -> bool:
        """Assert that two values are equal"""
        passed = actual == expected
        result = {
            "test": description or f"Assert {actual} == {expected}",
            "passed": passed,
            "actual": actual,
            "expected": expected
        }
        self.results.append(result)
        
        if passed:
            self.passed += 1
            print(f"  ✓ {result['test']}")
        else:
            self.failed += 1
            print(f"  ✗ {result['test']}")
            print(f"    Expected: {expected}")
            print(f"    Actual: {actual}")
        
        return passed
    
    def assert_true(self, condition: bool, description: str = "") -> bool:
        """Assert that a condition is true"""
        return self.assert_equals(condition, True, description)
    
    def assert_status_code(self, response: requests.Response, expected_code: int) -> bool:
        """Assert HTTP status code"""
        return self.assert_equals(
            response.status_code, 
            expected_code, 
            f"Status code is {expected_code}"
        )
    
    def assert_json_field(self, data: Dict, field: str, expected_value: Any = None) -> bool:
        """Assert that a JSON field exists and optionally has a specific value"""
        if field not in data:
            return self.assert_true(False, f"Field '{field}' exists in response")
        
        if expected_value is not None:
            return self.assert_equals(
                data[field], 
                expected_value, 
                f"Field '{field}' equals '{expected_value}'"
            )
        
        return self.assert_true(True, f"Field '{field}' exists in response")
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print(f"Test Summary: {self.name}")
        print("=" * 60)
        print(f"Total tests: {total}")
        print(f"Passed: {self.passed} ({success_rate:.1f}%)")
        print(f"Failed: {self.failed}")
        print("=" * 60)

def test_api_endpoints():
    """Test all API endpoints"""
    test = IntegrationTest("API Endpoints Test")
    
    print("\n" + "=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    
    # Test 1: Health endpoint
    print("\n1. Health Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health")
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_json_field(data, "status", "OK")
    test.assert_json_field(data, "time")
    
    # Test 2: Users endpoint
    print("\n2. Users Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 5})
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_json_field(data, "success", True)
    test.assert_json_field(data, "count", 5)
    test.assert_true(len(data["data"]) == 5, "Returned 5 users")
    test.assert_true("username" in data["data"][0], "User has username field")
    test.assert_true("email" in data["data"][0], "User has email field")
    
    # Test 3: Products endpoint
    print("\n3. Products Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/products", params={"count": 3})
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_json_field(data, "success", True)
    test.assert_true(len(data["data"]) == 3, "Returned 3 products")
    test.assert_true("price" in data["data"][0], "Product has price field")
    test.assert_true("category" in data["data"][0], "Product has category field")
    
    # Test 4: Orders endpoint
    print("\n4. Orders Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/orders", params={"count": 2})
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_true(len(data["data"]) == 2, "Returned 2 orders")
    test.assert_true("items" in data["data"][0], "Order has items field")
    test.assert_true("total" in data["data"][0], "Order has total field")
    
    # Test 5: Batch endpoint
    print("\n5. Batch Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/batch", params={
        "users": 2,
        "products": 3,
        "orders": 1
    })
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_true(len(data["data"]["users"]) == 2, "Returned 2 users")
    test.assert_true(len(data["data"]["products"]) == 3, "Returned 3 products")
    test.assert_true(len(data["data"]["orders"]) == 1, "Returned 1 order")
    
    # Test 6: Random endpoint
    print("\n6. Random Endpoint")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/random", params={"type": "user", "count": 3})
    test.assert_status_code(response, 200)
    data = response.json()
    test.assert_json_field(data, "type", "user")
    
    test.print_summary()
    return test

def test_error_handling():
    """Test error handling"""
    test = IntegrationTest("Error Handling Test")
    
    print("\n" + "=" * 60)
    print("Testing Error Handling")
    print("=" * 60)
    
    # Test 1: Invalid count (too high)
    print("\n1. Invalid Count (> 100)")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 150})
    test.assert_status_code(response, 400)
    data = response.json()
    test.assert_json_field(data, "error")
    
    # Test 2: Invalid count (too low)
    print("\n2. Invalid Count (< 1)")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 0})
    test.assert_status_code(response, 400)
    
    # Test 3: Invalid type
    print("\n3. Invalid Type Parameter")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/random", params={"type": "invalid"})
    test.assert_status_code(response, 400)
    
    # Test 4: Invalid status code
    print("\n4. Invalid Status Code")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/status/999")
    test.assert_status_code(response, 400)
    
    test.print_summary()
    return test

def test_data_consistency():
    """Test data consistency"""
    test = IntegrationTest("Data Consistency Test")
    
    print("\n" + "=" * 60)
    print("Testing Data Consistency")
    print("=" * 60)
    
    # Test 1: User data structure
    print("\n1. User Data Structure")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 1})
    user = response.json()["data"][0]
    required_fields = ["id", "username", "email", "firstName", "lastName", "age", "city"]
    for field in required_fields:
        test.assert_true(field in user, f"User has {field} field")
    
    # Test 2: Product data structure
    print("\n2. Product Data Structure")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/products", params={"count": 1})
    product = response.json()["data"][0]
    required_fields = ["id", "name", "category", "price", "inStock", "rating"]
    for field in required_fields:
        test.assert_true(field in product, f"Product has {field} field")
    
    # Test 3: Order data structure
    print("\n3. Order Data Structure")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/orders", params={"count": 1})
    order = response.json()["data"][0]
    required_fields = ["id", "userId", "status", "items", "total"]
    for field in required_fields:
        test.assert_true(field in order, f"Order has {field} field")
    
    # Test 4: Data types
    print("\n4. Data Type Validation")
    print("-" * 60)
    test.assert_true(isinstance(user["id"], int), "User ID is integer")
    test.assert_true(isinstance(user["age"], int), "User age is integer")
    test.assert_true(isinstance(product["price"], (int, float)), "Product price is numeric")
    test.assert_true(isinstance(order["items"], list), "Order items is list")
    
    test.print_summary()
    return test

def test_performance():
    """Test API performance"""
    test = IntegrationTest("Performance Test")
    
    print("\n" + "=" * 60)
    print("Testing API Performance")
    print("=" * 60)
    
    # Test 1: Response time for single request
    print("\n1. Single Request Response Time")
    print("-" * 60)
    start = time.time()
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 10})
    elapsed = time.time() - start
    test.assert_true(elapsed < 1.0, f"Response time < 1s (actual: {elapsed:.3f}s)")
    test.assert_status_code(response, 200)
    
    # Test 2: Batch request performance
    print("\n2. Batch Request Response Time")
    print("-" * 60)
    start = time.time()
    response = requests.get(f"{BASE_URL}/api/batch", params={
        "users": 20,
        "products": 20,
        "orders": 20
    })
    elapsed = time.time() - start
    test.assert_true(elapsed < 2.0, f"Batch response time < 2s (actual: {elapsed:.3f}s)")
    test.assert_status_code(response, 200)
    
    # Test 3: Multiple sequential requests
    print("\n3. Sequential Requests Performance")
    print("-" * 60)
    start = time.time()
    for _ in range(5):
        requests.get(f"{BASE_URL}/api/users", params={"count": 5})
    elapsed = time.time() - start
    test.assert_true(elapsed < 2.0, f"5 sequential requests < 2s (actual: {elapsed:.3f}s)")
    
    test.print_summary()
    return test

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("StatusService - Integration Tests")
    print("=" * 60)
    
    try:
        # Run all test suites
        test1 = test_api_endpoints()
        test2 = test_error_handling()
        test3 = test_data_consistency()
        test4 = test_performance()
        
        # Overall summary
        total_passed = test1.passed + test2.passed + test3.passed + test4.passed
        total_failed = test1.failed + test2.failed + test3.failed + test4.failed
        total_tests = total_passed + total_failed
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("Overall Test Summary")
        print("=" * 60)
        print(f"Total tests: {total_tests}")
        print(f"Passed: {total_passed} ({success_rate:.1f}%)")
        print(f"Failed: {total_failed}")
        print("=" * 60)
        
        if total_failed == 0:
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ {total_failed} test(s) failed")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to StatusService")
        print("Please make sure the service is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
