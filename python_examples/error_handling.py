#!/usr/bin/env python3
"""
Error Handling Example
Demonstrates proper error handling with the StatusService API
"""

import requests
import json
import time
from typing import Optional, Dict, Any

BASE_URL = "http://localhost:5000"

class APIClient:
    """Simple API client with error handling"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a GET request with error handling
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            Exception: On API or network errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            # Check for HTTP errors
            if response.status_code >= 400:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                raise Exception(f"HTTP {response.status_code}: {error_data.get('error', 'Unknown error')}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to API. Is the service running?")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from API")

def example_safe_request():
    """Example of safe API request with error handling"""
    client = APIClient(BASE_URL)
    
    print("=" * 60)
    print("Error Handling Examples")
    print("=" * 60)
    
    # Example 1: Successful request
    print("\n1. Successful Request")
    print("-" * 60)
    try:
        data = client.get("/api/users", params={"count": 3})
        print(f"✓ Success: Received {data['count']} users")
        print(f"  First user: {data['data'][0]['username']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Example 2: Invalid count parameter
    print("\n2. Invalid Parameter (count > 100)")
    print("-" * 60)
    try:
        data = client.get("/api/users", params={"count": 150})
        print(f"✓ Success: {data}")
    except Exception as e:
        print(f"✗ Expected Error: {e}")
    
    # Example 3: Invalid endpoint
    print("\n3. Invalid Endpoint")
    print("-" * 60)
    try:
        data = client.get("/api/invalid")
        print(f"✓ Success: {data}")
    except Exception as e:
        print(f"✗ Expected Error: {e}")
    
    # Example 4: Invalid type parameter
    print("\n4. Invalid Type Parameter")
    print("-" * 60)
    try:
        data = client.get("/api/random", params={"type": "invalid", "count": 1})
        print(f"✓ Success: {data}")
    except Exception as e:
        print(f"✗ Expected Error: {e}")
    
    # Example 5: Retry logic with exponential backoff
    print("\n5. Retry Logic Example")
    print("-" * 60)
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            data = client.get("/api/products", params={"count": 2})
            print(f"✓ Success on attempt {attempt + 1}")
            print(f"  Received {data['count']} products")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"✗ Attempt {attempt + 1} failed: {e}")
                print(f"  Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"✗ All {max_retries} attempts failed: {e}")

def example_status_code_handling():
    """Example of handling different status codes"""
    print("\n" + "=" * 60)
    print("Status Code Handling Examples")
    print("=" * 60)
    
    test_cases = [
        (200, "OK"),
        (201, "Created"),
        (400, "Bad Request"),
        (404, "Not Found"),
        (500, "Internal Server Error"),
    ]
    
    for status_code, description in test_cases:
        print(f"\n{description} ({status_code})")
        print("-" * 60)
        try:
            response = requests.get(
                f"{BASE_URL}/status/{status_code}",
                params={"message": description}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Handle based on status code
            if response.status_code == 200:
                print("✓ Success")
            elif response.status_code == 201:
                print("✓ Resource created")
            elif response.status_code >= 400 and response.status_code < 500:
                print("✗ Client error")
            elif response.status_code >= 500:
                print("✗ Server error")
                
        except Exception as e:
            print(f"✗ Exception: {e}")

if __name__ == "__main__":
    example_safe_request()
    example_status_code_handling()
