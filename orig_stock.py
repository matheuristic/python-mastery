import csv, sys
from decimal import Decimal


class Stock:
    __slots__ = ('name', '_shares', '_price')
    _types = (str, int, float)

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
        typ = self._types[1]
        if not isinstance(value, typ):
            raise TypeError(f'Expected {typ.__name__}')
        if value < 0:
            raise ValueError('shares must be >= 0')
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        typ = self._types[2]
        if not isinstance(value, typ):
            raise TypeError(f'Expected {typ.__name__}')
        if value < 0:
            raise ValueError('price must be >= 0')
        self._price = value

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


#def read_portfolio(filename):  # ex1_5
def read_portfolio(filename, cls=Stock):
    portfolio = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            # ex1_5
            #name, shares, price = row
            #shares = int(shares)
            #price = float(price)
            #s = Stock(name, shares, price)
            # ex3_3
            s = cls.from_row(row)
            portfolio.append(s)
    return portfolio


def print_portfolio(portfolio):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print('{0:-<10s} {1:-<10s} {2:-<10s}'.format('', '', ''))
    for s in portfolio:
        print(f'{s.name:>10s} {s.shares:>10d} {s.price:>10.2f}')


class DStock(Stock):
    _types = (str, int, Decimal)


class redirect_stdout:
    def __init__(self, out_file):
        self.out_file = out_file
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file
    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout
