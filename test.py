import unittest
from app import Product, Analyte

class Product_TestCase(unittest.TestCase):

    def test_init(self):
        '''Test Product object initialization'''

        product = Product(name='Product 1')
        with self.subTest():
            self.assertEqual(product.is_explosive, False)
        with self.subTest():
            self.assertEqual(product.is_associate_administer_exempt, False)
        with self.subTest():
            self.assertEqual(product.is_forbidden_for_transport, False)
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, True)