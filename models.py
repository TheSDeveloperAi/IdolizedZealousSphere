
from dataclasses import dataclass
from datetime import datetime

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

    def get_location(self) -> str:
        return self.address

    def add_to_order_history(self, order_details: dict) -> None:
        self._order_history.append({
            'date': datetime.now(),
            **order_details
        })

@dataclass
class Product:
    category: str
    finish: str
    color: str
    weight: int
    code: str
    flammable: bool = False

class Seller(Customer):
    def __init__(self, customer_id: int, name: str, address: str, email: str, phone: str, block: bool = False):
        super().__init__(customer_id, name, address, email, phone, None, block)
        self._total_commission = 0.0
        self._sales_history = []

    def calculate_commission(self, total_price: float, commission_rate: float) -> float:
        commission = (commission_rate / 100) * total_price
        self._total_commission += commission
        return commission

    def record_sale(self, customer_id: int, total_price: float, commission: float) -> None:
        self._sales_history.append({
            'date': datetime.now(),
            'customer_id': customer_id,
            'total_price': total_price,
            'commission': commission
        })

    def get_total_commission(self) -> float:
        return self._total_commission
