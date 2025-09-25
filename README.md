# 🍕 Pizza Ordering Agent

A Python-based pizza ordering agent that can handle complete pizza orders with various customization options.

## Features

- **Complete Menu System**: Supports different pizza sizes, crust types, and toppings
- **Order Management**: Start orders, add pizzas, view summaries, and confirm orders
- **Price Calculation**: Automatic pricing with base prices and topping costs
- **Customer Information**: Collects and manages customer details
- **Interactive CLI**: Command-line interface for easy interaction
- **Order Validation**: Input validation and error handling
- **Order Tracking**: Unique order IDs and status tracking

## Quick Start

### Basic Usage (Programmatic)

```python
from pizza_agent import PizzaOrderingAgent

# Create the agent
agent = PizzaOrderingAgent()

# Display menu
print(agent.display_menu())

# Start an order
agent.start_order("John Doe", "555-0123", "123 Main St", "john@example.com")

# Add pizzas
agent.add_pizza_to_order("large", "thin", ["pepperoni", "mushrooms"])
agent.add_pizza_to_order("medium", "thick", ["extra_cheese"])

# View order summary
print(agent.get_order_summary())

# Confirm order
print(agent.confirm_order())
```

### Interactive CLI

```bash
python3 pizza_cli.py
```

**Available Commands:**
- `menu` - Display the pizza menu
- `order` - Start a new order (requires customer info)
- `add` - Add a pizza to current order
- `summary` - Show current order summary
- `confirm` - Confirm and place the order
- `cancel` - Cancel the current order
- `help` - Show help message
- `quit` - Exit the program

## Menu Options

### Pizza Sizes
- **Small**: $12.99
- **Medium**: $15.99
- **Large**: $18.99
- **Extra Large**: $21.99

### Crust Types
- **Thin**: No extra charge
- **Thick**: +$1.00
- **Stuffed**: +$2.50
- **Gluten Free**: +$2.00

### Toppings (each)
- Pepperoni: +$2.00
- Sausage: +$2.00
- Extra Cheese: +$2.50
- Bacon: +$2.50
- Mushrooms: +$1.50
- Peppers: +$1.50
- Olives: +$1.50
- Pineapple: +$1.50
- Spinach: +$1.50
- Onions: +$1.00

## Example CLI Session

```
🍕 Welcome to the Interactive Pizza Ordering System! 🍕
Type 'help' for available commands or 'menu' to see our pizzas.

pizza> order
Enter customer information:
Name: Alice Smith
Phone: 555-0199
Address: 456 Oak Ave, Cityville, ST 67890
Email (optional): alice@example.com
✅ Order started for Alice Smith. Order ID: PZ0001

pizza> add
Available sizes: small, medium, large, extra_large
Available crusts: thin, thick, stuffed, gluten_free
Available toppings: pepperoni, mushrooms, sausage, peppers, onions, olives, extra_cheese, bacon, pineapple, spinach

Enter pizza details:
Size: large
Crust type: thin
Toppings (comma-separated, or 'none'): pepperoni, extra_cheese
✅ Added large thin pizza with pepperoni, extra_cheese - $23.49

pizza> summary

📋 ORDER SUMMARY - PZ0001
Customer: Alice Smith
Phone: 555-0199
Address: 456 Oak Ave, Cityville, ST 67890
Email: alice@example.com

PIZZAS:
  1. Large Thin pizza with pepperoni, extra_cheese - $23.49

TOTAL: $23.49
Status: Pending

pizza> confirm

📋 ORDER SUMMARY - PZ0001
Customer: Alice Smith
Phone: 555-0199
Address: 456 Oak Ave, Cityville, ST 67890
Email: alice@example.com

PIZZAS:
  1. Large Thin pizza with pepperoni, extra_cheese - $23.49

TOTAL: $23.49
Status: Pending

Confirm this order? (yes/no): yes
✅ Order PZ0001 confirmed!

📋 ORDER SUMMARY - PZ0001
Customer: Alice Smith
Phone: 555-0199
Address: 456 Oak Ave, Cityville, ST 67890
Email: alice@example.com

PIZZAS:
  1. Large Thin pizza with pepperoni, extra_cheese - $23.49

TOTAL: $23.49
Status: Confirmed

Estimated delivery time: 25-35 minutes
```

## Testing

Run the test suite to validate functionality:

```bash
python3 test_pizza_agent.py
```

The test suite includes comprehensive tests for:
- Menu initialization and display
- Pizza creation and price calculation
- Order management (start, add pizzas, confirm, cancel)
- Input validation and error handling
- Order totals and ID generation

## File Structure

- `pizza_agent.py` - Core pizza ordering agent class
- `pizza_cli.py` - Interactive command-line interface
- `test_pizza_agent.py` - Comprehensive test suite
- `README.md` - This documentation

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Architecture

The agent is built with a modular design:

1. **Data Models**: Uses Python dataclasses and enums for type safety
2. **Core Agent**: `PizzaOrderingAgent` class handles all business logic
3. **CLI Interface**: `PizzaOrderingCLI` provides user interaction
4. **Input Validation**: Comprehensive validation for all inputs
5. **Error Handling**: Graceful error handling with user-friendly messages

The agent maintains state for the current order and provides methods for all pizza ordering operations.