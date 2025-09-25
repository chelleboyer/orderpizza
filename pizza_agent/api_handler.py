"""
API-based pizza ordering handler
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from .models import Order, PizzaPlace, OrderStatus


class APIOrderHandler:
    """
    Handles pizza ordering through restaurant APIs
    """
    
    def __init__(self):
        self.timeout = 30
    
    def place_order(self, order: Order) -> Dict[str, Any]:
        """
        Place an order through the pizza place's API
        For demo purposes, this simulates API calls to various pizza places
        """
        try:
            # Generate order ID
            order.id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            # Prepare API payload
            payload = self._prepare_api_payload(order)
            
            # For demo purposes, we'll simulate different API responses
            # In production, this would make actual HTTP requests
            if order.pizza_place.name == "Tony's Pizza Palace":
                return self._simulate_tonys_api(order, payload)
            elif order.pizza_place.name == "Quick Slice Express":
                return self._simulate_quickslice_api(order, payload)
            else:
                return self._simulate_generic_api(order, payload)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"API order failed: {str(e)}",
                "order_id": None
            }
    
    def _prepare_api_payload(self, order: Order) -> Dict[str, Any]:
        """Prepare the API payload for the order"""
        return {
            "customer": {
                "name": order.customer.name,
                "phone": order.customer.phone,
                "address": order.customer.address,
                "email": order.customer.email
            },
            "items": [
                {
                    "name": pizza.name,
                    "size": pizza.size.value,
                    "toppings": [t.name for t in pizza.toppings],
                    "price": pizza.total_price
                }
                for pizza in order.pizzas
            ],
            "total": order.total_amount,
            "order_time": order.order_time
        }
    
    def _simulate_tonys_api(self, order: Order, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate Tony's Pizza Palace API"""
        # Simulate API call delay
        import time
        time.sleep(1)
        
        order.status = OrderStatus.CONFIRMED
        order.estimated_delivery = (datetime.now() + timedelta(minutes=35)).isoformat()
        
        return {
            "success": True,
            "message": "Order successfully placed at Tony's Pizza Palace!",
            "order_id": order.id,
            "estimated_delivery": order.estimated_delivery,
            "tracking_url": f"https://tonyspizza.com/track/{order.id}",
            "total": order.total_amount
        }
    
    def _simulate_quickslice_api(self, order: Order, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate Quick Slice Express API"""
        import time
        time.sleep(0.5)
        
        order.status = OrderStatus.CONFIRMED
        order.estimated_delivery = (datetime.now() + timedelta(minutes=25)).isoformat()
        
        return {
            "success": True,
            "message": "Express order confirmed at Quick Slice!",
            "order_id": order.id,
            "estimated_delivery": order.estimated_delivery,
            "status": "confirmed",
            "total": order.total_amount
        }
    
    def _simulate_generic_api(self, order: Order, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a generic pizza place API"""
        import time
        time.sleep(1.5)
        
        order.status = OrderStatus.CONFIRMED
        order.estimated_delivery = (datetime.now() + timedelta(minutes=40)).isoformat()
        
        return {
            "success": True,
            "message": f"Order placed successfully at {order.pizza_place.name}",
            "order_id": order.id,
            "estimated_delivery": order.estimated_delivery,
            "total": order.total_amount
        }
    
    def check_status(self, order_id: str, pizza_place: PizzaPlace) -> Dict[str, Any]:
        """Check order status through API"""
        try:
            # Simulate API status check
            import time
            time.sleep(0.5)
            
            # Mock status progression based on time since order
            statuses = [
                (0, OrderStatus.CONFIRMED, "Order confirmed and being prepared"),
                (10, OrderStatus.IN_PROGRESS, "Pizza is in the oven"),
                (25, OrderStatus.READY, "Order ready for pickup/delivery"),
                (35, OrderStatus.DELIVERED, "Order delivered")
            ]
            
            # For demo, we'll just return a random status
            import random
            status_info = random.choice(statuses)
            
            return {
                "success": True,
                "order_id": order_id,
                "status": status_info[1].value,
                "message": status_info[2],
                "estimated_delivery": (datetime.now() + timedelta(minutes=status_info[0])).isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to check order status: {str(e)}"
            }
    
    def cancel_order(self, order_id: str, pizza_place: PizzaPlace) -> Dict[str, Any]:
        """Cancel order through API"""
        try:
            # Simulate API cancellation
            import time
            time.sleep(0.5)
            
            return {
                "success": True,
                "message": f"Order {order_id} has been cancelled",
                "refund_amount": 0.0,  # Would calculate actual refund
                "cancellation_fee": 0.0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to cancel order: {str(e)}"
            }