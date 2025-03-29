from datetime import datetime
from dataclasses import dataclass

# Locations and their respective price factors
locations = ["goiania", "pernambuco", "bahia"]
price_factors = {
    "goiania": 4.0,
    "pernambuco": 4.5,
    "bahia": 5.0
}

# Base prices
base_prices = {
    500: 1.0,
    1000: 1.5,
    2000: 2.0
}

# Price tables
price_tables = {"711": {}, "411": {}}

def calculate_price(weight, location, table):
    """Calculate price based on weight, location, and table."""
    base_price = base_prices[weight] * price_factors[location]
    # Adjust prices based on the table
    if table == "711":
        return base_price  # Standard pricing
    elif table == "411":
        return base_price * 0.9  # For example, 10% discount
                
def populate_price_tables():
    """Populate the price tables with computed prices."""
    for table in price_tables:
        for category in ["Acrilico premium"]:
            for finish in ["fosco", "semibrilho"]:
                for color in ["black", "white", "green"]:
                    for weight in base_prices:
                        for location in locations:
                            price = calculate_price(weight, location, table)
                            price_tables[table][(category, finish, color, weight, location)] = price
                        

# Initialize price tables
populate_price_tables()

# Function to get the price based on the table, product attributes, and location
def get_price(table, product, location):
    """Get price for a product based on table, product attributes, and location.
    
    Args:
        table (str): Price table identifier ('711' or '411')
        product (Product): Product object containing category, finish, color, and weight
        location (str): Location identifier
        
    Returns:
        float or None: Price if found, None if not found
    """
    product_key = (product.category, product.finish, product.color, product.weight, location)
    table_prices = price_tables.get(table, {})
    return table_prices.get(product_key, None)

# Tax rates based on location
tax_rates = {
    "goiania": 0.10,   # 10% tax
    "pernambuco": 0.15,  # 15% tax
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

# List of customers
customers = [
    Customer(1, "Alice", "goiania", "alice@example.com", "123-456-7890", 4, False),
    Customer(2, "Bob", "pernambuco", "bob@example.com", "234-567-8901", 5, True),  # Blocked customer
    Customer(3, "Carol", "bahia", "carol@example.com", "345-678-9012", 6, False)
]

# List of sellers
sellers = [
    Seller(4, "Dave", "goiania", "dave@example.com", "456-789-0123", False),
    Seller(5, "Eve", "pernambuco", "eve@example.com", "567-890-1234", True),  # Blocked seller
    Seller(6, "Frank", "bahia", "frank@example.com", "678-901-2345", False)
]

# Creating dictionaries for faster lookups
customer_dict = {customer.customer_id: customer for customer in customers}
seller_dict = {seller.customer_id: seller for seller in sellers}

# Generate products from price table data
code_counter = 100
products = {}
for table_key in price_tables['711'].keys():
    category, finish, color, weight, _ = table_key
    code = f"P{code_counter}"
    flammable = color in ["black", "green"]  # Example flammability rule
    product = Product(category, finish, color, weight, code, flammable)
    products[code_counter] = product
    code_counter += 1

def get_customer_by_id(customer_id):
    return customer_dict.get(customer_id, None)

def get_seller_by_id(seller_id):
    return seller_dict.get(seller_id, None)

def get_product_by_id(product_id):
    return products.get(product_id, None)

# Function to add new products by code until the user finishes
def add_products_by_code(customer, seller, commission_rate):
    apply_discount = lambda price, discount: price - (price * discount / 100)
    calculate_tax = lambda price, flammable: price * tax_rates.get(customer.address, 0) if flammable else 0

    total_price = 0
    total_weight = 0
    flammable_weight = 0
    non_flammable_weight = 0
    volumes = {500: 0, 1000: 0, 2000: 0}

    print("Enter product codes to add products. Type 'finish' to end, 'del' to delete a product, 'qua' to change quantity, or 'disc' to change discount.")
    while True:
        user_input = input("Enter the product code, 'del' to delete, 'qua' to change quantity, 'disc' to change discount, or 'finish' to end: ").lower()
        if user_input == "finish":
            break
        elif user_input.startswith("del"):
            try:
                del_code = int(user_input.split()[1])
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
                        # Update volume summary
                        if product.weight == 500:
                            volumes[500] -= quantity // 4
                        else:
                            volumes[product.weight] -= quantity
                        print(f"Product {products[del_code]} has been removed successfully!")
                    else:
                        print("Invalid table number or location.")
                else:
                    print("Product code not found in the list.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter 'del' followed by a valid product code to delete.")
        elif user_input.startswith("qua"):
            try:
                qua_code = int(user_input.split()[1])
                if qua_code in customer_product_list:
                    _, discount = customer_product_list[qua_code]
                    new_quantity = int(input(f"Enter the new quantity for product {qua_code}: "))
                    if new_quantity <= 0:
                        print("Quantity must be a positive number. Please try again.")
                    elif products[qua_code].weight == 500 and new_quantity % 4 != 0:
                        print("Quantity for 500ml products must be a multiple of 4. Please try again.")
                    else:
                        customer_product_list[qua_code] = (new_quantity, discount)
                        print(f"Quantity for product {qua_code} has been updated to {new_quantity}.")
                else:
                    print("Product code not found in the list.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter 'qua' followed by a valid product code.")
        elif user_input.startswith("disc"):
            try:
                disc_code = int(user_input.split()[1])
                if disc_code in customer_product_list:
                    quantity, _ = customer_product_list[disc_code]
                    new_discount = float(input(f"Enter the new discount for product {disc_code} (0-100): "))
                    if 0 <= new_discount <= 100:
                        customer_product_list[disc_code] = (quantity, new_discount)
                        print(f"Discount for product {disc_code} has been updated to {new_discount}%.")
                    else:
                        print("Discount must be between 0 and 100. Please try again.")
                else:
                    print("Product code not found in the list.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter 'disc' followed by a valid product code.")
        else:
            try:
                product_code = int(user_input)
                if product_code in products:
                    if product_code in customer_product_list:
                        print("This product is already in your list.")
                    else:
                        product = products[product_code]
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
                            # Update volume summary
                            if product.weight == 500:
                                volumes[500] += quantity // 4
                            else:
                                volumes[product.weight] += quantity
                            print(f"Product {products[product_code]} has been added successfully!")
                            print(f"Subtotal price of {quantity} unit(s) of product {product_code} with discount and tax is ${item_total_price:.2f}")
                        else:
                            print("Invalid table number or location.")
                else:
                    print("Invalid product code. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid numeric product code, or type 'finish' to end.")

    print(f"Total price for all added products: ${total_price:.2f}")
    print(f"Total weight for all added products: {total_weight} ml")
    print(f"Total flammable weight: {flammable_weight} ml")
    print(f"Total non-flammable weight: {non_flammable_weight} ml")

    # Calculate the commission for the seller
    commission = seller.calculate_commission(total_price, commission_rate)
    print(f"Commission for the seller at {commission_rate}% is: ${commission:.2f}")

    # Display the volume summary
    print("\nVolume Summary:")
    for weight, volume in volumes.items():
        print(f"{weight} ml: {volume} packages")

# Function to search for sellers or customers by name
def search_by_name(name, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if name.lower() in entity.name.lower()]
    return results

# Function to search for sellers or customers by address
def search_by_address(address, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if address.lower() in entity.address.lower()]
    return results

# Main program logic
def main_program():
    # Track products in the customer's list
    global customer_product_list
    customer_product_list = {}
    global table # Declare table as global

    # Get current date and time
    current_datetime = datetime.now()
    print(f"Current date and time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    # Get a valid seller ID
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
                    break
            else:
                print("Invalid seller ID. Please try again.")
        elif user_input == "name":
            search_value = input("Enter the name (or part of the name) of the seller: ").lower()
            results = search_by_name(search_value, entity_type="seller")
            if results:
                print("Found sellers:")
                for seller in results:
                    print(f"ID: {seller.customer_id}, Name: {seller.name}, Address: {seller.address}, Email: {seller.email}, Phone: {seller.phone}")
            else:
                print("No sellers found with the given information.")
        elif user_input == "address":
            search_value = input("Enter the address of the seller: ").lower()
            results = search_by_address(search_value, entity_type="seller")
            if results:
                print("Found sellers:")
                for seller in results:
                    print(f"ID: {seller.customer_id}, Name: {seller.name}, Address: {seller.address}, Email: {seller.email}, Phone: {seller.phone}")
            else:
                print("No sellers found with the given information.")
        else:
            print("Invalid input. Please try again.")

    # Get the commission percentage
    while True:
        try:
            commission_rate = float(input("Enter the commission rate for the seller (0-100): "))
            if 0 <= commission_rate <= 100:
                break
            else:
                print("Commission rate must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric commission rate.")

    # Get a valid customer ID
    while True:
        user_input = input("Enter the customer ID directly, or type 'name' to search by name, or 'address' to search by address: ").lower()
        if user_input.isnumeric():
            customer_id = int(user_input)
            customer = get_customer_by_id(customer_id)
            if customer:
                if customer.block:
                    print("Customer's blocked due to lack of payment on recent orders. Please contact the financial department.")
                else:
                    # Verify if the customer is registered to the seller
                    if customer.seller_id == seller_id:
                        print(f"Customer Details:\nID: {customer.customer_id}\nName: {customer.name}\nAddress: {customer.address}\nEmail: {customer.email}\nPhone: {customer.phone}")
                        break
                    else:
                        print(f"Customer ID {customer_id} is not registered to Seller ID {seller_id}. Please try again.")
            else:
                print("Invalid customer ID. Please try again.")
        elif user_input == "name":
            search_value = input("Enter the name (or part of the name) of the customer: ").lower()
            results = search_by_name(search_value, entity_type="customer")
            if results:
                print("Found customers:")
                for customer in results:
                    print(f"ID: {customer.customer_id}, Name: {customer.name}, Address: {customer.address}, Email: {customer.email}, Phone: {customer.phone}")
            else:
                print("No customers found with the given information.")
        elif user_input == "address":
            search_value = input("Enter the address of the customer: ").lower()
            results = search_by_address(search_value, entity_type="customer")
            if results:
                print("Found customers:")
                for customer in results:
                    print(f"ID: {customer.customer_id}, Name: {customer.name}, Address: {customer.address}, Email: {customer.email}, Phone: {customer.phone}")
            else:
                print("No customers found with the given information.")
        else:
            print("Invalid input. Please try again.")

    # Get a valid table number
    while True:
        table = input("Enter the table number (711 or 411): ")
        if table in price_tables:
            break
        else:
            print("Invalid table number. Please enter 711 or 411.")

    # Prompt to add multiple products by code
    add_products_by_code(customer, seller, commission_rate)

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