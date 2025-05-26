from datetime import datetime
from dataclasses import dataclass
import pandas as pd
from typing import Dict, List, Tuple, Optional
# ---------------------------
# Global Pricing Information
# ---------------------------

#new text editor_2


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

BASE_COST_PER_500ML = 2.0

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
@dataclass
class Product:
    category: str
    finish: str
    color: str
    weight: int
    code: str
    flammable: bool = False
    cost: float = 0.0

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
    Customer(2, "Bob", "pernambuco", "bob@example.com", "234-567-8901", 5, True),
    Customer(3, "Carol", "bahia", "carol@example.com", "345-678-9012", 6, False)
]

sellers = [
    Seller(4, "Dave", "goiania", "dave@example.com", "456-789-0123", False),
    Seller(5, "Eve", "pernambuco", "eve@example.com", "567-890-1234", True),
    Seller(6, "Frank", "bahia", "frank@example.com", "678-901-2345", False)
]


transportation_list = [
    Transport(7, "Your Truck ldta", "Your Truck", "yourtruck@gmail.com", "667-553-767", False, cost=2.50),
    Transport(8, "Another Courier", "Some Address", "courier@email.com", "111-222-3333", False, cost=3.00),
]

customer_dict = {customer.customer_id: customer for customer in customers}
seller_dict = {seller.customer_id: seller for seller in sellers}
transport_dict = {transport.customer_id: transport for transport in transportation_list}

code_counter = 100
products = {}

code_counter = 100
products = {}
for table in PRICE_TABLES.keys():
    for table_key in PRICE_TABLES[table].keys():
        category, finish, color, weight, _ = table_key
        product_cost = (weight / 500.0) * BASE_COST_PER_500ML

        if (category, finish, color, weight) not in [(p.category, p.finish, p.color, p.weight) for p in products.values()]:
            code = f"P{code_counter}"
            flammable = color in ["black", "green"]
            product = Product(category, finish, color, weight, code, flammable, cost=product_cost)
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


def _get_payment_conditions():
    """Gets valid payment installment days from the user."""
    while True:
        payment_input = input("Enter payment terms as comma-separated days (e.g., 30, 60, 90): ").strip()
        if not payment_input:
            print("Payment terms cannot be empty. Please enter the terms.")
            continue

        terms_list = [term.strip() for term in payment_input.split(',')]
        valid_terms = []
        is_valid = True

        for term in terms_list:
            if not term.isdigit():
                print(f"Invalid input: '{term}' is not a valid number of days.")
                is_valid = False
                break
            days = int(term)
            if days < 0:
                print("Invalid input: Number of days cannot be negative.")
                is_valid = False
                break
            valid_terms.append(days)

        if is_valid and valid_terms:
            return valid_terms
        elif is_valid and not valid_terms:
             print("Invalid input: No valid payment terms entered.")
        else:
            print("Please try again.")

# ---------------------------
# Order Processing Functionality (Refactored)
# ---------------------------
import pandas as pd # Make sure this is at the top of your script

def add_products_by_code(customer, seller, commission_rate, table, payment_conditions):
    """
    Allow adding, deleting, and modifying products by their code. Calculates totals
    and applies commissions.
    """
    customer_product_list = {}
    total_price = 0 # This will accumulate the Line Total (incl Tax) for all products + transport fee
    total_weight = 0
    flammable_weight = 0
    non_flammable_weight = 0
    volumes = {500: 0, 1000: 0, 2000: 0}
    transport_info_entered = False
    transport = None # Initialize transport to None outside the loop
    final_transport_fee = 0 # Initialize final_transport_fee outside the loop

    apply_discount = lambda price, discount: price - (price * discount / 100)
    calculate_tax_rate_amount = lambda price, flammable, tax_rate: price * tax_rate if flammable else 0

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
                # Recalculation logic in option 6 will handle overall totals correctly
                _delete_product(del_code, customer, table, customer_product_list, products, total_price, total_weight, flammable_weight, non_flammable_weight, volumes)
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '3':
            try:
                qua_code = input("Enter the product code to change quantity for: ")
                _change_quantity(qua_code, customer_product_list, products)
                 # Recalculation logic in option 6 will handle overall totals correctly
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '4':
            try:
                disc_code = input("Enter the product code to change discount for: ")
                _apply_discount_to_product(disc_code, customer_product_list)
                 # Recalculation logic in option 6 will handle overall totals correctly
            except ValueError:
                print("Invalid product code. Please enter a valid code.")
        elif user_input == '5':
             # --- Integration of Transport Cost ---
             # transport is already initialized outside the loop
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

            # Note: Transport fee calculation impacting total_price happens when finishing order (option 6)
            if transport: # Check if transport object was successfully retrieved
                while True:
                    sender_input = input(f"Is '{transport.name}' the sender? (yes/no): ").lower()
                    if sender_input == 'yes':
                        transport.sender = True
                        # Fee is calculated and added to total_price in option 6 after final weight is known
                        print(f"Transport '{transport.name}' set as sender. Fee will be calculated based on final weight.")
                        break
                    elif sender_input == 'no':
                        transport.sender = False
                        print(f"Transport '{transport.name}' has been recorded for this order. Not the sender.")
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

        elif user_input == '6':
            if not transport_info_entered:
                print("Please enter the transport information (option 5) before finishing the order.")
            else:
                order_data = []
                # Recalculate totals/weights/volumes/cost here based on customer_product_list
                total_price = 0 # Reset and recalculate final total price (product totals only initially)
                total_weight = 0
                flammable_weight = 0
                non_flammable_weight = 0
                volumes = {500: 0, 1000: 0, 2000: 0}
                total_cost = 0.0 # Initialize total_cost for recalculation (product cost only initially)

                if customer_product_list:
                    for code, (quantity, discount) in customer_product_list.items():
                        product = products[int(code)]
                        base_price = get_price(table, product, customer.address)
                        if base_price is not None:
                            discounted_price = apply_discount(base_price, discount)
                            tax_rate = TAX_RATES.get(customer.address, 0)
                            tax_amount_per_item = calculate_tax_rate_amount(discounted_price, product.flammable, tax_rate)

                            unit_price_before_tax = discounted_price
                            unit_price_incl_tax = discounted_price + tax_amount_per_item

                            item_total_before_tax = discounted_price * quantity
                            line_tax_amount = tax_amount_per_item * quantity
                            line_total_with_tax = item_total_before_tax + line_tax_amount

                            total_price += line_total_with_tax # Add product line total to running total price

                            # Calculate and add to total_cost (product cost)
                            line_cost = product.cost * quantity
                            total_cost += line_cost


                            # Recalculate weights and volumes
                            total_weight += product.weight * quantity
                            if product.flammable:
                                flammable_weight += product.weight * quantity
                            else:
                                non_flammable_weight += product.weight * quantity
                            if product.weight == 500:
                                volumes[500] += quantity // 4
                            else:
                                volumes[product.weight] += quantity


                            product_name = f"{product.category} ({product.finish}, {product.color}, {product.weight}ml)"
                            order_data.append({
                                'Code': code,
                                'Product name': product_name,
                                'Unit Price (before Tax)': f"{unit_price_before_tax:.2f}",
                                'Total (before Tax)': f"{item_total_before_tax:.2f}",
                                'Tax Amount': f"{line_tax_amount:.2f}",
                                'Line Total (incl Tax)': f"{line_total_with_tax:.2f}"
                            })

                    # Calculate and add transport fee to final total if transport is sender
                    final_transport_fee = 0 # Re-initialize for calculation
                    if transport and transport.sender:
                         final_transport_fee = transport.calculate_transport_fee(total_weight)
                         total_price += final_transport_fee # total_price now includes product totals + transport fee


                    if order_data:
                        df = pd.DataFrame(order_data)
                        print("\n--- Order Summary ---")
                        print(df.to_string(index=False, col_space={'Code': 6, 'Product name': 30, 'Unit Price (before Tax)': 18, 'Total (before Tax)': 15, 'Tax Amount': 10, 'Line Total (incl Tax)': 18}))
                        print("--- End of Order Summary ---")

                        # Calculate and print total items
                        total_items = len(customer_product_list)
                        print(f"\nTotal products: {total_items} items")

                break # Finish order
        else:
            product_code_str = user_input
            try:
                product_code_int = int(product_code_str) # Ensure code is integer for products dict lookup
                if product_code_int in products:
                    # Check if product code (as string) is already in the list
                    if product_code_str in customer_product_list:
                        print("This product is already in your list.")
                        continue # Go back to the menu
                    else:
                         # Get quantity and discount for the new product
                        product = products[product_code_int] # Get product object
                        while True:
                            try:
                                quantity = int(input("Enter the quantity for this product: "))
                                if quantity <= 0:
                                    print("Quantity must be a positive number. Please try again.")
                                elif product.weight == 500 and quantity % 4 != 0:
                                    print("Quantity for 500ml products must be a multiple of 4. Please try again.")
                                else:
                                    break # Valid quantity entered
                            except ValueError:
                                print("Invalid input. Please enter a valid numeric quantity.")

                        while True:
                            try:
                                discount = float(input("Enter the discount for this product (0-100): "))
                                if 0 <= discount <= 100:
                                    break # Valid discount entered
                                else:
                                    print("Discount must be between 0 and 100. Please try again.")
                            except ValueError:
                                print("Invalid input. Please enter a valid numeric discount.")

                        # Add product and its quantity/discount to customer_product_list
                        customer_product_list[product_code_str] = (quantity, discount)
                        print(f"Product {product.code} ({product.category}, {product.weight}ml) added successfully!")
                        # No need to calculate/update totals here if recalculating in option 6

                else:
                    print(f"Invalid product code: {product_code_str}. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid product code or an option number.")

    # --- Final Summary Section ---

    # ... (Existing DataFrame summary for participants) ...

    detail_types = ['ID', 'Name', 'Address', 'Email', 'Phone', 'Seller ID', 'Blocked', 'Total Commission', 'Transport Cost', 'Sender']

    seller_details = [
        seller.customer_id,
        seller.name,
        seller.address,
        seller.email,
        seller.phone,
        'N/A',
        seller.block,
        f"${seller._total_commission:.2f}",
        'N/A',
        'N/A'
    ]

    customer_details = [
        customer.customer_id,
        customer.name,
        customer.address,
        customer.email,
        customer.phone,
        customer.seller_id,
        customer.block,
        'N/A',
        'N/A',
        'N/A'
    ]

    transport_details = []
    # Check if transport exists before accessing its attributes
    if transport_info_entered and transport:
        transport_details = [
            transport.customer_id,
            transport.name,
            transport.address,
            transport.email,
            transport.phone,
            'N/A',
            transport.block,
            'N/A', # Total Commission not applicable
            f"${transport.cost:.2f}" if hasattr(transport, 'cost') else 'N/A',
            transport.sender if hasattr(transport, 'sender') else 'N/A'
        ]
    else:
        transport_details = ['N/A'] * len(detail_types)

    participants_data = {
        'Detail Type': detail_types,
        'Seller': seller_details,
        'Customer': customer_details,
        'Transport': transport_details
    }

    df_participants = pd.DataFrame(participants_data)

    print("\n--- Order Participants Summary ---")
    print(df_participants.to_string(index=False, col_space={'Detail Type': 15, 'Seller': 25, 'Customer': 25, 'Transport': 25}))
    print("--- End of Order Participants Summary ---")


    # ... (Existing print statements for totals, weights, volumes) ...
    # These totals are based on the recalculation done before the order summary print

    # --- Print Total Cost of all products (including commission) ---
    # total_cost already includes product cost
    # commission is calculated below
    # We will print the updated total_cost after calculating commission

    print(f"\nTotal price for all added products (before Transport Fee): ${total_price - final_transport_fee:.2f}")
    print(f"Total weight for all added products: {total_weight} ml")
    print(f"Total flammable weight: {flammable_weight} ml")
    print(f"Total non-flammable weight: {non_flammable_weight} ml")

    print(f"\nFinal Total Order Price (including Transport Fee): ${total_price:.2f}")

    # Commission calculation uses total price BEFORE transport fee
    commission_base_price = total_price - final_transport_fee
    commission = seller.calculate_commission(commission_base_price, commission_rate)
    print(f"Commission for the seller at {commission_rate}% is: ${commission:.2f}")

    # --- Add commission to total_cost and print ---
    total_cost += commission # Add commission to product cost
    print(f"\nTotal order cost (products + commission): ${total_cost:.2f}") # Updated print statement


    print("\nVolume Summary:")
    for weight, volume in volumes.items():
        print(f"{weight} ml: {volume} packages")

    # Calculate and print installment details
    if payment_conditions:
        num_installments = len(payment_conditions)
        if num_installments > 0:
            price_per_installment = total_price / num_installments # Divide the FINAL total price
            print("\n--- Payment Schedule ---")
            print(f"Total installments: {num_installments}")
            for i, days in enumerate(payment_conditions):
                 print(f"  Installment {i + 1}: ${price_per_installment:.2f} (due in {days} days)")
            print("--- End of Payment Schedule ---")
        else:
            print("\nPayment: Full amount due immediately.")


    return customer_product_list, total_price, total_weight, flammable_weight, volumes


# ---------------------------
# Search and Main Program Logic
# ---------------------------
def search_by_name(name, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if name.lower() in entity.name.lower()]
    return results

def search_by_address(address, entity_type="customer"):
    entity_dict = customer_dict if entity_type == "customer" else seller_dict
    results = [entity for entity in entity_dict.values() if address.lower() in entity.address.lower()]
    return results

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
# Main Program Logic
# ---------------------------

def main_program():
    global customer_product_list
    customer_product_list = {}
    global table

    current_datetime = datetime.now()
    print(f"Current date and time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\nWelcome to the Sales System!")
    print("1. Start a New Order")
    print("2. Exit")

    while True:
        choice = input("Enter your choice: ")
        if choice == '1':
            seller = _get_valid_seller()
            if seller:
                commission_rate = _get_commission_rate()
                customer = _get_valid_customer(seller)
                if customer:
                    table = _get_table_number()
                    payment_conditions = _get_payment_conditions()
                    add_products_by_code(customer, seller, commission_rate, table, payment_conditions)
            break
        elif choice == '2':
            print("Thank you for using the Sales System. Goodbye!")
            return False
        else:
            print("Invalid choice. Please enter 1 or 2.")
    return True

# ---------------------------
# Entry Point
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

