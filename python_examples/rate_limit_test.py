#!/usr/bin/env python3
"""
Rate Limiting Test Example
Demonstrates rate limiting behavior and how to handle it
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_rate_limiting():
    """
    Test the rate limiting functionality
    The service has:
    - Tier 1: 30 requests per minute (returns 429)
    - Tier 2: 200 requests in 10 minutes (blocks IP)
    """
    print("=" * 60)
    print("Rate Limiting Test")
    print("=" * 60)
    print("\nTesting rate limits...")
    print("Note: Health, logs, blocklist endpoints are NOT rate-limited")
    print("\nSending requests to rate-limited endpoint...")
    
    successful = 0
    rate_limited = 0
    errors = 0
    
    # Send 35 requests quickly (should hit the 30/minute limit)
    for i in range(35):
        try:
            response = requests.get(f"{BASE_URL}/api/users", params={"count": 1})
            
            if response.status_code == 200:
                successful += 1
                print(f"Request {i+1}: ✓ Success")
            elif response.status_code == 429:
                rate_limited += 1
                print(f"Request {i+1}: ⚠ Rate limited (429)")
                error_data = response.json()
                print(f"  Error: {error_data.get('error', 'Unknown')}")
            else:
                errors += 1
                print(f"Request {i+1}: ✗ Error {response.status_code}")
            
            time.sleep(0.1)  # Small delay between requests
            
        except Exception as e:
            errors += 1
            print(f"Request {i+1}: ✗ Exception: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Rate limited: {rate_limited}")
    print(f"Errors: {errors}")
    print(f"Total: {successful + rate_limited + errors}")
    
    if rate_limited > 0:
        print("\n✓ Rate limiting is working correctly!")
        print("  The service returned 429 after exceeding the limit.")
    else:
        print("\n⚠ No rate limiting detected.")
        print("  You may need to send requests faster or check configuration.")

def test_rate_limit_recovery():
    """
    Test recovery after being rate limited
    """
    print("\n" + "=" * 60)
    print("Rate Limit Recovery Test")
    print("=" * 60)
    
    # Hit the rate limit
    print("\nStep 1: Hitting rate limit...")
    for i in range(35):
        requests.get(f"{BASE_URL}/api/users", params={"count": 1})
    
    response = requests.get(f"{BASE_URL}/api/users", params={"count": 1})
    if response.status_code == 429:
        print("✓ Rate limited as expected")
        
        # Wait for rate limit window to reset
        print("\nStep 2: Waiting 65 seconds for rate limit to reset...")
        for remaining in range(65, 0, -5):
            print(f"  {remaining} seconds remaining...")
            time.sleep(5)
        
        # Try again
        print("\nStep 3: Attempting request after waiting...")
        response = requests.get(f"{BASE_URL}/api/users", params={"count": 1})
        if response.status_code == 200:
            print("✓ Request successful! Rate limit has reset.")
        else:
            print(f"✗ Still rate limited (Status: {response.status_code})")
    else:
        print("⚠ Was not rate limited initially")

def test_exempt_endpoints():
    """
    Test that certain endpoints are exempt from rate limiting
    """
    print("\n" + "=" * 60)
    print("Exempt Endpoints Test")
    print("=" * 60)
    print("\nTesting endpoints that should NOT be rate-limited...")
    
    exempt_endpoints = [
        "/health",
        "/logs?limit=5",
        "/blocklist"
    ]
    
    for endpoint in exempt_endpoints:
        print(f"\nTesting {endpoint}")
        print("-" * 40)
        
        successful = 0
        # Send many requests quickly
        for i in range(50):
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                if response.status_code == 200:
                    successful += 1
            except:
                pass
        
        print(f"Sent 50 requests: {successful} successful")
        if successful == 50:
            print("✓ Endpoint is NOT rate-limited (as expected)")
        else:
            print(f"⚠ Only {successful}/50 successful - may be rate-limited")

def demonstrate_backoff_strategy():
    """
    Demonstrate exponential backoff strategy for handling rate limits
    """
    print("\n" + "=" * 60)
    print("Exponential Backoff Strategy")
    print("=" * 60)
    print("\nDemonstrating how to handle rate limits gracefully...")
    
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/api/users", params={"count": 10})
            
            if response.status_code == 200:
                print(f"\nAttempt {attempt + 1}: ✓ Success")
                data = response.json()
                print(f"Received {data['count']} users")
                break
                
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"\nAttempt {attempt + 1}: ⚠ Rate limited")
                    print(f"Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                else:
                    print(f"\nAttempt {attempt + 1}: ✗ Max retries reached")
                    
        except Exception as e:
            print(f"\nAttempt {attempt + 1}: ✗ Error: {e}")

def main():
    """Run all rate limiting tests"""
    print("=" * 60)
    print("StatusService - Rate Limiting Examples")
    print("=" * 60)
    print("\n⚠ WARNING: These tests will trigger rate limits!")
    print("This is intentional to demonstrate the behavior.")
    
    try:
        # Test 1: Basic rate limiting
        test_rate_limiting()
        
        # Test 2: Exempt endpoints
        test_exempt_endpoints()
        
        # Test 3: Backoff strategy
        demonstrate_backoff_strategy()
        
        # Note: test_rate_limit_recovery() takes over a minute
        # Uncomment to run:
        # test_rate_limit_recovery()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to StatusService")
        print("Please make sure the service is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
