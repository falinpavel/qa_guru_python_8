"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture(scope="function")
def book_product() -> Product:
    return Product(
        name="book",
        price=100,
        description="This is a book",
        quantity=1000)


@pytest.fixture(scope="function")
def pen_product() -> Product:
    return Product(
        name="pen",
        price=12,
        description="This is a simple pen",
        quantity=7000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, book_product: Product):
        # TODO напишите проверки на метод check_quantity
        assert book_product.check_quantity(-1) is False
        assert book_product.check_quantity(0) is False
        assert book_product.check_quantity(1) is True
        assert book_product.check_quantity(book_product.quantity - 1) is True
        assert book_product.check_quantity(book_product.quantity) is True
        assert book_product.check_quantity(book_product.quantity + 1) is False

    def test_product_buy(self, book_product: Product):
        # TODO напишите проверки на метод buy
        assert book_product.quantity == 1000
        assert book_product.check_quantity(1000) is True
        book_product.buy(1)
        assert book_product.quantity == 999
        assert book_product.check_quantity(1000) is False
        assert book_product.check_quantity(999) is True
        book_product.buy(999)
        assert book_product.quantity == 0
        assert book_product.check_quantity(1) is False

    def test_product_buy_more_than_available(self, book_product: Product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        assert book_product.quantity == 1000
        with pytest.raises(ValueError, match='Not enough products'):
            book_product.buy(book_product.quantity + 1)
        with pytest.raises(ValueError, match='Not enough products'):
            book_product.buy(-1)
        with pytest.raises(ValueError, match='Not enough products'):
            book_product.buy(0)
        assert book_product.quantity == 1000


@pytest.fixture(scope="function")
def empty_cart() -> Cart:
    return Cart()


@pytest.fixture(scope="function")
def not_empty_cart() -> Cart:
    cart = Cart()
    product_list = (
        Product(name="book1", price=100, description="This is a book1", quantity=1000),
        Product(name="book2", price=141, description="This is a book2", quantity=800),
        Product(name="book3", price=78, description="This is a book3", quantity=300),
        Product(name="book4", price=32, description="This is a book4", quantity=1000),
        Product(name="book5", price=111, description="This is a book5", quantity=950),
        Product(name="book6", price=213, description="This is a book6", quantity=1200)
    )
    for product in product_list:
        cart.add_product(product, buy_count=10)
    return cart


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_is_empty(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на проверку пустоты корзины
        """
        assert empty_cart.products == {}

    def test_cart_add_product(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на добавление продукта в пустую корзину,
        последующие проверки что товар добавился и его количество (проверяем дефолт by_count = 1)
        """
        assert empty_cart.products == {}
        empty_cart.add_product(product=book_product)
        assert book_product in empty_cart.products
        assert empty_cart.products[book_product] == 1
        empty_cart.add_product(product=book_product, buy_count=5)
        assert empty_cart.products[book_product] == 6

    def test_cart_add_product_more_than_available(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на добавление такого количества продуктов в корзину, чем
        есть в наличии
        """
        assert empty_cart.products == {}
        with pytest.raises(ValueError, match='Not enough products'):
            empty_cart.add_product(product=book_product, buy_count=book_product.quantity + 1)

    def test_cart_add_product_zero_and_negative_quantity(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на добавление нулевого и
        отрицательного количества продуктов в корзину
        """
        assert empty_cart.products == {}
        with pytest.raises(ValueError, match='You can not buy zero or negative products'):
            empty_cart.add_product(product=book_product, buy_count=0)
        with pytest.raises(ValueError, match='You can not buy zero or negative products'):
            empty_cart.add_product(product=book_product, buy_count=-1)

    def test_cart_add_and_remove_product(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на добавление продукта в пустую корзину,
        последующие проверки что товар добавился и его количество,
        затем удаление продукта из корзины методом remove_product
        """
        assert empty_cart.products == {}
        empty_cart.add_product(product=book_product, buy_count=5)
        assert book_product in empty_cart.products
        assert empty_cart.products[book_product] == 5
        empty_cart.remove_product(product=book_product, remove_count=1)
        assert empty_cart.products[book_product] == 4
        empty_cart.remove_product(product=book_product)
        assert book_product not in empty_cart.products
        assert empty_cart.products == {}

    def test_cart_add_two_different_products(self, empty_cart: Cart,
                                             book_product: Product, pen_product: Product):
        """
        Тест кейс на добавление двух разных продуктов в одну корзину
        """
        empty_cart.add_product(product=book_product)
        empty_cart.add_product(product=pen_product, buy_count=150)
        assert len(empty_cart.products) == 2
        assert book_product in empty_cart.products
        assert empty_cart.products[book_product] == 1
        assert pen_product in empty_cart.products
        assert empty_cart.products[pen_product] == 150

    def test_cart_remove_non_existent_product(self, not_empty_cart: Cart, book_product: Product):
        """
        Тест кейс на удаление продукта из не пустой корзины
        и проверка исключения KeyError при удалении несуществующего продукта
        """
        assert len(not_empty_cart.products) == 6
        with pytest.raises(KeyError, match='Product not in cart'):
            not_empty_cart.remove_product(Product("test", 113, "test test test", 1000))
        with pytest.raises(KeyError, match='Product not in cart'):
            not_empty_cart.remove_product(book_product)

    def test_cart_when_remove_count_more_than_quantity(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на удаление проверку условия,
        что удаляем всю позицию из корзины
        если remove_count > quantity
        """
        empty_cart.add_product(product=book_product)
        empty_cart.remove_product(product=book_product, remove_count=book_product.quantity + 1)
        assert len(empty_cart.products) == 0

    def test_no_empty_cart_clear(self, not_empty_cart):
        """
        Тест кейс на очистку корзины и проверка что она действительно стала пустой
        """
        assert not_empty_cart.products
        not_empty_cart.clear()
        assert not not_empty_cart.products

    def test_empty_cart_clear(self, empty_cart):
        """
        Тест кейс на очистку корзины и проверка что она действительно стала пустой
        """
        assert not empty_cart.products
        empty_cart.clear()
        assert not empty_cart.products

    def test_cart_get_total_price_many_products(self, not_empty_cart: Cart, book_product: Product):
        """
        Тест кейс на получение общей стоимости корзины
        в которой много продуктов
        изменение стоимости корзины в процессе и проверка
        очищения корзины и определения ее общей стоимости == 0
        """
        assert not_empty_cart.get_total_price() == 6750.0
        not_empty_cart.add_product(product=book_product)
        assert not_empty_cart.get_total_price() == 6850.0
        not_empty_cart.remove_product(product=book_product)
        assert not_empty_cart.get_total_price() == 6750.0
        not_empty_cart.clear()
        assert not_empty_cart.get_total_price() == 0

    def test_cart_get_total_price_one_product(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на получение общей стоимости корзины
        в которой есть один продукт
        """
        empty_cart.add_product(product=book_product)
        assert empty_cart.get_total_price() == book_product.price

    def test_cart_get_total_price_empty(self, empty_cart: Cart):
        """
        Тест кейс на получение общей стоимости пустой корзины
        """
        empty_cart.clear()
        assert empty_cart.get_total_price() == 0

    def test_cart_buy_one_product(self, empty_cart: Cart, book_product: Product):
        """
        Тест кейс на покупку одного продукта в корзине
        с достаточным количеством денег и достаточным колличеством товаров
        и проверка исключений ValueError
        """
        empty_cart.add_product(book_product, buy_count=1000)
        assert book_product in empty_cart.products
        assert empty_cart.products[book_product] == 1000
        empty_cart.buy_one(product=book_product, quantity=1000, money=100)
        assert book_product not in empty_cart.products
        assert empty_cart.products == {}
        # empty_cart.add_product(product, buy_count=1000)
        # with pytest.raises(ValueError, match='Not enough money'):
        #     empty_cart.buy_one(product=product, quantity=product.quantity, money=99)
        # with pytest.raises(ValueError, match='Not enough products'):
        #     empty_cart.buy_one(product=product, quantity=1001, money=150)
        # with pytest.raises(ValueError, match='Not enough products'):
        #     empty_cart.buy_one(product=product, quantity=-1, money=150)
        # assert empty_cart.products == {product: 1000}
        # empty_cart.buy_one(product=product, quantity=None, money=100)

    def test_cart_buy_more_then_one_product(self, not_empty_cart: Cart):
        """
        Тест кейс на покупку всех продуктов в корзине,
        проверки при попытке купить с недостаточным количеством денег
        (проверка исключений ValueError)
        и проверка очистки корзины при успешной покупке
        """
        assert len(not_empty_cart.products) == 6
        assert not_empty_cart.get_total_price() == 6750.0
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(money=6749)
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(money=0)
        with pytest.raises(ValueError):
            not_empty_cart.buy_all_cart(money=-1)
        not_empty_cart.buy_all_cart(money=6750)
        assert not_empty_cart.products == {}
        assert not_empty_cart.get_total_price() == 0
        assert len(not_empty_cart.products) == 0
