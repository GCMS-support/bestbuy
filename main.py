"""Einstiegspunkt: Benutzermenue fuer den Best-Buy-Store."""

import products
import promotions
import store


def list_products(best_buy):
    """Zeigt alle aktiven Produkte im Store an."""
    print("------")
    for number, product in enumerate(best_buy.get_all_products(), start=1):
        print(f"{number}. {product}")
    print("------")


def show_total_amount(best_buy):
    """Zeigt die Gesamtmenge aller Artikel im Store an."""
    print(f"Total of {best_buy.get_total_quantity()} items in store")


def make_order(best_buy):
    """Nimmt eine Bestellung entgegen und gibt den Gesamtpreis aus."""
    available = best_buy.get_all_products()
    list_products(best_buy)
    print("When you want to finish order, enter empty text.")

    shopping_list = []
    while True:
        choice = input("Which product # do you want? ").strip()
        amount = input("What amount do you want? ").strip()
        if not choice or not amount:
            break
        if not choice.isdigit() or not amount.isdigit():
            print("Error adding product!")
            continue
        index = int(choice) - 1
        if not 0 <= index < len(available):
            print("Error adding product!")
            continue
        shopping_list.append((available[index], int(amount)))
        print("Product added to list!")

    if not shopping_list:
        return
    try:
        total = best_buy.order(shopping_list)
        print("********")
        print(f"Order made! Total payment: ${total}")
    except ValueError as error:
        print(f"Error while making order! {error}")


def start(best_buy):
    """Zeigt das Menue an und verarbeitet die Benutzereingaben."""
    menu = ("\n   Store Menu\n"
            "   ----------\n"
            "1. List all products in store\n"
            "2. Show total amount in store\n"
            "3. Make an order\n"
            "4. Quit")
    actions = {
        "1": list_products,
        "2": show_total_amount,
        "3": make_order,
    }
    while True:
        print(menu)
        choice = input("Please choose a number: ").strip()
        if choice == "4":
            print("Bye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Error with your choice! Please try again!")
            continue
        action(best_buy)


def main():
    """Baut den Anfangsbestand auf und startet das Menue."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Aktionen anlegen
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Aktionen den Produkten zuweisen
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
