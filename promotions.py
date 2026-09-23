"""Rabatt-Aktionen (Promotions) fuer den Best-Buy-Store."""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstrakte Basisklasse fuer alle Aktionen."""

    def __init__(self, name):
        if not name:
            raise ValueError("Der Name der Aktion darf nicht leer sein.")
        self._name = name

    def get_name(self):
        """Gibt den Namen der Aktion zurueck."""
        return self._name

    def set_name(self, name):
        """Setzt den Namen der Aktion."""
        if not name:
            raise ValueError("Der Name der Aktion darf nicht leer sein.")
        self._name = name

    @property
    def name(self):
        return self.get_name()

    @name.setter
    def name(self, value):
        self.set_name(value)

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Berechnet den Preis fuer 'quantity' Stueck mit dieser Aktion."""

    def __str__(self):
        return self._name


class PercentDiscount(Promotion):
    """Prozentualer Rabatt, z. B. 20 % auf den Gesamtpreis."""

    def __init__(self, name, percent):
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Der Prozentsatz muss zwischen 0 und 100 liegen.")
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Jeder zweite Artikel kostet nur den halben Preis."""

    def apply_promotion(self, product, quantity) -> float:
        half_price_items = quantity // 2
        full_price_items = quantity - half_price_items
        return (full_price_items * product.price
                + half_price_items * product.price * 0.5)


class ThirdOneFree(Promotion):
    """Zwei kaufen, einen gratis dazu."""

    def apply_promotion(self, product, quantity) -> float:
        free_items = quantity // 3
        return (quantity - free_items) * product.price
