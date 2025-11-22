#!/usr/bin/env python3
"""
Basic API Request Example
Demonstrates simple GET requests to the StatusService API
"""

import requests
import json

# Base URL for the StatusService
BASE_URL = "http://localhost:5000"

def main():
    print("=" * 60)
    print("StatusService - Basic Request Examples")
    print("=" * 60)
    
    # Example 1: Health Check
    print("\n1. Health Check")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Example 2: Get Users
    print("\n2. Get 5 Random Users")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 5})
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Success: {data['success']}")
    print(f"Count: {data['count']}")
    print(f"First User: {json.dumps(data['data'][0], indent=2)}")
    
    # Example 3: Get Products
    print("\n3. Get 3 Random Products")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/products", params={"count": 3})
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Products: {json.dumps(data['data'], indent=2)}")
    
    # Example 4: Get Single Order
    print("\n4. Get Single Order with ID")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/orders", params={"id": 12345})
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Order: {json.dumps(data['data'], indent=2)}")
    
    # Example 5: Test Status Code
    print("\n5. Test 404 Status Code")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/status/404", params={"message": "Not Found"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Example 6: Batch Request
    print("\n6. Batch Request - Get Multiple Types")
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/api/batch", params={
        "users": 2,
        "products": 2,
        "orders": 2
    })
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Counts: {json.dumps(data['counts'], indent=2)}")
    print(f"Total items returned: Users={len(data['data']['users'])}, "
          f"Products={len(data['data']['products'])}, Orders={len(data['data']['orders'])}")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to StatusService")
        print("Please make sure the service is running on http://localhost:5000")
        print("Start it with: cd StatusService && dotnet run")
    except Exception as e:
        print(f"\n❌ Error: {e}")
