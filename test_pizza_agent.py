#!/usr/bin/env python3
"""
Tests for the Pizza Ordering Agent

Simple test suite to validate the pizza ordering functionality.
"""

import unittest
from pizza_agent import PizzaOrderingAgent, PizzaSize, CrustType


class TestPizzaOrderingAgent(unittest.TestCase):
    """Test cases for the PizzaOrderingAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = PizzaOrderingAgent()
    
    def test_menu_initialization(self):
        """Test that the menu is properly initialized."""
        self.assertIsNotNone(self.agent.menu)
        self.assertIn("sizes", self.agent.menu)
        self.assertIn("crusts", self.agent.menu)
        self.assertIn("toppings", self.agent.menu)
    
    def test_display_menu(self):
        """Test menu display functionality."""
        menu_text = self.agent.display_menu()
        self.assertIn("PIZZA MENU", menu_text)
        self.assertIn("SIZES:", menu_text)
        self.assertIn("CRUST TYPES:", menu_text)
        self.assertIn("TOPPINGS:", menu_text)
    
    def test_calculate_pizza_price(self):
        """Test pizza price calculation."""
        # Basic pizza price
        price = self.agent.calculate_pizza_price(PizzaSize.LARGE, CrustType.THIN, [])
        expected = 18.99  # Large pizza base price
        self.assertEqual(price, expected)
        
        # Pizza with crust upgrade
        price = self.agent.calculate_pizza_price(PizzaSize.MEDIUM, CrustType.STUFFED, [])
        expected = round(15.99 + 2.50, 2)  # Medium + stuffed crust
        self.assertEqual(price, expected)
        
        # Pizza with toppings
        price = self.agent.calculate_pizza_price(PizzaSize.SMALL, CrustType.THIN, ["pepperoni", "mushrooms"])
        expected = round(12.99 + 2.00 + 1.50, 2)  # Small + pepperoni + mushrooms
        self.assertEqual(price, expected)
    
    def test_create_pizza_valid(self):
        """Test creating a valid pizza."""
        pizza = self.agent.create_pizza("large", "thin", ["pepperoni"])
        
        self.assertEqual(pizza.size, PizzaSize.LARGE)
        self.assertEqual(pizza.crust, CrustType.THIN)
        self.assertEqual(pizza.toppings, ["pepperoni"])
        self.assertEqual(pizza.price, 20.99)  # 18.99 + 2.00
    
    def test_create_pizza_invalid_size(self):
        """Test creating pizza with invalid size."""
        with self.assertRaises(ValueError):
            self.agent.create_pizza("huge", "thin", [])
    
    def test_create_pizza_invalid_crust(self):
        """Test creating pizza with invalid crust."""
        with self.assertRaises(ValueError):
            self.agent.create_pizza("large", "crispy", [])
    
    def test_create_pizza_invalid_toppings(self):
        """Test creating pizza with invalid toppings."""
        with self.assertRaises(ValueError):
            self.agent.create_pizza("large", "thin", ["invalid_topping"])
    
    def test_start_order(self):
        """Test starting a new order."""
        result = self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        
        self.assertIsNotNone(self.agent.current_order)
        self.assertEqual(self.agent.current_order.customer.name, "Test Customer")
        self.assertEqual(self.agent.current_order.customer.phone, "555-1234")
        self.assertEqual(self.agent.current_order.customer.address, "123 Test St")
        self.assertIn("Order started", result)
    
    def test_add_pizza_to_order(self):
        """Test adding pizza to an order."""
        # Start an order first
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        
        # Add a pizza
        result = self.agent.add_pizza_to_order("medium", "thin", ["pepperoni"])
        
        self.assertEqual(len(self.agent.current_order.pizzas), 1)
        self.assertEqual(self.agent.current_order.total, 17.99)  # 15.99 + 2.00
        self.assertIn("Added", result)
    
    def test_add_pizza_without_order(self):
        """Test adding pizza without an active order."""
        result = self.agent.add_pizza_to_order("medium", "thin", ["pepperoni"])
        self.assertIn("No active order", result)
    
    def test_get_order_summary(self):
        """Test getting order summary."""
        # Start order and add pizza
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        self.agent.add_pizza_to_order("large", "thick", ["pepperoni", "mushrooms"])
        
        summary = self.agent.get_order_summary()
        
        self.assertIn("ORDER SUMMARY", summary)
        self.assertIn("Test Customer", summary)
        self.assertIn("Large Thick pizza", summary)
        self.assertIn("TOTAL:", summary)
    
    def test_confirm_order(self):
        """Test order confirmation."""
        # Start order and add pizza
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        self.agent.add_pizza_to_order("medium", "thin", ["pepperoni"])
        
        result = self.agent.confirm_order()
        
        self.assertIn("confirmed", result)
        self.assertIn("delivery time", result)
        self.assertIsNone(self.agent.current_order)  # Should be cleared after confirmation
    
    def test_confirm_empty_order(self):
        """Test confirming an order with no pizzas."""
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        
        result = self.agent.confirm_order()
        self.assertIn("no pizzas", result)
    
    def test_cancel_order(self):
        """Test order cancellation."""
        # Start an order
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        order_id = self.agent.current_order.order_id
        
        result = self.agent.cancel_order()
        
        self.assertIn("cancelled", result)
        self.assertIn(order_id, result)
        self.assertIsNone(self.agent.current_order)
    
    def test_cancel_no_order(self):
        """Test cancelling when no order exists."""
        result = self.agent.cancel_order()
        self.assertIn("No active order", result)
    
    def test_multiple_pizzas_total(self):
        """Test that order total is calculated correctly with multiple pizzas."""
        self.agent.start_order("Test Customer", "555-1234", "123 Test St")
        
        # Add first pizza: medium thin with pepperoni = 15.99 + 2.00 = 17.99
        self.agent.add_pizza_to_order("medium", "thin", ["pepperoni"])
        
        # Add second pizza: large thick with mushrooms = 18.99 + 1.00 + 1.50 = 21.49
        self.agent.add_pizza_to_order("large", "thick", ["mushrooms"])
        
        expected_total = 17.99 + 21.49
        self.assertEqual(self.agent.current_order.total, expected_total)
    
    def test_order_id_increment(self):
        """Test that order IDs increment correctly."""
        # First order
        self.agent.start_order("Customer 1", "555-1234", "123 Test St")
        first_id = self.agent.current_order.order_id
        self.agent.add_pizza_to_order("medium", "thin", [])
        self.agent.confirm_order()
        
        # Second order
        self.agent.start_order("Customer 2", "555-5678", "456 Test Ave")
        second_id = self.agent.current_order.order_id
        
        self.assertNotEqual(first_id, second_id)
        self.assertTrue(first_id < second_id)


def run_tests():
    """Run all tests and display results."""
    print("🧪 Running Pizza Ordering Agent Tests...\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPizzaOrderingAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 TEST SUMMARY:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) failed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()