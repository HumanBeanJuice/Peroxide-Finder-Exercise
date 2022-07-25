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

    def test_is_explosive(self):
        '''Test setting the Product attribute and confirm the regulatory definition is correctly applied'''

        product = Product(name='Product 1', is_explosive=True)
        with self.subTest():
            self.assertEqual(product.is_explosive, True)
        with self.subTest():
            self.assertEqual(product.regulatory_definition, '49 CFR 173.128(a)(1)')
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, False)

    def test_is_forbidden_for_transport(self):
        '''Test setting the Product attribute and confirm the regulatory definition is correctly applied'''

        product = Product(name='Product 1', is_forbidden_for_transport = True)
        with self.subTest():
            self.assertEqual(product.is_forbidden_for_transport, True)
        with self.subTest():
            self.assertEqual(product.regulatory_definition, '49 CFR 173.128(a)(2)')
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, False)

    def test_is_associate_administer(self):
        '''Test setting the Product attribute and confirm the regulatory definition is correctly applied'''

        product = Product(name='Product 1', is_associate_administer_exempt = True)
        with self.subTest():
            self.assertEqual(product.is_associate_administer_exempt, True)
        with self.subTest():
            self.assertEqual(product.regulatory_definition, '49 CFR 173.128(a)(3)')
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, False)

    # Test organic peroxide function on example test data

    def test_organic_peroxide_example_data_true(self):
        '''Test Product method for calculating the organic_peroxide_calculator - True Case'''

        product = Product(name='Product 1')
        self.assertEqual(product.is_organic_peroxide, True)
    
    # Test example results for 4-1 exempt example data

    def test_organic_peroxide_example_data_false_4_1(self):
        '''Test Product method for calculating the organic_peroxide_calculator - False Cases'''

        product = Product(name='Product 4')
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, False)
        with self.subTest():
            self.assertEqual(product.regulatory_definition, '49 CFR 173.128(a)(4)(i)')

    def test_organic_peroxide_example_data_false_4_2(self):

        product = Product(name='Test Product')
        with self.subTest():
            self.assertEqual(product.is_organic_peroxide, False)
        with self.subTest():
            self.assertEqual(product.regulatory_definition, '49 CFR 173.128(a)(4)(ii)')



unittest.main()