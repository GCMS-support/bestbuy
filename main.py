import products
import store


# Set up the initial stock of inventory.
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
]
best_buy = store.Store(product_list)


def display_products(store_obj: store.Store) -> None:
    """Display all active products with their selection numbers."""
    active_products = store_obj.get_all_products()

    if not active_products:
        print("No active products are available.")
        return

    for index, product in enumerate(active_products, start=1):
        print(f"{index}. ", end="")
        product.show()


def make_order(store_obj: store.Store) -> None:
    """Collect an order from the user and submit it to the store."""
    active_products = store_obj.get_all_products()

    if not active_products:
        print("No active products are available.")
        return

    display_products(store_obj)
    shopping_list = []
    print("When you want to finish the order, press Enter.")

    while True:
        product_input = input("Which product number do you want? ").strip()
        if not product_input:
            break

        try:
            product_number = int(product_input)
            if product_number < 1 or product_number > len(active_products):
                raise ValueError

            quantity = int(input("What amount do you want? ").strip())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid product number and a positive amount.")
            continue

        selected_product = active_products[product_number - 1]
        shopping_list.append((selected_product, quantity))
        print("Product added to the order.")

    if not shopping_list:
        print("No products were selected.")
        return

    try:
        total_price = store_obj.order(shopping_list)
    except ValueError as error:
        print(f"The order could not be completed: {error}")
        return

    print(f"Order made! Total payment: ${total_price}")


def start(store_obj: store.Store) -> None:
    """Run the store's command-line user interface."""
    while True:
        print("\nStore Menu")
        print("----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ").strip()

        if choice == "1":
            display_products(store_obj)
        elif choice == "2":
            print(f"Total amount in store: {store_obj.get_total_quantity()}")
        elif choice == "3":
            make_order(store_obj)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose a number between 1 and 4.")


if __name__ == "__main__":
    start(best_buy)
