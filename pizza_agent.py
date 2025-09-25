#!/usr/bin/env python3
"""
Pizza Ordering Agent

A simple agent that can take pizza orders with various customization options.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class PizzaSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


class CrustType(Enum):
    THIN = "thin"
    THICK = "thick"
    STUFFED = "stuffed"
    GLUTEN_FREE = "gluten_free"


@dataclass
class Pizza:
    size: PizzaSize
    crust: CrustType
    toppings: List[str]
    price: float


@dataclass
class Customer:
    name: str
    phone: str
    address: str
    email: Optional[str] = None


@dataclass
class Order:
    customer: Customer
    pizzas: List[Pizza]
    total: float
    order_id: str
    status: str = "pending"


class PizzaOrderingAgent:
    """Main pizza ordering agent class."""
    
    def __init__(self):
        self.menu = self._initialize_menu()
        self.current_order = None
        self.order_counter = 1
        
    def _initialize_menu(self) -> Dict:
        """Initialize the pizza menu with prices and options."""
        return {
            "sizes": {
                PizzaSize.SMALL: 12.99,
                PizzaSize.MEDIUM: 15.99,
                PizzaSize.LARGE: 18.99,
                PizzaSize.EXTRA_LARGE: 21.99
            },
            "crusts": {
                CrustType.THIN: 0.00,
                CrustType.THICK: 1.00,
                CrustType.STUFFED: 2.50,
                CrustType.GLUTEN_FREE: 2.00
            },
            "toppings": {
                "pepperoni": 2.00,
                "mushrooms": 1.50,
                "sausage": 2.00,
                "peppers": 1.50,
                "onions": 1.00,
                "olives": 1.50,
                "extra_cheese": 2.50,
                "bacon": 2.50,
                "pineapple": 1.50,
                "spinach": 1.50
            }
        }
    
    def display_menu(self) -> str:
        """Display the complete menu with prices."""
        menu_text = "🍕 PIZZA MENU 🍕\n\n"
        
        menu_text += "SIZES:\n"
        for size, price in self.menu["sizes"].items():
            menu_text += f"  {size.value.replace('_', ' ').title()}: ${price:.2f}\n"
        
        menu_text += "\nCRUST TYPES:\n"
        for crust, price in self.menu["crusts"].items():
            extra = f" (+${price:.2f})" if price > 0 else ""
            menu_text += f"  {crust.value.replace('_', ' ').title()}{extra}\n"
        
        menu_text += "\nTOPPINGS:\n"
        for topping, price in self.menu["toppings"].items():
            menu_text += f"  {topping.replace('_', ' ').title()}: +${price:.2f}\n"
        
        return menu_text
    
    def calculate_pizza_price(self, size: PizzaSize, crust: CrustType, toppings: List[str]) -> float:
        """Calculate the total price for a pizza."""
        price = self.menu["sizes"][size]
        price += self.menu["crusts"][crust]
        
        for topping in toppings:
            if topping in self.menu["toppings"]:
                price += self.menu["toppings"][topping]
        
        return round(price, 2)
    
    def create_pizza(self, size: str, crust: str, toppings: List[str]) -> Pizza:
        """Create a pizza with the specified options."""
        try:
            pizza_size = PizzaSize(size.lower())
            crust_type = CrustType(crust.lower())
        except ValueError as e:
            raise ValueError(f"Invalid size or crust type: {e}")
        
        # Validate toppings
        invalid_toppings = [t for t in toppings if t.lower() not in self.menu["toppings"]]
        if invalid_toppings:
            raise ValueError(f"Invalid toppings: {invalid_toppings}")
        
        # Normalize topping names
        normalized_toppings = [t.lower() for t in toppings]
        
        price = self.calculate_pizza_price(pizza_size, crust_type, normalized_toppings)
        
        return Pizza(
            size=pizza_size,
            crust=crust_type,
            toppings=normalized_toppings,
            price=price
        )
    
    def start_order(self, customer_name: str, phone: str, address: str, email: str = None) -> str:
        """Start a new order with customer information."""
        customer = Customer(
            name=customer_name,
            phone=phone,
            address=address,
            email=email
        )
        
        self.current_order = Order(
            customer=customer,
            pizzas=[],
            total=0.0,
            order_id=f"PZ{self.order_counter:04d}"
        )
        
        self.order_counter += 1
        return f"Order started for {customer_name}. Order ID: {self.current_order.order_id}"
    
    def add_pizza_to_order(self, size: str, crust: str, toppings: List[str]) -> str:
        """Add a pizza to the current order."""
        if not self.current_order:
            return "No active order. Please start an order first."
        
        try:
            pizza = self.create_pizza(size, crust, toppings)
            self.current_order.pizzas.append(pizza)
            self.current_order.total = sum(p.price for p in self.current_order.pizzas)
            
            return f"Added {pizza.size.value} {pizza.crust.value} pizza with {', '.join(pizza.toppings) if pizza.toppings else 'no toppings'} - ${pizza.price:.2f}"
        except ValueError as e:
            return f"Error adding pizza: {e}"
    
    def get_order_summary(self) -> str:
        """Get a summary of the current order."""
        if not self.current_order:
            return "No active order."
        
        summary = f"\n📋 ORDER SUMMARY - {self.current_order.order_id}\n"
        summary += f"Customer: {self.current_order.customer.name}\n"
        summary += f"Phone: {self.current_order.customer.phone}\n"
        summary += f"Address: {self.current_order.customer.address}\n"
        
        if self.current_order.customer.email:
            summary += f"Email: {self.current_order.customer.email}\n"
        
        summary += f"\nPIZZAS:\n"
        for i, pizza in enumerate(self.current_order.pizzas, 1):
            toppings_str = f" with {', '.join(pizza.toppings)}" if pizza.toppings else ""
            summary += f"  {i}. {pizza.size.value.title()} {pizza.crust.value.replace('_', ' ').title()} pizza{toppings_str} - ${pizza.price:.2f}\n"
        
        summary += f"\nTOTAL: ${self.current_order.total:.2f}\n"
        summary += f"Status: {self.current_order.status.title()}\n"
        
        return summary
    
    def confirm_order(self) -> str:
        """Confirm and finalize the current order."""
        if not self.current_order:
            return "No active order to confirm."
        
        if not self.current_order.pizzas:
            return "Cannot confirm order: no pizzas added."
        
        self.current_order.status = "confirmed"
        order_summary = self.get_order_summary()
        
        # Clear current order after confirmation
        confirmed_order_id = self.current_order.order_id
        self.current_order = None
        
        return f"✅ Order {confirmed_order_id} confirmed!\n{order_summary}\nEstimated delivery time: 25-35 minutes"
    
    def cancel_order(self) -> str:
        """Cancel the current order."""
        if not self.current_order:
            return "No active order to cancel."
        
        cancelled_id = self.current_order.order_id
        self.current_order = None
        return f"❌ Order {cancelled_id} has been cancelled."


def main():
    """Main function for testing the pizza ordering agent."""
    agent = PizzaOrderingAgent()
    
    print("🍕 Welcome to the Pizza Ordering Agent! 🍕\n")
    print(agent.display_menu())
    
    # Example order flow
    print("\n" + "="*50)
    print("EXAMPLE ORDER:")
    print("="*50)
    
    # Start an order
    result = agent.start_order("John Doe", "555-0123", "123 Main St, Anytown, ST 12345", "john@example.com")
    print(result)
    
    # Add some pizzas
    print(agent.add_pizza_to_order("large", "thin", ["pepperoni", "mushrooms"]))
    print(agent.add_pizza_to_order("medium", "thick", ["extra_cheese", "sausage", "peppers"]))
    
    # Show order summary
    print(agent.get_order_summary())
    
    # Confirm order
    print(agent.confirm_order())


if __name__ == "__main__":
    main()