# -------------------------------------
# shopping_cart.py
# CSU Global - Portfolio Milestone: Online Shopping Cart
# -------------------------------------

# 1. Define ItemToPurchase Class
class ItemToPurchase:
    def __init__(self, name="none", description="none", price=0, quantity=0):
        self.item_name = name
        self.item_description = description
        self.item_price = price
        self.item_quantity = quantity

    def print_item_cost(self):
        total = self.item_price * self.item_quantity
        print(f"{self.item_name} {self.item_quantity} @ ${self.item_price} = ${total}")

    def print_item_description(self):
        print(f"{self.item_name}: {self.item_description}")

# -------------------------------------

# 2. Define ShoppingCart Class
class ShoppingCart:
    def __init__(self, customer_name="none", current_date="January 1, 2020"):
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items = []

    def add_item(self, item):
        self.cart_items.append(item)

    def remove_item(self, item_name):
        found = False
        for i, item in enumerate(self.cart_items):
            if item.item_name == item_name:
                del self.cart_items[i]
                found = True
                break
        if not found:
            print("Item not found in cart. Nothing removed.")

    def modify_item(self, item):
        found = False
        for cart_item in self.cart_items:
            if cart_item.item_name == item.item_name:
                if item.item_description != "none":
                    cart_item.item_description = item.item_description
                if item.item_price != 0:
                    cart_item.item_price = item.item_price
                if item.item_quantity != 0:
                    cart_item.item_quantity = item.item_quantity
                found = True
                break
        if not found:
            print("Item not found in cart. Nothing modified.")

    def get_num_items_in_cart(self):
        return sum(item.item_quantity for item in self.cart_items)

    def get_cost_of_cart(self):
        return sum(item.item_price * item.item_quantity for item in self.cart_items)

    def print_total(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        total_items = self.get_num_items_in_cart()
        print(f"Number of Items: {total_items}")

        if not self.cart_items:
            print("SHOPPING CART IS EMPTY")
        else:
            for item in self.cart_items:
                item.print_item_cost()
            print(f"Total: ${self.get_cost_of_cart()}")

    def print_descriptions(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print("Item Descriptions")
        for item in self.cart_items:
            item.print_item_description()

# -------------------------------------

# 3. Define print_menu Function
def print_menu(cart):
    menu = (
        "\nMENU\n"
        "a - Add item to cart\n"
        "r - Remove item from cart\n"
        "c - Change item quantity\n"
        "i - Output items' descriptions\n"
        "o - Output shopping cart\n"
        "q - Quit"
    )

    option = ""
    while option != "q":
        print(menu)
        option = input("Choose an option:\n").lower()

        if option == 'a':
            name = input("Enter the item name:\n")
            desc = input("Enter the item description:\n")
            price = int(input("Enter the item price:\n"))
            qty = int(input("Enter the item quantity:\n"))
            item = ItemToPurchase(name, desc, price, qty)
            cart.add_item(item)

        elif option == 'r':
            name = input("Enter name of item to remove:\n")
            cart.remove_item(name)

        elif option == 'c':
            name = input("Enter the item name:\n")
            qty = int(input("Enter the new quantity:\n"))
            temp_item = ItemToPurchase(name, quantity=qty)
            cart.modify_item(temp_item)

        elif option == 'i':
            print("\nOUTPUT ITEMS' DESCRIPTIONS")
            cart.print_descriptions()

        elif option == 'o':
            print("\nOUTPUT SHOPPING CART")
            cart.print_total()

        elif option == 'q':
            break

        else:
            print("Invalid option. Please choose a valid menu item.")

# -------------------------------------

# 4. Main Function
def main():
    name = input("Enter customer's name:\n")
    date = input("Enter today's date:\n")
    print(f"\nCustomer name: {name}")
    print(f"Today's date: {date}")

    cart = ShoppingCart(name, date)
    print_menu(cart)

# -------------------------------------

if __name__ == "__main__":
    main()
