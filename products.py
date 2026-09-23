"""Produktklassen fuer den Best-Buy-Store."""


class Product:
    """Ein normales, lagerhaltiges Produkt."""

    def __init__(self, name, price, quantity):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Der Name darf nicht leer sein.")
        if price < 0:
            raise ValueError("Der Preis darf nicht negativ sein.")
        if quantity < 0:
            raise ValueError("Die Menge darf nicht negativ sein.")
        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = quantity > 0
        self._promotion = None

    # ------------------------------------------------------------------
    # Getter / Setter (klassisch) + Properties (Bonus)
    # ------------------------------------------------------------------
    def get_name(self):
        """Gibt den Namen des Produkts zurueck."""
        return self._name

    @property
    def name(self):
        return self.get_name()

    def get_price(self):
        """Gibt den Preis des Produkts zurueck."""
        return self._price

    def set_price(self, price):
        """Setzt den Preis; negative Preise sind nicht erlaubt."""
        if price < 0:
            raise ValueError("Der Preis darf nicht negativ sein.")
        self._price = price

    @property
    def price(self):
        return self.get_price()

    @price.setter
    def price(self, value):
        self.set_price(value)

    def get_quantity(self) -> float:
        """Gibt die aktuelle Menge zurueck."""
        return self._quantity

    def set_quantity(self, quantity):
        """Setzt die Menge; bei 0 wird das Produkt deaktiviert."""
        if quantity < 0:
            raise ValueError("Die Menge darf nicht negativ sein.")
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def quantity(self):
        return self.get_quantity()

    @quantity.setter
    def quantity(self, value):
        self.set_quantity(value)

    def get_promotion(self):
        """Gibt die aktuelle Aktion zurueck (oder None)."""
        return self._promotion

    def set_promotion(self, promotion):
        """Weist dem Produkt eine Aktion zu (None entfernt sie)."""
        self._promotion = promotion

    @property
    def promotion(self):
        return self.get_promotion()

    @promotion.setter
    def promotion(self, value):
        self.set_promotion(value)

    # ------------------------------------------------------------------
    # Aktiv / Inaktiv
    # ------------------------------------------------------------------
    def is_active(self) -> bool:
        """Gibt zurueck, ob das Produkt aktiv ist."""
        return self._active

    def activate(self):
        """Aktiviert das Produkt."""
        self._active = True

    def deactivate(self):
        """Deaktiviert das Produkt."""
        self._active = False

    @property
    def active(self):
        return self.is_active()

    # ------------------------------------------------------------------
    # Anzeige
    # ------------------------------------------------------------------
    def show(self) -> str:
        """Gibt eine Beschreibung des Produkts als String zurueck."""
        text = (f"{self._name}, Price: ${self._price} "
                f"Quantity:{self._quantity}")
        if self._promotion is not None:
            text += f", Promotion: {self._promotion.name}"
        return text

    def __str__(self):
        return self.show()

    def __repr__(self):
        return (f"{type(self).__name__}({self._name!r}, "
                f"{self._price}, {self._quantity})")

    # ------------------------------------------------------------------
    # Vergleiche (Bonus)
    # ------------------------------------------------------------------
    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price

    # ------------------------------------------------------------------
    # Kaufen
    # ------------------------------------------------------------------
    def buy(self, quantity) -> float:
        """Prueft den Kauf und reduziert danach den Lagerbestand."""
        total_price = self.get_purchase_price(quantity)
        self.set_quantity(self.quantity - quantity)
        return total_price

    def get_purchase_price(self, quantity) -> float:
        """Prueft den Kauf und berechnet den Preis ohne Bestandsaenderung."""
        if (isinstance(quantity, bool)
                or not isinstance(quantity, int) or quantity <= 0):
            raise ValueError("Die Kaufmenge muss groesser als 0 sein.")
        if not self.is_active():
            raise ValueError(f"Das Produkt '{self._name}' ist nicht aktiv.")
        if quantity > self._quantity:
            raise ValueError(
                f"Es sind nur {self._quantity} Stueck von "
                f"'{self._name}' verfuegbar."
            )
        return self._calculate_price(quantity)

    def _calculate_price(self, quantity) -> float:
        """Berechnet den Preis - mit Aktion, falls vorhanden."""
        if self._promotion is not None:
            return self._promotion.apply_promotion(self, quantity)
        return self._price * quantity


class NonStockedProduct(Product):
    """Ein nicht lagerhaltiges Produkt, z. B. eine Software-Lizenz."""

    def __init__(self, name, price):
        super().__init__(name, price, 0)
        self.activate()

    def set_quantity(self, quantity):
        """Die Menge bleibt immer 0."""
        self._quantity = 0

    @Product.quantity.setter
    def quantity(self, value):
        self.set_quantity(value)

    def get_purchase_price(self, quantity) -> float:
        """Prueft den Kauf ohne Lagerbegrenzung und berechnet den Preis."""
        if (isinstance(quantity, bool)
                or not isinstance(quantity, int) or quantity <= 0):
            raise ValueError("Die Kaufmenge muss groesser als 0 sein.")
        if not self.is_active():
            raise ValueError(f"Das Produkt '{self.name}' ist nicht aktiv.")
        return self._calculate_price(quantity)

    def show(self) -> str:
        text = f"{self.name}, Price: ${self.price} Quantity:Unlimited"
        if self.promotion is not None:
            text += f", Promotion: {self.promotion.name}"
        return text


class LimitedProduct(Product):
    """Ein Produkt, das pro Bestellung nur begrenzt gekauft werden darf."""

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Das Maximum muss groesser als 0 sein.")
        self.maximum = maximum

    def get_purchase_price(self, quantity) -> float:
        """Prueft das Bestelllimit und berechnet den Preis ohne Kauf."""
        if quantity > self.maximum:
            raise ValueError(
                f"Von '{self.name}' darf pro Bestellung nur {self.maximum} "
                f"Mal gekauft werden."
            )
        return super().get_purchase_price(quantity)

    def show(self) -> str:
        text = (f"{self.name}, Price: ${self.price} "
                f"Quantity:{self.quantity}, "
                f"Limited to {self.maximum} per order!")
        if self.promotion is not None:
            text += f", Promotion: {self.promotion.name}"
        return text
