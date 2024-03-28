from functools import total_ordering

# https://docs.python.org/3/library/functools.html#functools.total_ordering
# Decorator fills in missing comparison methods as long as __eq__ and one
# other relation like __lt__ is defined
@total_ordering
class MutInt:
    __slots__ = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        # String that when eval'ed will recreate this instance
        return f'MutInt({self.value!r})'

    def __format__(self, fmt):
        return format(self.value, fmt)

    def __add__(self, other):
        if isinstance(other, MutInt):
            return MutInt(self.value + other.value)
        elif isinstance(other, int):
            return MutInt(self.value + other)
        else:
            return NotImplemented

    __radd__ = __add__  # Reversed operands

    def __iadd__(self, other):
        if isinstance(other, MutInt):
            self.value += other.value
            return self
        elif isinstance(other, int):
            self.value += other
            return self
        else:
            return NotImplemented

    def __eq__(self, other):
        # https://peps.python.org/pep-0636/#adding-a-ui-matching-objects
        #     A pattern like KeyPress(), with no arguments will match any
        #     object which is an instance of the KeyPress class. Only the
        #     attributes you specify in the pattern are matched, and any
        #     other attributes are ignored.
        match other:
            case MutInt():
                return self.value == other.value
            case int():
                return self.value == other
            case _:
                return NotImplemented

    def __lt__(self, other):
        match other:
            case MutInt():
                return self.value < other.value
            case int():
                return self.value < other
            case _:
                return NotImplemented

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    __index__ = __int__
