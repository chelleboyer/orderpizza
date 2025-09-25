#!/usr/bin/env python3
"""
Demo script to test the pizza ordering agent functionality
"""

from pizza_agent import PizzaOrderingAgent


def run_demo():
    """Run a demonstration of the pizza ordering agent."""
    print("🍕 PIZZA ORDERING AGENT DEMO 🍕\n")
    
    # Create agent
    agent = PizzaOrderingAgent()
    
    print("1. Displaying Menu:")
    print("=" * 50)
    print(agent.display_menu())
    
    print("\n2. Starting an Order:")
    print("=" * 50)
    result = agent.start_order("Demo Customer", "555-DEMO", "123 Demo Street", "demo@example.com")
    print(result)
    
    print("\n3. Adding Pizzas:")
    print("=" * 50)
    
    # Add first pizza
    result1 = agent.add_pizza_to_order("large", "thin", ["pepperoni", "mushrooms"])
    print(result1)
    
    # Add second pizza
    result2 = agent.add_pizza_to_order("medium", "stuffed", ["extra_cheese", "sausage"])
    print(result2)
    
    # Add third pizza (plain)
    result3 = agent.add_pizza_to_order("small", "gluten_free", [])
    print(result3)
    
    print("\n4. Order Summary:")
    print("=" * 50)
    print(agent.get_order_summary())
    
    print("\n5. Confirming Order:")
    print("=" * 50)
    result = agent.confirm_order()
    print(result)
    
    print("\n6. Testing Error Handling:")
    print("=" * 50)
    
    # Try to add pizza without order
    result = agent.add_pizza_to_order("large", "thin", ["pepperoni"])
    print(f"Add pizza without order: {result}")
    
    # Try to create pizza with invalid size
    try:
        agent.create_pizza("gigantic", "thin", [])
    except ValueError as e:
        print(f"Invalid size error: {e}")
    
    # Try to create pizza with invalid toppings
    try:
        agent.create_pizza("large", "thin", ["chocolate"])
    except ValueError as e:
        print(f"Invalid topping error: {e}")
    
    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    run_demo()