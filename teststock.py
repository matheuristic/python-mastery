import unittest
import stock

class TestStock(unittest.TestCase):
    def test_create(self):
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
        
    def test_create_kw(self):
        s = stock.Stock(name='GOOG', shares=100, price=490.1)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)
        
    def test_cost(self):
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(s.cost, 49010.0)
        
    def test_sell(self):
        s = stock.Stock('GOOG', 100, 490.1)
        s.sell(25)
        self.assertEqual(s.shares, 75)
        
    def test_from_row(self):
        row = ("GOOG", 100, 490.1)
        s = stock.Stock.from_row(row)
        self.assertEqual(s.name, 'GOOG')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test___repr__(self):
        s = stock.Stock('GOOG', 100, 490.1)
        self.assertEqual(repr(s), "Stock('GOOG', 100, 490.1)")
        
    def test___eq__(self):
        s1 = stock.Stock('GOOG', 100, 490.1)
        s2 = stock.Stock('GOOG', 100, 490.1)
        self.assertTrue(s1 == s2)
        
    def test_bad_shares_str(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
            s.shares = '50'
            
    def test_bad_shares_neg(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
            s.shares = -50
            
    def test_bad_price_str(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(TypeError):
            s.price = '490.1'
            
    def test_bad_price_neg(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(ValueError):
            s.price = -490.1
    
    def test_bad_attrib(self):
        s = stock.Stock('GOOG', 100, 490.1)
        with self.assertRaises(AttributeError):
            s.share = 100


if __name__ == '__main__':
    unittest.main()
