#!/usr/bin/env python3
"""
Data Processing Example
Demonstrates how to fetch data from the API and process it
"""

import requests
import json
from typing import List, Dict, Any
from collections import Counter
import statistics

BASE_URL = "http://localhost:5000"

def fetch_users(count: int = 50) -> List[Dict[str, Any]]:
    """Fetch random users from the API"""
    response = requests.get(f"{BASE_URL}/api/users", params={"count": count})
    response.raise_for_status()
    return response.json()["data"]

def fetch_products(count: int = 50) -> List[Dict[str, Any]]:
    """Fetch random products from the API"""
    response = requests.get(f"{BASE_URL}/api/products", params={"count": count})
    response.raise_for_status()
    return response.json()["data"]

def fetch_orders(count: int = 50) -> List[Dict[str, Any]]:
    """Fetch random orders from the API"""
    response = requests.get(f"{BASE_URL}/api/orders", params={"count": count})
    response.raise_for_status()
    return response.json()["data"]

def analyze_users(users: List[Dict[str, Any]]) -> None:
    """Analyze user data"""
    print("\n" + "=" * 60)
    print("User Data Analysis")
    print("=" * 60)
    
    # Age statistics
    ages = [user["age"] for user in users]
    print(f"\nAge Statistics:")
    print(f"  Average age: {statistics.mean(ages):.1f}")
    print(f"  Median age: {statistics.median(ages):.1f}")
    print(f"  Min age: {min(ages)}")
    print(f"  Max age: {max(ages)}")
    
    # City distribution
    cities = [user["city"] for user in users]
    city_counts = Counter(cities)
    print(f"\nTop 5 Cities:")
    for city, count in city_counts.most_common(5):
        print(f"  {city}: {count} users ({count/len(users)*100:.1f}%)")
    
    # Active vs inactive
    active_count = sum(1 for user in users if user["isActive"])
    print(f"\nUser Status:")
    print(f"  Active: {active_count} ({active_count/len(users)*100:.1f}%)")
    print(f"  Inactive: {len(users) - active_count} ({(len(users)-active_count)/len(users)*100:.1f}%)")
    
    # Credits statistics
    credits = [user["credits"] for user in users]
    print(f"\nCredits Statistics:")
    print(f"  Average credits: ${statistics.mean(credits):.2f}")
    print(f"  Total credits: ${sum(credits):.2f}")

def analyze_products(products: List[Dict[str, Any]]) -> None:
    """Analyze product data"""
    print("\n" + "=" * 60)
    print("Product Data Analysis")
    print("=" * 60)
    
    # Price statistics
    prices = [product["price"] for product in products]
    print(f"\nPrice Statistics:")
    print(f"  Average price: ${statistics.mean(prices):.2f}")
    print(f"  Median price: ${statistics.median(prices):.2f}")
    print(f"  Min price: ${min(prices):.2f}")
    print(f"  Max price: ${max(prices):.2f}")
    
    # Category distribution
    categories = [product["category"] for product in products]
    category_counts = Counter(categories)
    print(f"\nCategory Distribution:")
    for category, count in category_counts.most_common():
        print(f"  {category}: {count} products ({count/len(products)*100:.1f}%)")
    
    # Rating statistics
    ratings = [product["rating"] for product in products]
    print(f"\nRating Statistics:")
    print(f"  Average rating: {statistics.mean(ratings):.2f} stars")
    print(f"  Median rating: {statistics.median(ratings):.2f} stars")
    
    # Stock analysis
    in_stock = sum(1 for product in products if product["inStock"] > 0)
    print(f"\nStock Status:")
    print(f"  In stock: {in_stock} ({in_stock/len(products)*100:.1f}%)")
    print(f"  Out of stock: {len(products) - in_stock} ({(len(products)-in_stock)/len(products)*100:.1f}%)")

def analyze_orders(orders: List[Dict[str, Any]]) -> None:
    """Analyze order data"""
    print("\n" + "=" * 60)
    print("Order Data Analysis")
    print("=" * 60)
    
    # Order totals
    totals = [order["total"] for order in orders]
    print(f"\nOrder Value Statistics:")
    print(f"  Average order: ${statistics.mean(totals):.2f}")
    print(f"  Median order: ${statistics.median(totals):.2f}")
    print(f"  Min order: ${min(totals):.2f}")
    print(f"  Max order: ${max(totals):.2f}")
    print(f"  Total revenue: ${sum(totals):.2f}")
    
    # Status distribution
    statuses = [order["status"] for order in orders]
    status_counts = Counter(statuses)
    print(f"\nOrder Status Distribution:")
    for status, count in status_counts.most_common():
        print(f"  {status}: {count} orders ({count/len(orders)*100:.1f}%)")
    
    # Item count statistics
    item_counts = [len(order["items"]) for order in orders]
    print(f"\nItems per Order:")
    print(f"  Average items: {statistics.mean(item_counts):.1f}")
    print(f"  Max items in an order: {max(item_counts)}")
    
    # Shipping address analysis
    cities = [order["shippingAddress"]["city"] for order in orders]
    city_counts = Counter(cities)
    print(f"\nTop 5 Shipping Destinations:")
    for city, count in city_counts.most_common(5):
        print(f"  {city}: {count} orders")

def export_to_json(data: Any, filename: str) -> None:
    """Export data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Exported data to {filename}")

def main():
    print("=" * 60)
    print("StatusService - Data Processing Examples")
    print("=" * 60)
    
    try:
        # Fetch data
        print("\nFetching data from API...")
        users = fetch_users(50)
        products = fetch_products(50)
        orders = fetch_orders(50)
        print(f"✓ Fetched {len(users)} users, {len(products)} products, {len(orders)} orders")
        
        # Analyze data
        analyze_users(users)
        analyze_products(products)
        analyze_orders(orders)
        
        # Export examples
        print("\n" + "=" * 60)
        print("Data Export Examples")
        print("=" * 60)
        export_to_json(users[:10], "sample_users.json")
        export_to_json(products[:10], "sample_products.json")
        export_to_json(orders[:5], "sample_orders.json")
        
        # Combined export
        combined_data = {
            "users": users[:10],
            "products": products[:10],
            "orders": orders[:5],
            "generated_at": requests.get(f"{BASE_URL}/health").json()["time"]
        }
        export_to_json(combined_data, "sample_combined_data.json")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to StatusService")
        print("Please make sure the service is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
