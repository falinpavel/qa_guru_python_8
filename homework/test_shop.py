"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        product_apple = Product(name="apple", price=3.35, description="This is green apple", quantity=30)
        print(product_apple.check_quantity(33))
        product_banana = Product(name="banana", price=1.99, description="This is yellow banana", quantity=10)
        product_orange = Product(name="orange", price=2.85, description="This is orange", quantity=15)
        product_pineapple = Product(name="pineapple", price=9.99, description="This is red pineapple", quantity=5)
        pass

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        pass

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        pass


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
