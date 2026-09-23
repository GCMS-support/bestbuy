"""Store-Klasse fuer den Best-Buy-Laden."""


class Store:
    """Verwaltet eine Sammlung von Produkten."""

    def __init__(self, products=None):
        self.products = list(products) if products else []

    def add_product(self, product):
        """Fuegt dem Store ein Produkt hinzu."""
        self.products.append(product)

    def remove_product(self, product):
        """Entfernt ein Produkt aus dem Store."""
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Gibt zurueck, wie viele Artikel insgesamt im Store liegen."""
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> list:
        """Gibt alle aktiven Produkte zurueck."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list) -> float:
        """Fasst Produkte zusammen und prueft den gesamten Auftrag zuerst."""
        quantities = {}
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Das Produkt gehoert nicht zu diesem Store.")
            if (isinstance(quantity, bool)
                    or not isinstance(quantity, int) or quantity <= 0):
                raise ValueError(
                    "Die Kaufmenge muss eine positive ganze Zahl sein."
                )
            quantities[product] = quantities.get(product, 0) + quantity

        # Mengen, Limits und Aktionen vor jeder Bestandsaenderung pruefen.
        total_price = sum(
            product.get_purchase_price(quantity)
            for product, quantity in quantities.items()
        )
        for product, quantity in quantities.items():
            product.set_quantity(product.quantity - quantity)
        return float(total_price)

    def __contains__(self, product):
        return product in self.products

    def __add__(self, other):
        return Store(self.products + other.products)

    def __str__(self):
        return "\n".join(product.show() for product in self.get_all_products())
