"""
Example script showing how to use the Pizza Ordering Agent programmatically
"""

from pizza_agent.agent import PizzaOrderingAgent
from pizza_agent.models import (
    Order, Pizza, PizzaTopping, CustomerInfo, PizzaPlace, PizzaSize
)

def main():
    # Create the agent
    agent = PizzaOrderingAgent()
    
    # Create customer info
    customer = CustomerInfo(
        name="John Doe",
        phone="555-1234",
        address="123 Main St, City, State 12345",
        email="john@example.com"
    )
    
    # Create pizza place (API-enabled)
    pizza_place = PizzaPlace(
        name="Tony's Pizza Palace",
        phone="555-0123",
        api_url="https://api.tonyspizza.com/orders",
        supports_api=True
    )
    
    # Create pizzas
    toppings = [
        PizzaTopping(name="Pepperoni", price=2.0),
        PizzaTopping(name="Extra Cheese", price=2.5)
    ]
    
    pizza1 = Pizza(
        name="Supreme Pizza",
        size=PizzaSize.LARGE,
        toppings=toppings,
        base_price=12.0
    )
    
    pizza2 = Pizza(
        name="Margherita",
        size=PizzaSize.MEDIUM,
        toppings=[],
        base_price=10.0
    )
    
    # Create order
    order = Order(
        customer=customer,
        pizzas=[pizza1, pizza2],
        pizza_place=pizza_place
    )
    
    print("🍕 Placing pizza order...")
    print(f"Customer: {customer.name}")
    print(f"Restaurant: {pizza_place.name} ({'API' if pizza_place.supports_api else 'Phone'})")
    print(f"Pizzas: {len(order.pizzas)}")
    print(f"Total: ${order.calculate_total:.2f}")
    print()
    
    # Place the order
    result = agent.order_pizza(order)
    
    if result["success"]:
        print("✅ Order placed successfully!")
        print(f"Order ID: {result['order_id']}")
        print(f"Message: {result['message']}")
        print(f"Estimated delivery: {result.get('estimated_delivery', 'TBD')}")
        
        # Check order status
        print("\n📋 Checking order status...")
        status_result = agent.check_order_status(result['order_id'])
        if status_result["success"]:
            print(f"Status: {status_result['status']}")
            print(f"Message: {status_result['message']}")
        
    else:
        print("❌ Order failed!")
        print(f"Error: {result['error']}")
    
    # Show order history
    print("\n📚 Order History:")
    history = agent.get_order_history()
    for order_info in history:
        print(f"- Order {order_info['id']}: {order_info['customer_name']} - ${order_info['total_amount']:.2f} ({order_info['status']})")
    
    # Show available pizza places
    print("\n🏪 Available Pizza Places:")
    places = agent.suggest_pizza_places()
    for place in places:
        api_type = "API" if place["supports_api"] else "Phone"
        print(f"- {place['name']} ({api_type}) - Rating: {place['rating']}/5")

if __name__ == "__main__":
    main()