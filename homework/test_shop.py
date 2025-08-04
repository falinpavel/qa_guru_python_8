"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product(
        "book",
        100,
        "This is a book",
        1000)


@pytest.fixture
def empty_cart():
    return Cart()


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
        with pytest.raises(ValueError, match='Not enough products'):
            product.buy(-1)
        with pytest.raises(ValueError, match='Not enough products'):
            product.buy(0)
        assert product.quantity == 1000


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_is_empty(self, empty_cart, product):
        """
        Тест кейс на проверку пустоты корзины
        """
        assert empty_cart.products == {}

    def test_cart_add_product(self, empty_cart, product):
        """
        Тест кейс на добавление продукта в пустую корзину,
        последующие проверки что товар добавился и его количество (проверяем дефолт by_count = 1)
        """
        assert empty_cart.products == {}
        empty_cart.add_product(product=product)
        assert product in empty_cart.products
        assert empty_cart.products == {product: 1}

    def test_cart_add_and_remove_product(self, empty_cart, product):
        """
        Тест кейс на добавление продукта в пустую корзину,
        последующие проверки что товар добавился и его количество,
        затем удаление продукта из корзины методом remove_product
        """
        assert empty_cart.products == {}
        empty_cart.add_product(product=product, buy_count=5)
        assert product in empty_cart.products
        assert empty_cart.products == {product: 5}
        empty_cart.remove_product(product=product, remove_count=1)
        assert empty_cart.products == {product: 4}
        empty_cart.remove_product(product=product)
        assert product not in empty_cart.products
        assert empty_cart.products == {}

    def test_remove_products_from_not_empty_cart(self, not_empty_cart, product):
        """
        Тест кейс на удаление продукта из не пустой корзины
        и проверка исключения KeyError при удалении несуществующего продукта
        """
        assert len(not_empty_cart.products) == 6
        with pytest.raises(KeyError):
            not_empty_cart.remove_product(Product("test", 113, "test test test", 1000))

    def test_cart_clear(self, not_empty_cart):
        """
        Тест кейс на очистку корзины и проверка пустоты
        """
        assert not_empty_cart.products != {}
        not_empty_cart.clear()
        assert not_empty_cart.products == {}

    def test_get_total_price(self, not_empty_cart, product):
        """
        Тест кейс на получение общей стоимости корзины,
        изменение стоимости корзины и проверка
        очищения корзины и ее общей стоимости == 0
        """
        assert not_empty_cart.get_total_price() == 6880
        not_empty_cart.add_product(product=product)
        assert not_empty_cart.get_total_price() == 6980
        not_empty_cart.remove_product(product=product)
        assert not_empty_cart.get_total_price() == 6880
        not_empty_cart.clear()
        assert not_empty_cart.get_total_price() == 0

    def test_buy_one_product_in_cart(self, empty_cart, product):
        """
        Тест кейс на покупку одного продукта в корзине
        с достаточным количеством денег и достаточным колличеством товаров
        и проверка исключений ValueError
        """
        empty_cart.add_product(product, buy_count=1000)
        assert product in empty_cart.products
        assert empty_cart.products[product] == 1000
        empty_cart.buy_one(product=product, quantity=empty_cart.products[product], money=100)
        assert product not in empty_cart.products
        assert empty_cart.products == {}
        empty_cart.add_product(product, buy_count=1000)
        with pytest.raises(ValueError):
            empty_cart.buy_one(product=product, quantity=product.quantity, money=99)
        with pytest.raises(ValueError):
            empty_cart.buy_one(product=product, quantity=1001, money=150)
        with pytest.raises(ValueError):
            empty_cart.buy_one(product=product, quantity=-1, money=150)

    def test_buy_more_then_one_product_in_cart(self, not_empty_cart):
        """
        Тест кейс на покупку всех продуктов в корзине,
        проверки при попытке купить с недостаточным количеством денег
        (проверка исключений ValueError)
        и проверка очистки корзины при успешной покупке
        """
        assert len(not_empty_cart.products) == 6
        assert not_empty_cart.get_total_price() == 6880
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(6879)
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(0)
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(-1)
        not_empty_cart.buy_all_cart(money=6880)
        assert not_empty_cart.products == {}
        assert not_empty_cart.get_total_price() == 0
