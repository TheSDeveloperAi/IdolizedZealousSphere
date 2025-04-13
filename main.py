thefrom datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# ---------------------------
# Global Pricing Information
# ---------------------------
LOCATIONS = ["goiania", "pernambuco", "bahia"]
PRICE_FACTORS = {
    "goiania": 4.0,
    "pernambuco": 4.5,
    "bahia": 5.0
}
BASE_PRICES = {
    500: 1.0,
    1000: 1.5,
    2000: 2.0
}
PRICE_TABLES = {"711": {}, "411": {}}
TAX_RATES = {
    "goiania": 0.10,      # 10% tax
    "pernambuco": 0.15,   # 15% tax
    "bahia": 0.12         # 12% tax
}

# ---------------------------
# Price Table Setup
# ---------------------------
def calculate_price(weight, location, table):
    """Calculate price based on weight, location, and table."""
    base_price = BASE_PRICES[weight] * PRICE_FACTORS[location]
    if table == "711":
        return base_price
    elif table == "411":
        return base_price * 0.9

def populate_price_tables():
    """Populate the price tables with computed prices."""
    for table in PRICE_TABLES:
        for category in ["Acrilico premium"]:
            for finish in ["fosco", "semibrilho"]:
                for color in ["black", "white", "green"]:
                    for weight in BASE_PRICES:
                        for location in LOCATIONS:
                            price = calculate_price(weight, location, table)
                            PRICE_TABLES[table][(category, finish, color, weight, location)] = price

populate_price_tables()

def get_price(table, product, location):
    """Get price for a product based on table, product attributes, and location."""
    product_key = (product.category, product.finish, product.color, product.weight, location)
    table_prices = PRICE_TABLES.get(table, {})
    return table_prices.get(product_key, None)

# ---------------------------
# Domain Classes
# ---------------------------
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

 #   def add_to_order_history(self, order_details: dict) -> None:  #idea to the end of program
      #  """Add an order to customer's history."""
      #  self._order_history.append({
        #    'date': datetime.now(),
         #   **order_details
     #   })

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
        """Calculate commission for a sale."""
        commission = (commission_rate / 100) * total_price
        self._total_commission += commission
        return commission

 #   def record_sale(self, customer_id: int, total_price: float, commission: float) -> None:  #idea to the end of program
     #   """Record a sale in seller's history."""
    #    self._sales_history.append({
      #      'date': datetime.now(),
       #     'customer_id': customer_id,
       #     'total_price': total_price,
       #     'commission': commission
     #   })

    def get_total_commission(self) -> float:
        """Get total commission earned."""
        return self._total_commission

class Transport(Customer):
     def __init__(self, customer_id: int, name: str,  address: str, email: str, phone: str, block:  bool=False, cost: float = 0.0):
         super().__init__(customer_id, name, address, email, phone, None, block)
         self.cost = cost
         self.sender = False

     def calculate_transport_fee(self, total_weight_ml: float) -> float:
         """Calculates the transport fee based on total weight in kg."""
         if self.sender:
             total_weight_kg = total_weight_ml / 1000.0
             return total_weight_kg * self.cost
         else:
             return 0.0

# ---------------------------
# Sample Data and Product Generation
# ---------------------------
customers = [
    Customer(1, "Alice", "goiania", "alice@example.com", "123-456-7890", 4, False),
    Customer(2, "Bob", "pernambuco", "bob@example.com", "234-567-8901", 5, True),  # Blocked customer
    Customer(3, "Carol", "bahia", "carol@example.com", "345-678-9012", 6, False)
]

sellers = [
    Seller(4, "Dave", "goiania", "dave@example.com", "456-789-0123", False),
    Seller(5, "Eve", "pernambuco", "eve@example.com", "567-890-1234", True),  # Blocked seller
    Seller(6, "Frank", "bahia", "frank@example.com", "678-901-2345", False)
]


transportation_list = [
    Transport(7, "Your Truck ldta", "Your Truck", "yourtruck@gmail.com", "667-553-767", False, cost=2.50),
    Transport(8, "Another Courier", "Some Address", "courier@email.com", "111-222-3333", False, cost=3.00),
    # Add more Transport objects with different costs
]

customer_dict = {customer.customer_id: customer for customer in customers}
seller_dict = {seller.customer_id: seller for seller in sellers}
transport_dict = {transport.customer_id: transport for transport in transportation_list}

code_counter = 100
products = {}
for table in PRICE_TABLES.keys():
    for table_key in PRICE_TABLES[table].keys():
        category, finish, color, weight, _ = table_key
        if (category, finish, color, weight) not in [(p.category, p.finish, p.color, p.weight) for p in products.values()]:
            code = f"P{code_counter}"
            flammable = color in ["black", "green"]
            product = Product(category, finish, color, weight, code, flammable)
            products[code_counter] = product
            code_counter += 1

# ---------------------------
# Helper Lookup Functions
# ---------------------------
def get_customer_by_id(customer_id):
    return customer_dict.get(customer_id, None)

def get_seller_by_id(seller_id):
    return seller_dict.get(seller_id, None)

# ---------------------------
# Order Processing Helper Functions
# ---------------------------
def _delete_product(del_code, customer, table, customer_product_list, products, total_price, total_weight, flammable_weight, non_flammable_weight, volumes):
    """Helper function to delete a product from the order."""
    apply_discount = lambda price, discount: price - (price * discount / 100)
    calculate_tax = lambda price, flammable: price * TAX_RATES.get(customer.address, 0) if flammable else 0
    if del_code in customer_product_list:
        quantity, discount = customer_product_list.pop(del_code)
        product = products[del_code]
        base_price = get_price(table, product, customer.address)
        if base_price is not None:
            discounted_price = apply_discount(base_price, discount)
            tax = calculate_tax(discounted_price, product.flammable)
            item_total_price = (discounted_price + tax) * quantity
            total_price -= item_total_price
            total_weight -= product.weight * quantity
            if product.flammable:
                flammable_weight -= product.weight * quantity
            else:
                non_flammable_weight -= product.weight * quantity
            if product.weight == 500:
                volumes[500] -= quantity // 4
            else:
                volumes[product.weight] -= quantity
            print(f"Product {products[del_code]} has been removed successfully!")
            return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, True
        else:
            print("Invalid table number or location.")
            return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False
    else:
        print("Product code not found in the list.")
        return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False

def _change_quantity(qua_code, customer_product_list, products):
    """Helper function to change the quantity of a product in the order."""
    if qua_code in customer_product_list:
        _, discount = customer_product_list[qua_code]
        new_quantity = int(input(f"Enter the new quantity for product {qua_code}: "))
        if new_quantity <= 0:
            print("Quantity must be a positive number. Please try again.")
            return False
        elif products[qua_code].weight == 500 and new_quantity % 4 != 0:
            print("Quantity for 500ml products must be a multiple of 4. Please try again.")
            return False
        else:
            customer_product_list[qua_code] = (new_quantity, discount)
            print(f"Quantity for product {qua_code} has been updated to {new_quantity}.")
            return True
    else:
        print("Product code not found in the list.")
        return False

def _apply_discount_to_product(disc_code, customer_product_list):
    """Helper function to apply a discount to a product in the order."""
    if disc_code in customer_product_list:
        quantity, _ = customer_product_list[disc_code]
        new_discount = float(input(f"Enter the new discount for product {disc_code} (0-100): "))
        if 0 <= new_discount <= 100:
            customer_product_list[disc_code] = (quantity, new_discount)
            print(f"Discount for product {disc_code} has been updated to {new_discount}%.")
            return True
        else:
            print("Discount must be between 0 and 100. Please try again.")
            return False
    else:
        print("Product code not found in the list.")
        return False

def _add_new_product(product_code, customer, table, customer_product_list, products, total_price, total_weight, flammable_weight, non_flammable_weight, volumes):
    """Helper function to add a new product to the order."""
    apply_discount = lambda price, discount: price - (price * discount / 100)
    calculate_tax = lambda price, flammable: price * TAX_RATES.get(customer.address, 0) if flammable else 0
    try:
        product_code_int = int(product_code)
        if product_code_int in products:
            if product_code in customer_product_list:
                print("This product is already in your list.")
                return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False
            else:
                product = products[product_code_int]
                while True:
                    try:
                        quantity = int(input("Enter the quantity for this product: "))
                        if quantity <= 0:
                            print("Quantity must be a positive number. Please try again.")
                        elif product.weight == 500 and quantity % 4 != 0:
                            print("Quantity for 500ml products must be a multiple of 4. Please try again.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid numeric quantity.")
                while True:
                    try:
                        discount = float(input("Enter the discount for this product (0-100): "))
                        if 0 <= discount <= 100:
                            break
                        else:
                            print("Discount must be between 0 and 100. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid numeric discount.")
                customer_product_list[product_code] = (quantity, discount)
                base_price = get_price(table, product, customer.address)
                if base_price is not None:
                    discounted_price = apply_discount(base_price, discount)
                    tax = calculate_tax(discounted_price, product.flammable)
                    item_total_price = (discounted_price + tax) * quantity
                    total_price += item_total_price
                    total_weight += product.weight * quantity
                    if product.flammable:
                        flammable_weight += product.weight * quantity
                    else:
                        non_flammable_weight += product.weight * quantity
                    if product.weight == 500:
                        volumes[500] += quantity // 4
                    else:
                        volumes[product.weight] += quantity
                    print(f"Product {products[product_code_int]} has been added successfully!")
                    print(f"Subtotal price of {quantity} unit(s) of product {product_code} with discount and tax is ${item_total_price:.2f}")
                    return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, True
                else:
                    print("Invalid table number or location.")
                    return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False
        else:
            print("Invalid product code. Please try again.")
            return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False
    except ValueError:
        print("Invalid product code format.") # Added for robustness
        return total_price, total_weight, flammable_weight, non_flammable_weight, volumes, False




# ---------------------------
# Order Processing Functionality (Refactored)
# ---------------------------
def add_products_by_code(customer, seller, commission_rate, table):
    """
    Allow adding, deleting, and modifying products by their code. Calculates totals
    and applies commissions.
    """
    customer_product_list = {}
    total_price = 0
    total_weight = 0
    flammable_weight = 0
    non_flammable_weight = 0
    volumes = {500: 0, 1000: 0, 2000: 0}
    transport_info_entered = False  # Flag to track if transport info is entered

    apply_discount = lambda price, discount: price - (price * discount / 100)
    calculate_tax = lambda price, flammable: price * TAX_RATES.get(customer.address, 0) if flammable else 0

    print("\nOrder Processing:")
    while True:
        print("\nEnter product code to add (or choose an option):")
        print("  2. Delete Product")
        print("  3. Change Quantity")
        print("  4. Change Discount")
        print("  5. Enter Transport Information")
        print("  6. Finish Order")
        user_input = input("Enter code or option number: ").strip()

        if user_input == '2':
            try:
                del_code = input("Enter the product code to delete: ")
                total_price, total_weight, flammable_weight, non_flammable_weight, volumes, _ = _delete_product(
                    del_code, customer, table, customer_product_list, products, total_price, total_weight, flammable_weight, non_flammable_weight, volumes
                )
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '3':
            try:
                qua_code = input("Enter the product code to change quantity for: ")
                _change_quantity(qua_code, customer_product_list, products)
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '4':
            try:
                disc_code = input("Enter the product code to change discount for: ")
                _apply_discount_to_product(disc_code, customer_product_list)
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '5':
            # --- Integration of Transport Cost ---
            transport = None
            while True:
                transport_id_str = input("Enter the Transport ID for this order: ")
                if not transport_id_str:
                    print("Transport ID cannot be empty. Please enter a valid ID.")
                    continue
                try:
                    transport_id = int(transport_id_str)
                    transport = transport_dict.get(transport_id)
                    if transport:
                        transport_info_entered = True  # Set the flag to True
                        break  # Valid ID found
                    else:
                        print("Invalid Transport ID. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid numeric Transport ID.")

            if transport:
                while True:
                    sender_input = input(f"Is '{transport.name}' the sender? (yes/no): ").lower()
                    if sender_input == 'yes':
                        transport.sender = True
                        transport_fee = transport.calculate_transport_fee(total_weight)
                        if transport_fee > 0:
                            total_price += transport_fee
                            print(f"Transport fee (sender '{transport.name}'): ${transport_fee:.2f}")
                        elif transport.sender:
                            print(f"Transport '{transport.name}' is the sender, but the calculated fee is $0.00 (likely due to zero total weight).")
                        break
                    elif sender_input == 'no':
                        transport.sender = False
                        print(f"Transport '{transport.name}' has been recorded for this order. No transport fee applied as it is not the sender.")
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
        elif user_input == '6':
            if not transport_info_entered:
                print("Please enter the transport information (option 5) before finishing the order.")
            else:
                if customer_product_list:
                    print("\n--- Order Summary ---")
                    print(f"{'Product':<30} {'Code':<10} {'Qty':<5} {'Price':<10}")
                    print("-" * 55)
                    for code, (quantity, discount) in customer_product_list.items():
                        product = products[int(code)]
                        base_price = get_price(table, product, customer.address)
                        if base_price is not None:
                            discounted_price = apply_discount(base_price, discount)
                            tax = calculate_tax(discounted_price, product.flammable)
                            unit_price = discounted_price + tax
                            product_name = f"{product.category} ({product.finish}, {product.color}, {product.weight}ml)"
                            print(f"{product_name:<30} {code:<10} {quantity:<5} ${unit_price:<9.2f}")
                    print("-" * 55)
                break # Finish order
        else:
            product_code_str = user_input
            try:
                product_code = int(product_code_str)
                total_price, total_weight, flammable_weight, non_flammable_weight, volumes, _ = _add_new_product(
                    product_code_str, customer, table, customer_product_list, products, total_price, total_weight, flammable_weight, non_flammable_weight, volumes
                )
            except ValueError:
                print("Invalid input. Please enter a valid product code or an option number.")

    print(f"Total price for all added products: ${total_price:.2f}")
    print(f"Total weight for all added products: {total_weight} ml")
    print(f"Total flammable weight: {flammable_weight} ml")
    print(f"Total non-flammable weight: {non_flammable_weight} ml")

    print(f"\nFinal Total Price: ${total_price:.2f}")

    commission = seller.calculate_commission(total_price, commission_rate)
    print(f"Commission for the seller at {commission_rate}% is: ${commission:.2f}")

    print("\nVolume Summary:")
    for weight, volume in volumes.items():
        print(f"{weight} ml: {volume} packages")


# ---------------------------
# Search and Main Program Logic (No changes in this snippet)
# ---------------------------
def search_by_name(name, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if name.lower() in entity.name.lower()]
    return results

def search_by_address(address, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if address.lower() in entity.address.lower()]
    return results


# ... (Rest of your code remains the same until the main_program function) ...

# ---------------------------
# Helper Functions for Main Program
# ---------------------------
def _get_valid_seller():
    """Gets a valid seller ID from the user, with search options."""
    while True:
        user_input = input("Enter the seller ID directly, or type 'name' to search by name, or 'address' to search by address: ").lower()
        if user_input.isnumeric():
            seller_id = int(user_input)
            seller = get_seller_by_id(seller_id)
            if seller:
                if seller.block:
                    print("Seller no longer at the company. Please contact HR for clarification.")
                else:
                    print(f"Seller Details:\nID: {seller.customer_id}\nName: {seller.name}\nAddress: {seller.address}\nEmail: {seller.email}\nPhone: {seller.phone}")
                    return seller
            else:
                print("Invalid seller ID. Please try again.")
        elif user_input == "name":
            search_value = input("Enter the name (or part of the name) of the seller: ").lower()
            results = search_by_name(search_value, entity_type="seller")
            if results:
                print("Found sellers:")
                for s in results:
                    print(f"ID: {s.customer_id}, Name: {s.name}, Address: {s.address}, Email: {s.email}, Phone: {s.phone}")
            else:
                print("No sellers found with the given information.")
        elif user_input == "address":
            search_value = input("Enter the address of the seller: ").lower()
            results = search_by_address(search_value, entity_type="seller")
            if results:
                print("Found sellers:")
                for s in results:
                    print(f"ID: {s.customer_id}, Name: {s.name}, Address: {s.address}, Email: {s.email}, Phone: {s.phone}")
            else:
                print("No sellers found with the given information.")
        else:
            print("Invalid input. Please try again.")

def _get_commission_rate():
    """Gets the commission rate from the user."""
    while True:
        try:
            commission_rate = float(input("Enter the commission rate for the seller (0-100): "))
            if 0 <= commission_rate <= 100:
                return commission_rate
            else:
                print("Commission rate must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric commission rate.")

def _get_valid_customer(seller):
    """Gets a valid customer ID from the user, with search and seller association check."""
    while True:
        user_input = input("Enter the customer ID directly, or type 'name' to search by name, or 'address' to search by address: ").lower()
        if user_input.isnumeric():
            customer_id = int(user_input)
            customer = get_customer_by_id(customer_id)
            if customer:
                if customer.block:
                    print("Customer's blocked due to lack of payment on recent orders. Please contact the financial department.")
                else:
                    if customer.seller_id == seller.customer_id:
                        print(f"Customer Details:\nID: {customer.customer_id}\nName: {customer.name}\nAddress: {customer.address}\nEmail: {customer.email}\nPhone: {customer.phone}")
                        return customer
                    else:
                        print(f"Customer ID {customer_id} is not registered to Seller ID {seller.customer_id}. Please try again.")
            else:
                print("Invalid customer ID. Please try again.")
        elif user_input == "name":
            search_value = input("Enter the name (or part of the name) of the customer: ").lower()
            results = search_by_name(search_value, entity_type="customer")
            if results:
                print("Found customers:")
                for c in results:
                    print(f"ID: {c.customer_id}, Name: {c.name}, Address: {c.address}, Email: {c.email}, Phone: {c.phone}")
            else:
                print("No customers found with the given information.")
        elif user_input == "address":
            search_value = input("Enter the address of the customer: ").lower()
            results = search_by_address(search_value, entity_type="customer")
            if results:
                print("Found customers:")
                for c in results:
                    print(f"ID: {c.customer_id}, Name: {c.name}, Address: {c.address}, Email: {c.email}, Phone: {c.phone}")
                else:
                    print("No customers found with the given information.")
        else:
            print("Invalid input. Please try again.")

def _get_table_number():
    """Gets a valid table number from the user."""
    while True:
        table = input("Enter the table number (711 or 411): ")
        if table in PRICE_TABLES:
            return table
        else:
            print("Invalid table number. Please enter 711 or 411.")

# ---------------------------
# Main Program Logic (Refactored)
# ---------------------------
def main_program():
    global customer_product_list
    customer_product_list = {}
    global table

    current_datetime = datetime.now()
    print(f"Current date and time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    seller = _get_valid_seller()

    if seller:
        commission_rate = _get_commission_rate()
        customer = _get_valid_customer(seller)

        if customer:
            table = _get_table_number()
            add_products_by_code(customer, seller, commission_rate, table)

# ---------------------------
# Entry Point (No changes)
# ---------------------------
if __name__ == "__main__":
    while True:
        print("\nWelcome to the Sales System!")
        choice = input("Enter 'start' to begin a new order or 'exit' to quit: ").lower()
        if choice == 'exit':
            print("Thank you for using the Sales System. Goodbye!")
            break
        elif choice == 'start':
            main_program()
        else:
            print("Invalid choice. Please enter 'start' or 'exit'.")

