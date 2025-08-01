# Online Shopping Cart Portfolio Project

# ItemToPurchase class
default_item_name = "none"
default_item_price = 0.0
default_item_quantity = 0

class ItemToPurchase:
    def __init__(self, item_name=default_item_name, item_price=default_item_price, item_quantity=default_item_quantity, item_description="none"):
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity
        self.item_description = item_description

    def print_item_cost(self):
        cost = self.item_price * self.item_quantity
        print(f"{self.item_name} {self.item_quantity} @ ${int(self.item_price)} = ${int(cost)}")

    def print_item_description(self):
        print(f"{self.item_name}: {self.item_description}")

# ShoppingCart class
class ShoppingCart:
    def __init__(self, customer_name="none", current_date="January 1, 2020"):
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items = []

    def add_item(self, item):
        self.cart_items.append(item)

    def remove_item(self, item_name):
        found = False
        for item in self.cart_items:
            if item.item_name == item_name:
                self.cart_items.remove(item)
                found = True
                break
        if not found:
            print("Item not found in cart. Nothing removed.")

    def modify_item(self, item_to_modify):
        found = False
        for item in self.cart_items:
            if item.item_name == item_to_modify.item_name:
                found = True
                if item_to_modify.item_price != 0:
                    item.item_price = item_to_modify.item_price
                if item_to_modify.item_quantity != 0:
                    item.item_quantity = item_to_modify.item_quantity
                if item_to_modify.item_description != "none":
                    item.item_description = item_to_modify.item_description
                break
        if not found:
            print("Item not found in cart. Nothing modified.")

    def get_num_items_in_cart(self):
        return sum(item.item_quantity for item in self.cart_items)

    def get_cost_of_cart(self):
        return sum(item.item_price * item.item_quantity for item in self.cart_items)

    def print_total(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print(f"Number of Items: {self.get_num_items_in_cart()}")
        if not self.cart_items:
            print("SHOPPING CART IS EMPTY")
        else:
            for item in self.cart_items:
                item.print_item_cost()
            print(f"Total: ${int(self.get_cost_of_cart())}")

    def print_descriptions(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print("Item Descriptions")
        for item in self.cart_items:
            item.print_item_description()

# print_menu function
def print_menu(cart):
    menu = (
        "\nMENU\n"
        "a - Add item to cart\n"
        "r - Remove item from cart\n"
        "c - Change item quantity\n"
        "i - Output items' descriptions\n"
        "o - Output shopping cart\n"
        "q - Quit\n"
    )
    choice = ""
    while choice != "q":
        print(menu)
        choice = input("Choose an option:\n").lower()

        if choice == "a":
            print("ADD ITEM TO CART")
            name = input("Enter the item name:\n")
            description = input("Enter the item description:\n")
            try:
                price = float(input("Enter the item price:\n"))
                quantity = int(input("Enter the item quantity:\n"))
                if price < 0 or quantity < 0:
                    raise ValueError
                item = ItemToPurchase(name, price, quantity, description)
                cart.add_item(item)
            except ValueError:
                print("Invalid input. Price and quantity must be non-negative numbers.")

        elif choice == "r":
            print("REMOVE ITEM FROM CART")
            name = input("Enter name of item to remove:\n")
            cart.remove_item(name)

        elif choice == "c":
            print("CHANGE ITEM QUANTITY")
            name = input("Enter the item name:\n")
            try:
                quantity = int(input("Enter the new quantity:\n"))
                if quantity < 0:
                    raise ValueError
                item = ItemToPurchase(name, item_quantity=quantity)
                cart.modify_item(item)
            except ValueError:
                print("Invalid input. Quantity must be a non-negative number.")

        elif choice == "i":
            print("OUTPUT ITEMS' DESCRIPTIONS")
            cart.print_descriptions()

        elif choice == "o":
            print("OUTPUT SHOPPING CART")
            cart.print_total()

        elif choice != "q":
            print("Invalid option. Please choose a valid menu option.")

# Main function
if __name__ == "__main__":
    customer_name = input("Enter customer's name:\n") or "John Doe"
    current_date = input("Enter today's date:\n") or "February 1, 2020"
    print(f"Customer name: {customer_name}")
    print(f"Today's date: {current_date}\n")
    shopping_cart = ShoppingCart(customer_name, current_date)
    print_menu(shopping_cart)