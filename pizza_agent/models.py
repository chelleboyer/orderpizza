"""
Data models for pizza ordering system
"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum


class PizzaSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PizzaTopping(BaseModel):
    name: str
    price: float = 0.0


class Pizza(BaseModel):
    name: str
    size: PizzaSize
    toppings: List[PizzaTopping] = Field(default_factory=list)
    base_price: float = 10.0
    
    @property
    def total_price(self) -> float:
        size_multiplier = {
            PizzaSize.SMALL: 0.8,
            PizzaSize.MEDIUM: 1.0,
            PizzaSize.LARGE: 1.3,
            PizzaSize.EXTRA_LARGE: 1.6
        }
        toppings_cost = sum(topping.price for topping in self.toppings)
        return (self.base_price + toppings_cost) * size_multiplier[self.size]


class CustomerInfo(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    email: Optional[str] = None


class PizzaPlace(BaseModel):
    name: str
    phone: str
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    supports_api: bool = False
    menu: List[Pizza] = Field(default_factory=list)


class Order(BaseModel):
    id: Optional[str] = None
    customer: CustomerInfo
    pizzas: List[Pizza]
    pizza_place: PizzaPlace
    status: OrderStatus = OrderStatus.PENDING
    total_amount: float = 0.0
    order_time: Optional[str] = None
    estimated_delivery: Optional[str] = None
    
    @property
    def calculate_total(self) -> float:
        return sum(pizza.total_price for pizza in self.pizzas)