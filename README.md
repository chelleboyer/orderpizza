# 🍕 Pizza Ordering Agent

An intelligent agentic application that can order pizza through restaurant APIs or by simulating phone calls to pizza places. This system automatically chooses the best ordering method based on the restaurant's capabilities.

## Features

- 🤖 **Intelligent Agent**: Automatically selects API or phone ordering based on restaurant capabilities
- 🍕 **Pizza Customization**: Support for different sizes, toppings, and custom pizzas
- 📞 **Phone Orders**: Simulates phone calls for restaurants without APIs
- 🔗 **API Integration**: Handles API-based ordering for modern pizza places
- 📋 **Order Management**: Track order status, cancel orders, and view history
- 💳 **Pricing**: Automatic price calculation with size and topping modifiers
- 🏪 **Restaurant Directory**: Built-in database of pizza places with ratings and delivery times

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chelleboyer/orderpizza.git
cd orderpizza
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The easiest way to use the pizza ordering agent is through the interactive CLI:

```bash
python cli.py order
```

This will guide you through:
1. Entering your customer information
2. Selecting a pizza place
3. Customizing your pizza(s)
4. Placing the order

#### Other CLI Commands

- **Check order status**: `python cli.py status ORDER_ID`
- **Cancel an order**: `python cli.py cancel ORDER_ID`
- **View order history**: `python cli.py history`
- **List pizza places**: `python cli.py places`

### Programmatic Usage

You can also use the agent programmatically in your Python code:

```python
from pizza_agent.agent import PizzaOrderingAgent
from pizza_agent.models import Order, Pizza, CustomerInfo, PizzaPlace, PizzaSize

# Create agent
agent = PizzaOrderingAgent()

# Create customer
customer = CustomerInfo(
    name="John Doe",
    phone="555-1234", 
    address="123 Main St"
)

# Create pizza place
pizza_place = PizzaPlace(
    name="Tony's Pizza Palace",
    phone="555-0123",
    supports_api=True,
    api_url="https://api.tonyspizza.com/orders"
)

# Create pizza
pizza = Pizza(
    name="Pepperoni Pizza",
    size=PizzaSize.LARGE,
    base_price=12.0
)

# Create and place order
order = Order(customer=customer, pizzas=[pizza], pizza_place=pizza_place)
result = agent.order_pizza(order)

if result["success"]:
    print(f"Order placed! ID: {result['order_id']}")
else:
    print(f"Order failed: {result['error']}")
```

See `example.py` for a complete example.

## Architecture

### Core Components

1. **PizzaOrderingAgent**: Main orchestrator that handles order routing
2. **APIOrderHandler**: Handles API-based orders for modern restaurants
3. **PhoneOrderHandler**: Simulates phone-based ordering for traditional restaurants
4. **Models**: Pydantic data models for type safety and validation

### Order Flow

```
User Request → PizzaOrderingAgent → API/Phone Handler → Restaurant → Confirmation
```

The agent automatically determines whether to use API or phone ordering based on the restaurant's capabilities.

### Supported Restaurants

The system comes with three demo pizza places:

- **Tony's Pizza Palace**: API-enabled, fast delivery (30-45 min)
- **Mario's Italian Kitchen**: Phone-only, traditional (45-60 min)  
- **Quick Slice Express**: API-enabled, fastest delivery (20-30 min)

## Configuration

Copy `.env.example` to `.env` and customize settings:

- **API timeouts**
- **Phone call simulation delays**
- **Default pizza places**
- **API keys for real integrations**

## API vs Phone Ordering

### API Ordering
- ✅ Instant confirmation
- ✅ Real-time status updates
- ✅ Automatic order tracking
- ✅ Digital receipts

### Phone Ordering
- 📞 Human-like interaction simulation
- 📞 Handles traditional restaurants
- 📞 Confirmation numbers provided
- 📞 Status updates via callback simulation

## Error Handling

The system includes comprehensive error handling:
- Network timeouts for API calls
- Busy phone lines (with retry logic)
- Invalid menu items
- Payment processing issues
- Delivery address validation

## Testing

Run the example script to test the system:

```bash
python example.py
```

This will demonstrate both API and phone ordering workflows.

## Future Enhancements

- 🌐 Integration with real pizza restaurant APIs
- 🎙️ Voice AI integration for actual phone calls  
- 📱 Mobile app interface
- 🗺️ GPS location services for restaurant discovery
- 💳 Real payment processing
- 🚚 Delivery tracking integration
- 📊 Analytics and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

Made with ❤️ for pizza lovers everywhere! 🍕