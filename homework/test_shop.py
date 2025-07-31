"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product


@pytest.fixture
def product():
    return Product(
        "book",
        100,
        "This is a book",
        1000)


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

        assert product.quantity == 1000 # количество продуктов не должно измениться


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
