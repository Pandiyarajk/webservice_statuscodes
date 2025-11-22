using System.Text.Json;

namespace StatusService.Services;

public class DataGenerationService
{
    private static readonly Random _random = new Random();
    
    private static readonly string[] FirstNames = {
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa"
    };
    
    private static readonly string[] LastNames = {
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"
    };
    
    private static readonly string[] Cities = {
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
        "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville"
    };
    
    private static readonly string[] ProductCategories = {
        "Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys",
        "Beauty", "Automotive", "Food", "Health"
    };
    
    private static readonly string[] ProductAdjectives = {
        "Premium", "Deluxe", "Pro", "Ultra", "Smart", "Eco", "Advanced", "Classic",
        "Modern", "Vintage", "Compact", "Wireless"
    };
    
    private static readonly string[] ProductNouns = {
        "Widget", "Gadget", "Device", "Tool", "Kit", "Set", "System", "Solution",
        "Package", "Bundle", "Collection", "Series"
    };
    
    private static readonly string[] OrderStatuses = {
        "Pending", "Processing", "Shipped", "Delivered", "Cancelled"
    };
    
    public object GenerateUser(int? id = null)
    {
        var userId = id ?? _random.Next(1000, 99999);
        var firstName = FirstNames[_random.Next(FirstNames.Length)];
        var lastName = LastNames[_random.Next(LastNames.Length)];
        
        return new
        {
            id = userId,
            username = $"{firstName.ToLower()}.{lastName.ToLower()}{_random.Next(10, 99)}",
            email = $"{firstName.ToLower()}.{lastName.ToLower()}@example.com",
            firstName = firstName,
            lastName = lastName,
            age = _random.Next(18, 75),
            city = Cities[_random.Next(Cities.Length)],
            phone = $"+1-{_random.Next(200, 999)}-{_random.Next(100, 999)}-{_random.Next(1000, 9999)}",
            registeredAt = DateTime.UtcNow.AddDays(-_random.Next(1, 365)).ToString("o"),
            isActive = _random.Next(0, 10) > 1,
            credits = Math.Round(_random.NextDouble() * 1000, 2)
        };
    }
    
    public object GenerateProduct(int? id = null)
    {
        var productId = id ?? _random.Next(1000, 99999);
        var category = ProductCategories[_random.Next(ProductCategories.Length)];
        var adjective = ProductAdjectives[_random.Next(ProductAdjectives.Length)];
        var noun = ProductNouns[_random.Next(ProductNouns.Length)];
        
        return new
        {
            id = productId,
            name = $"{adjective} {noun}",
            category = category,
            price = Math.Round(_random.NextDouble() * 500 + 10, 2),
            description = $"High-quality {adjective.ToLower()} {noun.ToLower()} for all your {category.ToLower()} needs",
            inStock = _random.Next(0, 100),
            rating = Math.Round(_random.NextDouble() * 2 + 3, 1),
            reviews = _random.Next(0, 500),
            sku = $"{category.Substring(0, 3).ToUpper()}-{_random.Next(1000, 9999)}",
            weight = Math.Round(_random.NextDouble() * 10 + 0.5, 2),
            createdAt = DateTime.UtcNow.AddDays(-_random.Next(30, 730)).ToString("o")
        };
    }
    
    public object GenerateOrder(int? id = null, int? userId = null)
    {
        var orderId = id ?? _random.Next(10000, 999999);
        var itemCount = _random.Next(1, 6);
        var items = new List<object>();
        var total = 0.0;
        
        for (int i = 0; i < itemCount; i++)
        {
            var price = Math.Round(_random.NextDouble() * 100 + 10, 2);
            var quantity = _random.Next(1, 4);
            items.Add(new
            {
                productId = _random.Next(1000, 9999),
                productName = $"{ProductAdjectives[_random.Next(ProductAdjectives.Length)]} {ProductNouns[_random.Next(ProductNouns.Length)]}",
                quantity = quantity,
                price = price,
                subtotal = Math.Round(price * quantity, 2)
            });
            total += price * quantity;
        }
        
        return new
        {
            id = orderId,
            userId = userId ?? _random.Next(1000, 9999),
            status = OrderStatuses[_random.Next(OrderStatuses.Length)],
            items = items,
            subtotal = Math.Round(total, 2),
            tax = Math.Round(total * 0.08, 2),
            shipping = Math.Round(_random.NextDouble() * 20 + 5, 2),
            total = Math.Round(total * 1.08 + _random.NextDouble() * 20 + 5, 2),
            orderDate = DateTime.UtcNow.AddDays(-_random.Next(0, 60)).ToString("o"),
            shippingAddress = new
            {
                street = $"{_random.Next(100, 9999)} {LastNames[_random.Next(LastNames.Length)]} Street",
                city = Cities[_random.Next(Cities.Length)],
                state = "CA",
                zipCode = $"{_random.Next(10000, 99999)}"
            }
        };
    }
    
    public List<object> GenerateUsers(int count)
    {
        var users = new List<object>();
        for (int i = 0; i < count; i++)
        {
            users.Add(GenerateUser());
        }
        return users;
    }
    
    public List<object> GenerateProducts(int count)
    {
        var products = new List<object>();
        for (int i = 0; i < count; i++)
        {
            products.Add(GenerateProduct());
        }
        return products;
    }
    
    public List<object> GenerateOrders(int count)
    {
        var orders = new List<object>();
        for (int i = 0; i < count; i++)
        {
            orders.Add(GenerateOrder());
        }
        return orders;
    }
    
    public object GenerateRandomData(string type, int count = 1)
    {
        return type.ToLower() switch
        {
            "user" => count == 1 ? GenerateUser() : GenerateUsers(count),
            "product" => count == 1 ? GenerateProduct() : GenerateProducts(count),
            "order" => count == 1 ? GenerateOrder() : GenerateOrders(count),
            _ => new { error = $"Unknown type: {type}. Use 'user', 'product', or 'order'" }
        };
    }
}
