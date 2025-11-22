#!/usr/bin/env python3
"""
Service-to-Service Integration Example
Demonstrates how to use StatusService as a data provider for another service
"""

import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

# Configuration
STATUS_SERVICE_URL = "http://localhost:5000"
# Simulate another service endpoint (you can replace with real service)
TARGET_SERVICE_URL = "http://localhost:8000"  # Your actual service URL

class DataPipeline:
    """
    Example data pipeline that fetches data from StatusService
    and processes it for another service
    """
    
    def __init__(self, source_url: str):
        self.source_url = source_url
        self.session = requests.Session()
        self.stats = {
            "requests": 0,
            "successful": 0,
            "failed": 0,
            "records_processed": 0
        }
    
    def fetch_users(self, count: int) -> List[Dict[str, Any]]:
        """Fetch users from StatusService"""
        try:
            self.stats["requests"] += 1
            response = self.session.get(
                f"{self.source_url}/api/users",
                params={"count": count}
            )
            response.raise_for_status()
            data = response.json()["data"]
            self.stats["successful"] += 1
            self.stats["records_processed"] += len(data)
            return data
        except Exception as e:
            self.stats["failed"] += 1
            print(f"Error fetching users: {e}")
            return []
    
    def fetch_products(self, count: int) -> List[Dict[str, Any]]:
        """Fetch products from StatusService"""
        try:
            self.stats["requests"] += 1
            response = self.session.get(
                f"{self.source_url}/api/products",
                params={"count": count}
            )
            response.raise_for_status()
            data = response.json()["data"]
            self.stats["successful"] += 1
            self.stats["records_processed"] += len(data)
            return data
        except Exception as e:
            self.stats["failed"] += 1
            print(f"Error fetching products: {e}")
            return []
    
    def fetch_orders(self, count: int) -> List[Dict[str, Any]]:
        """Fetch orders from StatusService"""
        try:
            self.stats["requests"] += 1
            response = self.session.get(
                f"{self.source_url}/api/orders",
                params={"count": count}
            )
            response.raise_for_status()
            data = response.json()["data"]
            self.stats["successful"] += 1
            self.stats["records_processed"] += len(data)
            return data
        except Exception as e:
            self.stats["failed"] += 1
            print(f"Error fetching orders: {e}")
            return []
    
    def transform_user_for_target_service(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Transform user data for target service format"""
        return {
            "external_id": user["id"],
            "full_name": f"{user['firstName']} {user['lastName']}",
            "email": user["email"],
            "location": user["city"],
            "phone_number": user["phone"],
            "account_status": "active" if user["isActive"] else "inactive",
            "balance": user["credits"],
            "imported_at": datetime.utcnow().isoformat()
        }
    
    def transform_product_for_target_service(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Transform product data for target service format"""
        return {
            "external_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "unit_price": product["price"],
            "quantity_available": product["inStock"],
            "average_rating": product["rating"],
            "review_count": product["reviews"],
            "sku_code": product["sku"],
            "imported_at": datetime.utcnow().isoformat()
        }
    
    def process_and_send(self, data_type: str, count: int, transform_func, 
                         send_to_service: bool = False):
        """
        Generic method to fetch, transform, and optionally send data
        """
        print(f"\n{'=' * 60}")
        print(f"Processing {data_type.title()}")
        print(f"{'=' * 60}")
        
        # Fetch data based on type
        if data_type == "users":
            raw_data = self.fetch_users(count)
        elif data_type == "products":
            raw_data = self.fetch_products(count)
        elif data_type == "orders":
            raw_data = self.fetch_orders(count)
        else:
            print(f"Unknown data type: {data_type}")
            return []
        
        print(f"Fetched {len(raw_data)} {data_type}")
        
        # Transform data
        transformed_data = [transform_func(item) for item in raw_data]
        print(f"Transformed {len(transformed_data)} {data_type}")
        
        # Display sample
        if transformed_data:
            print(f"\nSample transformed {data_type[:-1]}:")
            print(json.dumps(transformed_data[0], indent=2))
        
        # Optionally send to target service
        if send_to_service and transformed_data:
            print(f"\nSending to target service...")
            # This is where you would actually send to your service
            # For demonstration, we'll just simulate it
            success = self.simulate_send_to_service(data_type, transformed_data)
            if success:
                print(f"✓ Successfully sent {len(transformed_data)} {data_type} to target service")
            else:
                print(f"✗ Failed to send {data_type} to target service")
        
        return transformed_data
    
    def simulate_send_to_service(self, data_type: str, data: List[Dict]) -> bool:
        """
        Simulate sending data to another service
        Replace this with actual API call to your service
        """
        # Example: POST to your actual service
        # try:
        #     response = requests.post(
        #         f"{TARGET_SERVICE_URL}/import/{data_type}",
        #         json={"items": data},
        #         headers={"Content-Type": "application/json"}
        #     )
        #     return response.status_code == 200
        # except Exception as e:
        #     print(f"Error sending to service: {e}")
        #     return False
        
        # For demonstration, just return success
        time.sleep(0.1)  # Simulate network delay
        return True
    
    def run_full_pipeline(self, users_count: int = 10, products_count: int = 10, 
                          orders_count: int = 5, send_to_service: bool = False):
        """Run the complete data pipeline"""
        print("=" * 60)
        print("Running Full Data Pipeline")
        print("=" * 60)
        print(f"Source: {self.source_url}")
        print(f"Target: {TARGET_SERVICE_URL if send_to_service else 'Simulation Mode'}")
        print(f"Timestamp: {datetime.utcnow().isoformat()}")
        
        start_time = time.time()
        
        # Process users
        users = self.process_and_send(
            "users", 
            users_count, 
            self.transform_user_for_target_service,
            send_to_service
        )
        
        # Process products
        products = self.process_and_send(
            "products",
            products_count,
            self.transform_product_for_target_service,
            send_to_service
        )
        
        elapsed = time.time() - start_time
        
        # Print statistics
        print("\n" + "=" * 60)
        print("Pipeline Statistics")
        print("=" * 60)
        print(f"Total API requests: {self.stats['requests']}")
        print(f"Successful requests: {self.stats['successful']}")
        print(f"Failed requests: {self.stats['failed']}")
        print(f"Records processed: {self.stats['records_processed']}")
        print(f"Execution time: {elapsed:.2f}s")
        print(f"Records/second: {self.stats['records_processed']/elapsed:.2f}")
        print("=" * 60)

def example_continuous_sync():
    """
    Example of continuous data synchronization
    Useful for keeping test data in sync between services
    """
    print("\n" + "=" * 60)
    print("Continuous Sync Example (Ctrl+C to stop)")
    print("=" * 60)
    
    pipeline = DataPipeline(STATUS_SERVICE_URL)
    sync_interval = 30  # seconds
    iteration = 0
    
    print(f"Syncing every {sync_interval} seconds...")
    print("This would typically run as a background service or cron job")
    print("\n(This is just a demonstration - will run 3 iterations)")
    
    try:
        for iteration in range(3):
            iteration += 1
            print(f"\n--- Sync Iteration {iteration} ---")
            
            # Fetch fresh data
            users = pipeline.fetch_users(5)
            products = pipeline.fetch_products(5)
            
            print(f"Synced {len(users)} users and {len(products)} products")
            
            # In a real scenario, you would:
            # 1. Transform the data
            # 2. Compare with existing data in target service
            # 3. Only update changed records
            # 4. Log sync results
            
            if iteration < 3:
                print(f"Waiting {sync_interval} seconds until next sync...")
                time.sleep(sync_interval)
    
    except KeyboardInterrupt:
        print("\n\nSync stopped by user")
    
    print(f"\nTotal syncs completed: {iteration}")

def example_batch_export():
    """
    Example of batch data export for integration testing
    """
    print("\n" + "=" * 60)
    print("Batch Export for Integration Testing")
    print("=" * 60)
    
    # Fetch a large batch of test data
    response = requests.get(
        f"{STATUS_SERVICE_URL}/api/batch",
        params={
            "users": 50,
            "products": 50,
            "orders": 50
        }
    )
    
    if response.status_code == 200:
        data = response.json()["data"]
        
        # Create test fixtures for different scenarios
        test_fixtures = {
            "smoke_test": {
                "users": data["users"][:5],
                "products": data["products"][:5],
                "orders": data["orders"][:5]
            },
            "load_test": {
                "users": data["users"][:25],
                "products": data["products"][:25],
                "orders": data["orders"][:25]
            },
            "full_integration": {
                "users": data["users"],
                "products": data["products"],
                "orders": data["orders"]
            }
        }
        
        # Export fixtures
        for test_type, fixture_data in test_fixtures.items():
            filename = f"test_fixture_{test_type}.json"
            with open(filename, 'w') as f:
                json.dump(fixture_data, f, indent=2)
            print(f"✓ Exported {filename}")
            print(f"  - {len(fixture_data['users'])} users")
            print(f"  - {len(fixture_data['products'])} products")
            print(f"  - {len(fixture_data['orders'])} orders")
        
        print("\nThese fixtures can be used for:")
        print("  • Unit testing")
        print("  • Integration testing")
        print("  • Load testing")
        print("  • Development seed data")

def main():
    """Main demonstration"""
    print("=" * 60)
    print("StatusService - Service Integration Examples")
    print("=" * 60)
    
    try:
        # Example 1: Basic pipeline
        pipeline = DataPipeline(STATUS_SERVICE_URL)
        pipeline.run_full_pipeline(
            users_count=10,
            products_count=10,
            orders_count=5,
            send_to_service=False  # Set to True when you have a real target service
        )
        
        # Example 2: Batch export for testing
        example_batch_export()
        
        # Example 3: Continuous sync (commented out by default)
        # example_continuous_sync()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to StatusService")
        print("Please make sure the service is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
