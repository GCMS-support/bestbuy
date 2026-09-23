"""Regressionstests fuer komplette Bestellungen."""
import pytest
from products import Product, LimitedProduct, NonStockedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


def test_repeated_macbook_receives_discount():
    product = Product("MacBook Air M2", 1450, 100)
    product.promotion = SecondHalfPrice("Second Half Price!")
    assert Store([product]).order([(product, 1), (product, 1)]) == 2175
    assert product.quantity == 98


def test_repeated_earbuds_receive_third_free():
    product = Product("Bose", 250, 500)
    product.promotion = ThirdOneFree("Third One Free!")
    assert Store([product]).order([(product, 1)] * 3) == 500
    assert product.quantity == 497


@pytest.mark.parametrize("split", [False, True])
def test_shipping_limit_preserves_entire_inventory(split):
    mac = Product("MacBook Air M2", 1450, 2)
    shipping = LimitedProduct("Shipping", 10, 250, 1)
    basket = [(mac, 2)] + ([(shipping, 1)] * 2 if split else [(shipping, 2)])
    with pytest.raises(ValueError):
        Store([mac, shipping]).order(basket)
    assert (mac.quantity, mac.active) == (2, True)
    assert (shipping.quantity, shipping.active) == (250, True)


def test_combined_stock_limit_preserves_inventory():
    first = Product("First", 10, 1)
    second = Product("Second", 20, 3)
    with pytest.raises(ValueError):
        Store([first, second]).order([(first, 1), (second, 2), (second, 2)])
    assert (first.quantity, first.active) == (1, True)
    assert second.quantity == 3


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "1"])
def test_invalid_line_cannot_be_hidden_by_aggregation(quantity):
    product = Product("Product", 10, 10)
    with pytest.raises(ValueError):
        Store([product]).order([(product, 2), (product, quantity)])
    assert product.quantity == 10


def test_successful_mixed_order():
    mac = Product("MacBook Air M2", 1450, 2)
    mac.promotion = SecondHalfPrice("Second Half Price!")
    license = NonStockedProduct("Windows", 125)
    license.promotion = PercentDiscount("30% off!", 30)
    shipping = LimitedProduct("Shipping", 10, 250, 1)
    total = Store([mac, license, shipping]).order(
        [(mac, 1), (license, 2), (mac, 1), (shipping, 1)])
    assert total == 2360
    assert (mac.quantity, mac.active) == (0, False)
    assert (license.quantity, license.active) == (0, True)
    assert shipping.quantity == 249


def test_promotion_error_does_not_reduce_inventory():
    class BrokenPromotion:
        def apply_promotion(self, product, quantity):
            raise RuntimeError("Promotion failed")
    first = Product("First", 10, 1)
    second = Product("Second", 20, 2)
    second.promotion = BrokenPromotion()
    with pytest.raises(RuntimeError):
        Store([first, second]).order([(first, 1), (second, 1)])
    assert (first.quantity, first.active) == (1, True)
    assert second.quantity == 2


def test_inactive_product_does_not_reduce_other_inventory():
    first = Product("First", 10, 1)
    second = Product("Second", 20, 2)
    second.deactivate()
    with pytest.raises(ValueError):
        Store([first, second]).order([(first, 1), (second, 1)])
    assert first.quantity == 1
    assert second.active is False


def test_foreign_product_is_rejected():
    first = Product("First", 10, 1)
    second = Product("Second", 20, 2)
    with pytest.raises(ValueError):
        Store([first]).order([(first, 1), (second, 1)])
    assert first.quantity == 1
    assert second.quantity == 2


def test_empty_order():
    assert Store().order([]) == 0.0


def test_zero_stock_starts_inactive():
    assert Product("Empty", 10, 0).active is False
    assert NonStockedProduct("License", 10).active is True


def test_direct_special_product_purchases():
    license = NonStockedProduct("License", 125)
    assert license.buy(3) == 375
    assert (license.quantity, license.active) == (0, True)
    shipping = LimitedProduct("Shipping", 10, 2, 1)
    with pytest.raises(ValueError):
        shipping.buy(2)
    assert shipping.quantity == 2
    assert shipping.buy(1) == 10
    assert shipping.quantity == 1


def test_properties_keep_classic_accessors_working():
    product = Product("Product", 10, 2)
    product.price = 20
    product.quantity = 1
    assert product.get_price() == 20
    assert product.get_quantity() == 1
    assert product.name == product.get_name()
    with pytest.raises(ValueError):
        product.price = -1
