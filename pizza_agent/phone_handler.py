"""
Phone-based pizza ordering handler
Simulates calling a pizza place to place orders
"""

import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Any
from .models import Order, PizzaPlace, OrderStatus


class PhoneOrderHandler:
    """
    Handles pizza ordering through phone calls (simulated)
    In a real implementation, this could integrate with voice AI services
    """
    
    def __init__(self):
        self.call_simulation_delay = 3  # seconds
    
    def place_order(self, order: Order) -> Dict[str, Any]:
        """
        Place an order by calling the pizza place
        This simulates the phone ordering process
        """
        try:
            # Generate order ID
            order.id = f"PHONE-{uuid.uuid4().hex[:8].upper()}"
            
            # Simulate phone call process
            call_result = self._simulate_phone_call(order)
            
            if call_result["success"]:
                order.status = OrderStatus.CONFIRMED
                order.estimated_delivery = call_result["estimated_delivery"]
                
                return {
                    "success": True,
                    "message": f"Phone order placed successfully at {order.pizza_place.name}",
                    "order_id": order.id,
                    "estimated_delivery": order.estimated_delivery,
                    "total": order.total_amount,
                    "confirmation_number": call_result.get("confirmation_number"),
                    "phone_number": order.pizza_place.phone
                }
            else:
                return call_result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Phone order failed: {str(e)}",
                "order_id": None
            }
    
    def _simulate_phone_call(self, order: Order) -> Dict[str, Any]:
        """
        Simulate the phone call process
        In production, this would use voice AI or human agents
        """
        print(f"📞 Calling {order.pizza_place.name} at {order.pizza_place.phone}...")
        time.sleep(self.call_simulation_delay)
        
        # Simulate different call scenarios
        scenarios = [
            self._successful_call_scenario,
            self._busy_line_scenario,
            self._successful_call_scenario,  # Weight success higher
            self._successful_call_scenario,
        ]
        
        import random
        scenario = random.choice(scenarios)
        return scenario(order)
    
    def _successful_call_scenario(self, order: Order) -> Dict[str, Any]:
        """Simulate a successful phone order"""
        print("📞 Connected! Placing order...")
        
        # Simulate conversation
        conversation_steps = [
            "Hello, I'd like to place an order for delivery",
            f"Customer name: {order.customer.name}",
            f"Phone number: {order.customer.phone}",
            f"Address: {order.customer.address or 'Not provided'}",
            "Here's my order:"
        ]
        
        for step in conversation_steps:
            print(f"  🗣️  {step}")
            time.sleep(0.5)
        
        # List pizzas
        for i, pizza in enumerate(order.pizzas, 1):
            toppings_str = ", ".join([t.name for t in pizza.toppings]) if pizza.toppings else "no toppings"
            print(f"  🍕 Pizza {i}: {pizza.size.value} {pizza.name} with {toppings_str}")
            time.sleep(0.3)
        
        print(f"  💰 Total: ${order.total_amount:.2f}")
        time.sleep(1)
        
        confirmation_number = f"CONF-{uuid.uuid4().hex[:6].upper()}"
        estimated_delivery = (datetime.now() + timedelta(minutes=45)).isoformat()
        
        print(f"  ✅ Order confirmed! Confirmation: {confirmation_number}")
        print(f"  🚚 Estimated delivery: 45 minutes")
        
        return {
            "success": True,
            "confirmation_number": confirmation_number,
            "estimated_delivery": estimated_delivery
        }
    
    def _busy_line_scenario(self, order: Order) -> Dict[str, Any]:
        """Simulate a busy phone line"""
        print("📞 Line is busy... trying again...")
        time.sleep(2)
        
        # Try again with success
        return self._successful_call_scenario(order)
    
    def check_status(self, order_id: str, pizza_place: PizzaPlace) -> Dict[str, Any]:
        """Check order status by calling the restaurant"""
        try:
            print(f"📞 Calling {pizza_place.name} to check order {order_id}...")
            time.sleep(self.call_simulation_delay)
            
            # Simulate status check call
            statuses = [
                (OrderStatus.CONFIRMED, "Your order is being prepared"),
                (OrderStatus.IN_PROGRESS, "Your pizza is currently in the oven"),
                (OrderStatus.READY, "Your order is ready for pickup"),
                (OrderStatus.DELIVERED, "Your order has been delivered")
            ]
            
            import random
            status, message = random.choice(statuses)
            
            print(f"  📋 Status: {message}")
            
            return {
                "success": True,
                "order_id": order_id,
                "status": status.value,
                "message": message
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to check order status by phone: {str(e)}"
            }
    
    def cancel_order(self, order_id: str, pizza_place: PizzaPlace) -> Dict[str, Any]:
        """Cancel order by calling the restaurant"""
        try:
            print(f"📞 Calling {pizza_place.name} to cancel order {order_id}...")
            time.sleep(self.call_simulation_delay)
            
            print("  🗣️  I'd like to cancel my order")
            print(f"  🗣️  Order ID: {order_id}")
            time.sleep(1)
            print("  ✅ Order has been cancelled")
            
            return {
                "success": True,
                "message": f"Order {order_id} has been cancelled by phone",
                "refund_amount": 0.0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to cancel order by phone: {str(e)}"
            }