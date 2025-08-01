from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    # def __init__(self, name, price, description, quantity):
    #     self.name = name
    #     self.price = price
    #     self.description = description
    #     self.quantity = quantity
    #
    # def __eq__(self, other):
    #     return (self.name == other.name and
    #             self.price == other.price and
    #             self.description == other.description and
    #             self.quantity == other.quantity)

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return True if self.quantity >= quantity > 0 else False

    def buy(self, quantity) -> None:
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity) is False:
            raise ValueError('Not enough products')
        else:
            self.quantity -= quantity

    def __hash__(self) -> int:
        """
        Метод __hash__ — это специальный метод в Python,
        который позволяет определить как вычислять хеш
        для вашего пользовательского объекта. Он возвращает целое число, хеш объекта.
        """
        return hash((self.name, self.price, self.description, self.quantity))


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """
    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count: int = 1) -> None:
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products.keys():
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count: int = None) -> None:
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if remove_count is None:
            self.products.pop(product)
        else:
            if remove_count > self.products[product]:
                self.products.pop(product)
            else:
                self.products[product] -= remove_count

    def clear(self) -> None:
        self.products.clear()

    def get_total_price(self) -> float:
        return sum([product.price * self.products[product] for product in self.products.keys()])

    def buy_one(self, product: Product, quantity: int, money: int) -> None:
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if money >= product.price:
            if product.check_quantity(quantity) is False:
                raise ValueError('Not enough products')
            elif quantity == product.quantity:
                self.remove_product(product=product)
            else:
                self.remove_product(product=product, remove_count=quantity)
                self.products[product] -= quantity
        else:
            raise ValueError('Not enough money')

    def buy_all_cart(self, money: int) -> None:
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if money >= self.get_total_price():
            self.clear()
        else:
            raise ValueError('Not enough money')
