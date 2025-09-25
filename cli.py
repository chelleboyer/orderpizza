#!/usr/bin/env python3
"""
Pizza Ordering CLI
Interactive command-line interface for the pizza ordering agent
"""

import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from pizza_agent.agent import PizzaOrderingAgent
from pizza_agent.models import (
    Order, Pizza, PizzaTopping, CustomerInfo, PizzaPlace, 
    PizzaSize, OrderStatus
)

app = typer.Typer(help="🍕 Pizza Ordering Agent - Order pizza through API or phone!")
console = Console()
agent = PizzaOrderingAgent()


def get_pizza_size() -> PizzaSize:
    """Interactive pizza size selection"""
    sizes = list(PizzaSize)
    console.print("\n🍕 Available sizes:")
    for i, size in enumerate(sizes, 1):
        console.print(f"  {i}. {size.value.replace('_', ' ').title()}")
    
    while True:
        try:
            choice = int(Prompt.ask("Select pizza size", default="2")) - 1
            if 0 <= choice < len(sizes):
                return sizes[choice]
            console.print("❌ Invalid choice, please try again")
        except ValueError:
            console.print("❌ Please enter a number")


def get_toppings() -> List[PizzaTopping]:
    """Interactive toppings selection"""
    available_toppings = [
        PizzaTopping(name="Pepperoni", price=2.0),
        PizzaTopping(name="Mushrooms", price=1.5),
        PizzaTopping(name="Sausage", price=2.0),
        PizzaTopping(name="Bell Peppers", price=1.5),
        PizzaTopping(name="Onions", price=1.0),
        PizzaTopping(name="Extra Cheese", price=2.5),
        PizzaTopping(name="Olives", price=1.5),
        PizzaTopping(name="Bacon", price=3.0),
    ]
    
    console.print("\n🧄 Available toppings:")
    for i, topping in enumerate(available_toppings, 1):
        console.print(f"  {i}. {topping.name} (+${topping.price:.2f})")
    
    console.print("\nEnter topping numbers separated by commas (or press Enter for no toppings):")
    
    toppings_input = Prompt.ask("Toppings", default="")
    selected_toppings = []
    
    if toppings_input.strip():
        try:
            indices = [int(x.strip()) - 1 for x in toppings_input.split(',')]
            for idx in indices:
                if 0 <= idx < len(available_toppings):
                    selected_toppings.append(available_toppings[idx])
        except ValueError:
            console.print("❌ Invalid input, using no toppings")
    
    return selected_toppings


def get_customer_info() -> CustomerInfo:
    """Get customer information"""
    console.print("\n👤 Customer Information:")
    name = Prompt.ask("Your name")
    phone = Prompt.ask("Phone number")
    address = Prompt.ask("Delivery address", default="")
    email = Prompt.ask("Email (optional)", default="")
    
    return CustomerInfo(
        name=name,
        phone=phone,
        address=address if address else None,
        email=email if email else None
    )


def select_pizza_place() -> PizzaPlace:
    """Select a pizza place"""
    places = agent.suggest_pizza_places()
    
    console.print("\n🏪 Available pizza places:")
    table = Table()
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Phone", style="yellow")
    table.add_column("API Support", style="blue")
    table.add_column("Rating", style="magenta")
    table.add_column("Delivery Time", style="white")
    
    for i, place in enumerate(places, 1):
        api_support = "✅" if place["supports_api"] else "📞"
        table.add_row(
            str(i),
            place["name"],
            place["phone"],
            api_support,
            f"{place['rating']}/5",
            place["estimated_delivery"]
        )
    
    console.print(table)
    
    while True:
        try:
            choice = int(Prompt.ask("Select pizza place", default="1")) - 1
            if 0 <= choice < len(places):
                selected = places[choice]
                return PizzaPlace(
                    name=selected["name"],
                    phone=selected["phone"],
                    api_url=selected.get("api_url"),
                    supports_api=selected["supports_api"]
                )
            console.print("❌ Invalid choice, please try again")
        except ValueError:
            console.print("❌ Please enter a number")


@app.command()
def order():
    """🍕 Place a new pizza order"""
    console.print(Panel.fit("🍕 Welcome to Pizza Ordering Agent!", style="bold green"))
    
    # Get customer information
    customer = get_customer_info()
    
    # Select pizza place
    pizza_place = select_pizza_place()
    
    # Build pizza order
    pizzas = []
    
    while True:
        console.print(f"\n🍕 Pizza #{len(pizzas) + 1}")
        pizza_name = Prompt.ask("Pizza name", default="Margherita")
        size = get_pizza_size()
        toppings = get_toppings()
        
        pizza = Pizza(name=pizza_name, size=size, toppings=toppings)
        pizzas.append(pizza)
        
        console.print(f"\n✨ Pizza added: {pizza.name} ({size.value}) - ${pizza.total_price:.2f}")
        
        if not Confirm.ask("Add another pizza?"):
            break
    
    # Create and place order
    order = Order(
        customer=customer,
        pizzas=pizzas,
        pizza_place=pizza_place
    )
    
    console.print(f"\n💰 Order total: ${order.calculate_total:.2f}")
    
    if Confirm.ask("Place this order?"):
        with console.status("Placing your order..."):
            result = agent.order_pizza(order)
        
        if result["success"]:
            console.print(Panel(
                f"✅ Order placed successfully!\n"
                f"Order ID: {result['order_id']}\n"
                f"Total: ${result['total']:.2f}\n"
                f"Estimated delivery: {result.get('estimated_delivery', 'TBD')}",
                title="Order Confirmed",
                style="green"
            ))
        else:
            console.print(Panel(
                f"❌ Order failed: {result['error']}",
                title="Order Failed",
                style="red"
            ))
    else:
        console.print("❌ Order cancelled")


@app.command()
def status(order_id: str = typer.Argument(help="Order ID to check")):
    """📋 Check order status"""
    with console.status(f"Checking status for order {order_id}..."):
        result = agent.check_order_status(order_id)
    
    if result["success"]:
        console.print(Panel(
            f"Order ID: {result['order_id']}\n"
            f"Status: {result['status']}\n"
            f"Message: {result['message']}",
            title="Order Status",
            style="blue"
        ))
    else:
        console.print(Panel(
            f"❌ {result['error']}",
            title="Status Check Failed",
            style="red"
        ))


@app.command()
def cancel(order_id: str = typer.Argument(help="Order ID to cancel")):
    """❌ Cancel an order"""
    if Confirm.ask(f"Are you sure you want to cancel order {order_id}?"):
        with console.status(f"Cancelling order {order_id}..."):
            result = agent.cancel_order(order_id)
        
        if result["success"]:
            console.print(Panel(
                f"✅ {result['message']}",
                title="Order Cancelled",
                style="yellow"
            ))
        else:
            console.print(Panel(
                f"❌ {result['error']}",
                title="Cancellation Failed",
                style="red"
            ))
    else:
        console.print("Cancellation aborted")


@app.command()
def history():
    """📚 View order history"""
    orders = agent.get_order_history()
    
    if not orders:
        console.print("📭 No orders found")
        return
    
    table = Table()
    table.add_column("Order ID", style="cyan")
    table.add_column("Customer", style="green")
    table.add_column("Restaurant", style="yellow")
    table.add_column("Total", style="magenta")
    table.add_column("Status", style="blue")
    table.add_column("Time", style="white")
    
    for order in orders:
        table.add_row(
            order["id"],
            order["customer_name"],
            order["pizza_place"],
            f"${order['total_amount']:.2f}",
            order["status"],
            order["order_time"][:19] if order["order_time"] else "N/A"
        )
    
    console.print(table)


@app.command()
def places():
    """🏪 List available pizza places"""
    places = agent.suggest_pizza_places()
    
    table = Table()
    table.add_column("Name", style="green")
    table.add_column("Phone", style="yellow")
    table.add_column("API Support", style="blue")
    table.add_column("Rating", style="magenta")
    table.add_column("Delivery Time", style="white")
    
    for place in places:
        api_support = "✅ API" if place["supports_api"] else "📞 Phone Only"
        table.add_row(
            place["name"],
            place["phone"],
            api_support,
            f"{place['rating']}/5 ⭐",
            place["estimated_delivery"]
        )
    
    console.print(table)


if __name__ == "__main__":
    app()