#from abc import ABC


class Structure:
    _fields = None
    
    def __init__(self, *args):
        if self._fields is None:
            raise Exception('class attribute _fields not defined')
        if len(self._fields) != len(args):
            raise TypeError(f'Expected {len(self._fields)} arguments')
        for f, v in zip(self._fields, args):
            setattr(self, f, v)
            
    def __repr__(self):
        fieldvalreprs = (repr(getattr(self, f)) for f in self._fields)
        return f'{self.__class__.__name__}({", ".join(fieldvalreprs)})'
        
    def __setattr__(self, name, val):
        if name.startswith('_') or name in self._fields:
            self.__dict__[name] = val
        else:
            raise AttributeError(f'No attribute {name}')
            

def main_6_1():
    class Stock(Structure):
        _fields = ('name','shares','price')

    class Date(Structure):
        _fields = ('year', 'month', 'day')
        
    s = Stock('GOOG',100,490.1)
    print(s.name)
    print(s.shares)
    print(s.price)
    #s = Stock('AA',50)
    print(s)
    s.shares = 50
    s.share = 50
    
if __name__ == '__main__':
    main_6_1()