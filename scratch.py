# exec(open('stock.py').read())

#class Stock:
#    def __init__(self, name, shares, price):
#        self.name = name
#        self.shares = shares
#        self.price = price
#    def __setattr__(self, name, value):
#        if name not in { 'name', 'shares', 'price' }:
#            raise AttributeError('No attribute %s' % name)
#        super().__setattr__(name, value)
#
#s = Stock('GOOG', 100, 490.1)

# class Readonly:
#     def __init__(self, obj):
#         self.__dict__['_obj'] = obj
#     def __setattr__(self, name, value):
#         raise AttributeError("Can't set attribute")
#     def __getattr__(self, name):
#         return getattr(self._obj, name)

# from stock import Stock
# s = Stock('GOOG', 100, 490.1)
# p = Readonly(s)

# class Spam:
#     def a(self):
#         print('Spam.a')
#     def b(self):
#         print('Spam.b')
# class MySpam:
#     def __init__(self):
#         self._spam = Spam()
#     def a(self):
#         print('MySpam.a')
#         self._spam.a()
#     def c(self):
#         print('MySpam.c')
#     def __getattr__(self, name):
#         return getattr(self._spam, name)

# ex5_1

# import reader
# import stock

# port = reader.read_csv_as_dicts('Data/portfolio.csv', [str, int, float])
# print(port)

# print()

# port = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
# print(port)

# print()

# with open('Data/portfolio.csv', 'r') as f:
#     headers = next(f).strip().split(',')
#     port = reader.csv_as_dicts(f, [str,int,float], headers=headers)
#     print(port)

# ex5_2

# def parse_line(line):
#     try:
#         name, value = line.split('=', 1)
#     except ValueError:
#         return None
#     return name, value

# import time
# def worker(x, y):
#     print('About to work')
#     time.sleep(20)
#     print('Done')
#     return x + y
    
# # >>> import threading
# # >>> t = threading.Thread(target=worker, args=(2, 3))
# # >>> t.start()

# # Note the problem of not knowing when the worker is completed, also the return value of the worker is not captured

# import threading
# from concurrent.futures import Future
# # Wrapper around the function to use a future
# def do_work(x, y, fut):
#     fut.set_result(worker(x,y))

# # >>> fut = Future()
# # >>> t = threading.Thread(target=do_work, args=(2, 3, fut))
# # >>> t.start()
# # About to work  
# # >>> result = fut.result()
# # Done
# # >>> result
# # 5
# # >>>

# # Good example of threading

# # >>> from concurrent.futures import ThreadPoolExecutor
# # >>> pool = ThreadPoolExecutor()
# # >>> fut = pool.submit(worker, 2, 3)
# # About to work
# # >>> fut
# # <Future at 0x102157080 state=running>
# # >>> fut.result()
# # Done
# # 5
# # >>>

# ex5_3

# from reader import convert_csv

# def make_dict(headers, row):
#     return dict(zip(headers, row))

# lines = open('Data/portfolio.csv')
# print(convert_csv(lines, make_dict))

# print()

# import reader
# import stock

# port = reader.read_csv_as_dicts('Data/portfolio.csv', [str, int, float])
# print(port)

# print()

# port = reader.read_csv_as_instances('Data/portfolio.csv', stock.Stock)
# print(port)

# ex5_4

# # closure as a data structure
# def counter(value):
#     def incr():
#         nonlocal value
#         value += 1
#         return value
        
#     def decr():
#         nonlocal value
#         value -= 1
#         return value
        
#     return incr, decr
    
# up, down = counter(0)
# print(up())
# print(up())
# print(up())
# print(down())
# print(down())

# from typedproperty import typedproperty

# class Stock:
#     name = typedproperty('name', str)
#     shares = typedproperty('shares', int)
#     price = typedproperty('price', float)

#     def __init__(self, name, shares, price):
#         self.name = name
#         self.shares = shares
#         self.price = price
        
# s = Stock('GOOG', 100, 490.10)
# print(s.name)
# print(s.shares)
# s.shares = 75
# try:
#     s.shares = '75'  # TypeError
# except TypeError as e:
#     print(e)

# from typedproperty import String, Integer, Float

# class Stock:
#     name = String('name')
#     shares = Integer('shares')
#     price = Float('price')
#     def __init__(self, name, shares, price):
#         self.name = name
#         self.shares = shares
#         self.price = price

# s = Stock('GOOG', 100, 490.10)
# print(s.name)
# print(s.shares)
# s.shares = 75
# try:
#     s.shares = '75'  # TypeError
# except TypeError as e:
#     print(e)

# print('---')
    
# from typedproperty import String2, Integer2, Float2

# class Stock2:
#     name = String2()
#     shares = Integer2()
#     price = Float2()

#     def __init__(self, name, shares, price):
#         # print(self.name, self.shares, self.price)
#         self.name = name
#         self.shares = shares
#         self.price = price

# s = Stock2('GOOG', 100, 490.10)
# print(s.name)
# print(s.shares)
# s.shares = 75
# print(s.shares)
# try:
#     s.shares = '75'  # TypeError
# except TypeError as e:
#     print(e)
# print(s.shares)

# ex5_5

# from reader import read_csv_as_dicts
# port = read_csv_as_dicts('Data/missing.csv', types=[str, int, float])

import reader
import logging
logging.basicConfig(level=logging.DEBUG)
port = reader.read_csv_as_dicts('Data/missing.csv', types=[str, int, float])