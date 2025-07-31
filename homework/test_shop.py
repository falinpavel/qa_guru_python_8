"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    my_product = Product(
        "book",
        100,
        "This is a book",
        1000
    )
    return my_product


@pytest.fixture
def empty_cart():
    cart = Cart()
    return cart


@pytest.fixture
def not_empty_cart():
    cart = Cart()
    product_list = (
        Product("book1", 113, "This is a book1", 1000),
        Product("book2", 141, "This is a book2", 800),
        Product("book3", 78, "This is a book3", 300),
        Product("book4", 32, "This is a book4", 10),
        Product("book5", 111, "This is a book5", 950),
        Product("book6", 213, "This is a book6", 1200)
    )
    for product in product_list:
        cart.add_product(product, 10)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(-1) is False
        assert product.check_quantity(0) is False
        assert product.check_quantity(1) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        assert product.quantity == 1000
        assert product.check_quantity(1000) is True
        product.buy(1)
        assert product.quantity == 999
        assert product.check_quantity(1000) is False
        assert product.check_quantity(999) is True
        product.buy(999)
        assert product.quantity == 0
        assert product.check_quantity(1) is False

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        assert product.quantity == 1000
        with pytest.raises(ValueError, match='Not enough products'):
            product.buy(product.quantity + 1)
            product.buy(-1)
        assert product.quantity == 1000  # количество продуктов не должно измениться


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_is_empty(self, empty_cart, product):
        assert empty_cart.products == {}

    def test_cart_add_product(self, empty_cart, product):
        assert empty_cart.products == {}
        empty_cart.add_product(product)
        assert product in empty_cart.products
        assert empty_cart.products == {product: 1}

    def test_cart_add_and_remove_product(self, empty_cart, product):
        assert empty_cart.products == {}
        empty_cart.add_product(product, 5)
        assert product in empty_cart.products
        assert empty_cart.products == {product: 5}
        empty_cart.remove_product(product, 1)
        assert empty_cart.products == {product: 4}
        empty_cart.remove_product(product)
        assert product not in empty_cart.products
        assert empty_cart.products == {}

    def test_remove_products_from_not_empty_cart(self, not_empty_cart, product):
        assert len(not_empty_cart.products) == 6

    def test_cart_clear(self, not_empty_cart):
        assert not_empty_cart.products != {}
        not_empty_cart.clear()
        assert not_empty_cart.products == {}

    def test_get_total_price(self, not_empty_cart, product):
        assert not_empty_cart.get_total_price() == 6880
        not_empty_cart.add_product(product)
        assert not_empty_cart.get_total_price() == 6980
        not_empty_cart.remove_product(product)
        assert not_empty_cart.get_total_price() == 6880
        not_empty_cart.clear()
        assert not_empty_cart.get_total_price() == 0

    def test_buy(self, empty_cart, product):
        assert empty_cart.products == {}
        empty_cart.add_product(product)
        assert product in empty_cart.products
        assert empty_cart.products == {product: 1}
        empty_cart.buy(product, 1)
