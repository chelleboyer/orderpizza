#!/usr/bin/env python3
"""
Interactive Pizza Ordering CLI

An interactive command-line interface for the pizza ordering agent.
"""

import sys
from pizza_agent import PizzaOrderingAgent


class PizzaOrderingCLI:
    """Interactive CLI for pizza ordering."""
    
    def __init__(self):
        self.agent = PizzaOrderingAgent()
        self.commands = {
            'menu': self.show_menu,
            'order': self.start_order,
            'add': self.add_pizza,
            'summary': self.show_summary,
            'confirm': self.confirm_order,
            'cancel': self.cancel_order,
            'help': self.show_help,
            'quit': self.quit_cli
        }
    
    def show_help(self):
        """Display available commands."""
        help_text = """
🍕 PIZZA ORDERING COMMANDS 🍕

menu     - Display the pizza menu
order    - Start a new order (requires customer info)
add      - Add a pizza to current order
summary  - Show current order summary
confirm  - Confirm and place the order
cancel   - Cancel the current order
help     - Show this help message
quit     - Exit the program

EXAMPLES:
> order John Doe, 555-0123, 123 Main St
> add large, thin, pepperoni, mushrooms
> add medium, thick, extra_cheese
"""
        print(help_text)
    
    def show_menu(self):
        """Display the pizza menu."""
        print(self.agent.display_menu())
    
    def start_order(self):
        """Start a new order with customer information."""
        print("Enter customer information:")
        try:
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            address = input("Address: ").strip()
            email = input("Email (optional): ").strip() or None
            
            if not name or not phone or not address:
                print("❌ Name, phone, and address are required.")
                return
            
            result = self.agent.start_order(name, phone, address, email)
            print(f"✅ {result}")
        except KeyboardInterrupt:
            print("\n❌ Order cancelled.")
        except Exception as e:
            print(f"❌ Error starting order: {e}")
    
    def add_pizza(self):
        """Add a pizza to the current order."""
        if not self.agent.current_order:
            print("❌ No active order. Use 'order' command to start an order first.")
            return
        
        print("\nAvailable sizes: small, medium, large, extra_large")
        print("Available crusts: thin, thick, stuffed, gluten_free")
        print("Available toppings: pepperoni, mushrooms, sausage, peppers, onions, olives, extra_cheese, bacon, pineapple, spinach")
        print("\nEnter pizza details:")
        
        try:
            size = input("Size: ").strip().lower().replace(' ', '_')
            crust = input("Crust type: ").strip().lower().replace(' ', '_')
            toppings_input = input("Toppings (comma-separated, or 'none'): ").strip()
            
            if not size or not crust:
                print("❌ Size and crust are required.")
                return
            
            # Parse toppings
            if toppings_input.lower() in ['none', '']:
                toppings = []
            else:
                toppings = [t.strip().lower().replace(' ', '_') for t in toppings_input.split(',')]
            
            result = self.agent.add_pizza_to_order(size, crust, toppings)
            print(f"✅ {result}")
        except KeyboardInterrupt:
            print("\n❌ Pizza addition cancelled.")
        except Exception as e:
            print(f"❌ Error adding pizza: {e}")
    
    def show_summary(self):
        """Show the current order summary."""
        print(self.agent.get_order_summary())
    
    def confirm_order(self):
        """Confirm the current order."""
        if not self.agent.current_order:
            print("❌ No active order to confirm.")
            return
        
        print(self.agent.get_order_summary())
        try:
            confirm = input("\nConfirm this order? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                result = self.agent.confirm_order()
                print(result)
            else:
                print("❌ Order not confirmed.")
        except KeyboardInterrupt:
            print("\n❌ Order confirmation cancelled.")
    
    def cancel_order(self):
        """Cancel the current order."""
        result = self.agent.cancel_order()
        print(result)
    
    def quit_cli(self):
        """Exit the CLI."""
        print("👋 Thank you for using the Pizza Ordering Agent!")
        sys.exit(0)
    
    def parse_command(self, user_input: str) -> tuple:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        return command, args
    
    def run(self):
        """Run the interactive CLI."""
        print("🍕 Welcome to the Interactive Pizza Ordering System! 🍕")
        print("Type 'help' for available commands or 'menu' to see our pizzas.")
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("pizza> ").strip()
                
                if not user_input:
                    continue
                
                command, args = self.parse_command(user_input)
                
                if command in self.commands:
                    self.commands[command]()
                else:
                    print(f"❌ Unknown command: {command}. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main entry point for the CLI."""
    cli = PizzaOrderingCLI()
    cli.run()


if __name__ == "__main__":
    main()