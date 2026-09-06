class Product:
    """Represents a product that is available in the store."""

    def __init__(self, name: str, price: float, quantity: int):
        """Create a product with a name, price, and initial quantity."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError("Price must be a number.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0

    def get_quantity(self) -> int:
        """Return the current product quantity."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Set the product quantity and deactivate it when it reaches zero."""
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be an integer.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active

    def activate(self) -> None:
        """Activate the product."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self.active = False

    def show(self) -> None:
        """Print a human-readable representation of the product."""
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity: int) -> float:
        """Buy a quantity of the product and return the total price."""
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if not self.is_active():
            raise ValueError("Cannot buy an inactive product.")
        if quantity > self.quantity:
            raise ValueError("Not enough product in stock.")

        self.set_quantity(self.quantity - quantity)
        return float(self.price * quantity)


def main() -> None:
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()


if __name__ == "__main__":
    main()
