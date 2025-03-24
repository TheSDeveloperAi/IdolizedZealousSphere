
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

# Dictionary of state tax rates
tax_rates = {
    "sao paulo": 0.18,  # 18% tax
    "rio de janeiro": 0.20,  # 20% tax
    "minas gerais": 0.18,  # 18% tax
    "goiania": 0.17,    # 17% tax
    "pernambuco": 0.18, # 18% tax
    "bahia": 0.12     # 12% tax
}

class Customer:
    def __init__(self, customer_id: int, name: str, address: str, email: str, phone: str, seller_id: int, block: bool = False):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.seller_id = seller_id
        self.block = block
        self._order_history = []

    def __str__(self) -> str:
        return f"Customer(customer_id='{self.customer_id}', name='{self.name}', address='{self.address}', email='{self.email}', phone='{self.phone}', seller_id='{self.seller_id}', block={self.block})"

    def is_blocked(self) -> bool:
        """Check if customer is blocked."""
        return self.block

    def get_location(self) -> str:
        """Get customer's location for pricing."""
        return self.address

    def add_to_order_history(self, order_details: dict) -> None:
        """Add an order to customer's history."""
        self._order_history.append({
            'date': datetime.now(),
            **order_details
        })

@dataclass
class Product:
    category: str
    finish: str
    code: str
    flammable: bool = False

class Seller(Customer):
    def __init__(self, customer_id: int, name: str, address: str, email: str, phone: str, block: bool = False):
        super().__init__(customer_id, name, address, email, phone, None, block)
        self._total_commission = 0.0
        self._sales_history = []

    def calculate_commission(self, total_price: float, commission_rate: float) -> float:
        """Calculate commission for a sale."""
        commission = (commission_rate / 100) * total_price
        self._total_commission += commission
        return commission

    def record_sale(self, customer_id: int, total_price: float, commission: float) -> None:
        """Record a sale in seller's history."""
        self._sales_history.append({
            'date': datetime.now(),
            'customer_id': customer_id,
            'total_price': total_price,
            'commission': commission
        })

    def get_total_commission(self) -> float:
        """Get total commission earned."""
        return self._total_commission

# Factory function to create a Customer object
def create_customer(customer_id, name, address, email, phone, seller_id, block=False):
    return Customer(customer_id, name, address, email, phone, seller_id, block)

# Factory function to create a Seller object
def create_seller(customer_id, name, address, email, phone, block=False):
    return Seller(customer_id, name, address, email, phone, block)

# List of customers using the factory function
customers = [
    create_customer(1, "Alice", "sao paulo", "alice@example.com", "123-456-7890", 4),
    create_customer(2, "Bob", "rio de janeiro", "bob@example.com", "234-567-8901", 5),
    create_customer(3, "Charlie", "minas gerais", "charlie@example.com", "345-678-9012", 6, True)  # Blocked customer
]

# List of sellers
sellers = [
    Seller(4, "Dave", "goiania", "dave@example.com", "456-789-0123"),
    Seller(5, "Eve", "pernambuco", "eve@example.com", "567-890-1234", True),  # Blocked seller
    Seller(6, "Frank", "bahia", "frank@example.com", "678-901-2345")
]

# Creating dictionaries for faster lookups
customer_dict = {customer.customer_id: customer for customer in customers}
seller_dict = {seller.customer_id: seller for seller in sellers}

def get_price(base_price: float, customer_location: str, product_category: str) -> float:
    """Calculate final price based on location tax and product category"""
    # Get tax rate for the location (default to highest rate if location not found)
    tax_rate = tax_rates.get(customer_location.lower(), max(tax_rates.values()))
    
    # Apply category-specific markup
    category_markup = {
        'electronics': 1.15,  # 15% markup
        'clothing': 1.10,    # 10% markup
        'furniture': 1.20    # 20% markup
    }
    markup = category_markup.get(product_category.lower(), 1.0)
    
    # Calculate final price
    final_price = base_price * (1 + tax_rate) * markup
    return round(final_price, 2)

def process_order(customer_id: int, seller_id: int, items: List[Dict], commission_rate: float = 5.0) -> Optional[float]:
    """Process an order and return the total price if successful"""
    
    # Verify customer and seller exist and aren't blocked
    customer = customer_dict.get(customer_id)
    seller = seller_dict.get(seller_id)
    
    if not customer or not seller:
        print("Error: Customer or seller not found")
        return None
    
    if customer.block or seller.block:
        print("Error: Customer or seller is blocked")
        return None
    
    # Calculate total price for all items
    total_price = 0
    for item in items:
        base_price = item.get('base_price', 0)
        category = item.get('category', '')
        final_price = get_price(base_price, customer.address, category)
        total_price += final_price
    
    # Calculate commission
    commission = seller.calculate_commission(total_price, commission_rate)
    
    # Record the sale
    seller.record_sale(customer_id, total_price, commission)
    
    return total_price

# Example usage
if __name__ == "__main__":
    # Example order
    order_items = [
        {"base_price": 100, "category": "electronics"},
        {"base_price": 50, "category": "clothing"}
    ]
    
    # Process an order
    total = process_order(1, 4, order_items)
    if total:
        print(f"Order processed successfully. Total price: ${total:.2f}")
