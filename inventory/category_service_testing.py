import unittest
from unittest.mock import patch , MagicMock
from inventory.categoryService import CategoryServices
from mongoengine import connect , disconnect
import mongomock

class TestProductCategoryServices(unittest.TestCase):
    
    @classmethod 
    def setUpClass(cls):
        connect('test_db' , host = 'mongodb://localhost' , mongo_client_class=mongomock.MongoClient)
        
    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    @patch('inventory.categoryService.ProductRepository')
    def test_get_product_by_category(self , mock_repository):
        
        mock_product1 = MagicMock()
        mock_product1.to_mongo.return_value = {'product_id': '123', 'name': 'Test Product', 'price': 100, 'category': ['Electronics']}
        
        mock_product2 = MagicMock()
        mock_product2.to_mongo.return_value = {'product_id': '124', 'name': 'Test Product 2', 'price': 200, 'category': ['Electronics']}
        
        mock_repository.objects.get_all_products_from_belonging_to_a_category.return_value = [mock_product1 , mock_product2]
        
        products = CategoryServices.get_product_by_category('Electronics')
        
        print("Products" , products)
        
        self.assertEqual(len(products), 2)

        self.assertEqual(products[0].to_mongo(), {'product_id': '123', 'name': 'Test Product', 'price': 100, 'category': ['Electronics']})
        self.assertEqual(products[1].to_mongo(), {'product_id': '124', 'name': 'Test Product 2', 'price': 200, 'category': ['Electronics']})
        
        mock_repository.objects.get_all_products_from_belonging_to_a_category.assert_called_once_with('Electronics')
        
    @patch('inventory.categoryService.ProductRepository')
    def test_add_product_to_category(self, mock_repository):
        
        mock_repository.objects.add_a_product_to_a_category.return_value = True

        result = CategoryServices.add_product_to_a_category(
            '123',
            'Fashion'
        )
        
        self.assertTrue(result)

        mock_repository.objects.add_a_product_to_a_category.assert_called_once_with(
            '123',
            'Fashion'
        )

    @patch('inventory.categoryService.ProductRepository')
    def test_delete_product(self, mock_repository):
        
        mock_repository.objects.remove_a_product_from_a_category.return_value = 1

        product_id = "123"
        result = CategoryServices.remove_product_from_a_category(product_id , 'Electronics')

        self.assertEqual(result, 1)
        mock_repository.objects.remove_a_product_from_a_category.assert_called_once_with(product_id , 'Electronics')
            
    @patch('inventory.categoryService.ProductRepository')
    def test_fetch_products_using_rich_filters(self, mock_repository):
        
        mock_products = [
            {'product_id': '101', 'name': 'Laptop', 'price': 500, 'category': 'Electronics'},
            {'product_id': '102', 'name': 'Smartphone', 'price': 300, 'category': 'Electronics'}
        ]

        
        mock_repository.objects.fetch_product_on_the_basis_of_multiple_filters.return_value = mock_products

        
        result = CategoryServices.fetch_products_using_rich_filters('Electronics', 200, 600)

        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)  
        self.assertEqual(result[0]['name'], 'Laptop')
        self.assertEqual(result[1]['name'], 'Smartphone')

        
        mock_repository.objects.fetch_product_on_the_basis_of_multiple_filters.assert_called_once_with(
            'Electronics', 200, 600
        )
        
if __name__ == '__main__':
    unittest.main()