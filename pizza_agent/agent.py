"""
Core Pizza Ordering Agent
Handles both API and phone-based pizza ordering
"""

import json
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from .models import Order, PizzaPlace, OrderStatus, CustomerInfo, Pizza
from .phone_handler import PhoneOrderHandler
from .api_handler import APIOrderHandler


class PizzaOrderingAgent:
    """
    Main agent class that coordinates pizza ordering through different channels
    """
    
    def __init__(self):
        self.phone_handler = PhoneOrderHandler()
        self.api_handler = APIOrderHandler()
        self.order_history: List[Order] = []
        
    def order_pizza(self, order: Order) -> Dict[str, Any]:
        """
        Main method to order pizza - automatically chooses API or phone based on pizza place capabilities
        """
        try:
            # Update order total
            order.total_amount = order.calculate_total
            order.order_time = datetime.now().isoformat()
            
            # Choose ordering method based on pizza place capabilities
            if order.pizza_place.supports_api and order.pizza_place.api_url:
                result = self._order_via_api(order)
            else:
                result = self._order_via_phone(order)
            
            # Store order in history
            self.order_history.append(order)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to place order: {str(e)}",
                "order_id": None
            }
    
    def _order_via_api(self, order: Order) -> Dict[str, Any]:
        """Order pizza through API"""
        return self.api_handler.place_order(order)
    
    def _order_via_phone(self, order: Order) -> Dict[str, Any]:
        """Order pizza through phone simulation"""
        return self.phone_handler.place_order(order)
    
    def check_order_status(self, order_id: str) -> Dict[str, Any]:
        """Check the status of an existing order"""
        # Find order in history
        order = next((o for o in self.order_history if o.id == order_id), None)
        
        if not order:
            return {"success": False, "error": "Order not found"}
        
        # Check status based on ordering method
        if order.pizza_place.supports_api:
            return self.api_handler.check_status(order_id, order.pizza_place)
        else:
            return self.phone_handler.check_status(order_id, order.pizza_place)
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order"""
        order = next((o for o in self.order_history if o.id == order_id), None)
        
        if not order:
            return {"success": False, "error": "Order not found"}
        
        # Cancel based on ordering method
        if order.pizza_place.supports_api:
            result = self.api_handler.cancel_order(order_id, order.pizza_place)
        else:
            result = self.phone_handler.cancel_order(order_id, order.pizza_place)
        
        if result.get("success"):
            order.status = OrderStatus.CANCELLED
        
        return result
    
    def get_order_history(self) -> List[Dict[str, Any]]:
        """Get all past orders"""
        return [
            {
                "id": order.id,
                "customer_name": order.customer.name,
                "pizza_place": order.pizza_place.name,
                "total_amount": order.total_amount,
                "status": order.status.value,
                "order_time": order.order_time,
                "pizzas": [
                    {
                        "name": pizza.name,
                        "size": pizza.size.value,
                        "toppings": [t.name for t in pizza.toppings],
                        "price": pizza.total_price
                    }
                    for pizza in order.pizzas
                ]
            }
            for order in self.order_history
        ]
    
    def suggest_pizza_places(self, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Suggest pizza places based on location (mock implementation)"""
        # This would integrate with a real location service in production
        mock_places = [
            {
                "name": "Tony's Pizza Palace",
                "phone": "555-0123",
                "supports_api": True,
                "api_url": "https://api.tonyspizza.com/orders",
                "rating": 4.5,
                "estimated_delivery": "30-45 minutes"
            },
            {
                "name": "Mario's Italian Kitchen",
                "phone": "555-0456",
                "supports_api": False,
                "rating": 4.2,
                "estimated_delivery": "45-60 minutes"
            },
            {
                "name": "Quick Slice Express",
                "phone": "555-0789",
                "supports_api": True,
                "api_url": "https://api.quickslice.com/v1/orders",
                "rating": 3.8,
                "estimated_delivery": "20-30 minutes"
            }
        ]
        
        return mock_places