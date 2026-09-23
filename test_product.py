"""Unit-Tests fuer die Klasse Product."""

import pytest

from products import Product


def test_creating_prod():
    """Ein normales Produkt wird korrekt erzeugt."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True


def test_creating_prod_invalid_details():
    """Ungueltige Details loesen eine Ausnahme aus."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=1450, quantity=-1)


def test_prod_becomes_inactive():
    """Bei Menge 0 wird das Produkt inaktiv."""
    product = Product("MacBook Air M2", price=1450, quantity=1)
    product.buy(1)
    assert product.quantity == 0
    assert product.is_active() is False


def test_buy_modifies_quantity():
    """Ein Kauf reduziert die Menge und liefert den richtigen Preis."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    total_price = product.buy(2)
    assert total_price == 2900
    assert product.quantity == 98


def test_buy_too_much():
    """Ein Kauf ueber den Bestand hinaus loest eine Ausnahme aus."""
    product = Product("MacBook Air M2", price=1450, quantity=10)
    with pytest.raises(ValueError):
        product.buy(11)
