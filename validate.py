class Validator:
    # Don't actually need __init__ here if we have __set_name__ below
    def __init__(self, name=None):
        self.name = name

    # Python 3.6+ only
    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)

class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type}')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass


def add(x,y):
    Integer.check(x)
    Integer.check(y)
    return x + y

class StockOld:
    __slots__ = ('name', '_shares', '_price')
    _types = (str, int, float)
    _validators = (NonEmptyString, PositiveInteger, PositiveFloat)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.name)}, {repr(self.shares)}, {repr(self.price)})'

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = self._validators[1].check(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = self._validators[2].check(value)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares

    def __eq__(self, other):
        return (
            isinstance(other, Stock) and
            (self.name, self.shares, self.price) == (other.name, other.shares, other.price)
        )


class Stock:
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.name)}, {repr(self.shares)}, {repr(self.price)})'

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, shares):
        self.shares -= shares

    def __eq__(self, other):
        return (
            isinstance(other, Stock) and
            (self.name, self.shares, self.price) == (other.name, other.shares, other.price)
        )
