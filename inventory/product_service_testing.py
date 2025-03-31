import unittest
from unittest.mock import patch , MagicMock
from inventory.productService import ProductServices
from mongoengine import connect , disconnect
import mongomock
from inventory.models import Category
from parameterized import parameterized

class TestProductServices(unittest.TestCase):
    
    @classmethod 
    def setUpClass(cls):
        connect('test_db' , host = 'mongodb://localhost' , mongo_client_class=mongomock.MongoClient)
        Category.seed_categories()
        
    @classmethod
    def tearDownClass(cls):
        disconnect()
    
    @parameterized.expand([
        ("test_1" , "123" , "Test Product 1" , 100),
        ("test_2" , "456" , "Test Product 2" , 200),
        ("test_3" , "789" , "Test Product 3" , 300),
    ])
    def test_get_product_by_id(self , name , product_id , price , mock_repository):
        
        with patch('inventory.productService.ProductRepository') as mock_repository:
            mock_product = MagicMock()
            mock_product.to_mongo.return_value = {'product_id': product_id , 'name': name , 'price': price}
            mock_repository.objects.get_product_by_id.return_value = mock_product
        
            product = ProductServices.get_product_by_id(product_id)
        
            self.assertIsNotNone(product)
            self.assertEqual(product.to_mongo() , {'product_id': product_id, 'name': name, 'price': price})
            mock_repository.objects.get_product_by_id.assert_called_once_with(product_id=product_id)
        
        
    @patch('inventory.productService.ProductRepository')
    def test_add_product(self, mock_repository):
        
        mock_repository.add_product.return_value = MagicMock()

        result = ProductServices.add_product(
            name="Test Product",
            description="Test Description",
            category="Electronics",
            price=999.99,
            brand="TestBrand",
            quantity=10
        )

        mock_repository.add_product.assert_called_once_with(
            name="Test Product",
            description="Test Description",
            category="Electronics",
            price=999.99,
            brand="TestBrand",
            quantity=10
        )

        
        self.assertIsNotNone(result)


    @patch('inventory.productService.ProductRepository')
    def test_update_product(self, mock_repository):

        mock_queryset = MagicMock()
        mock_repository.objects.update_product.return_value = mock_queryset


        mock_queryset.first.return_value.update.return_value = 1


        product_id = "123"
        data = {"price": 1500, "quantity": 5}
        result = ProductServices.update_product(product_id, data)

        self.assertIsNotNone(result)
        mock_repository.objects.update_product.assert_called_once_with(product_id, data)


    @patch('inventory.productService.ProductRepository')
    def test_delete_product(self, mock_repository):
        
        mock_repository.objects.delete_product.return_value = 1

        product_id = "123"
        result = ProductServices.delete_product(product_id)

        self.assertEqual(result, 1)
        mock_repository.objects.delete_product.assert_called_once_with(product_id)
        
    @patch('inventory.productService.ProductRepository')
    def test_get_products_by_brand_name(self , mock_repository):
            
        mock_product1 = MagicMock()
        mock_product1.to_mongo.return_value = {'product_id': '123' , 'name': 'Test Product' , 'price': 100 , 'brand': 'Dell'}
        
        mock_product2 = MagicMock()
        mock_product2.to_mongo.return_value = {'product_id': '124' , 'name': 'Test Product 2' , 'price': 1000 , 'brand': 'Dell'}
        
        mock_repository.objects.get_product_by_brand.return_value = [mock_product1 , mock_product2]
            
        products = ProductServices.get_product_by_brand('Dell')
            
        self.assertIsNotNone(products)
        self.assertEqual(len(products) , 2)
        
        self.assertEqual(products[0].to_mongo() , {'product_id': '123' , 'name': 'Test Product' , 'price': 100 , 'brand': 'Dell'})
        self.assertEqual(products[1].to_mongo() , {'product_id': '124' , 'name': 'Test Product 2' , 'price': 1000 , 'brand': 'Dell'})
        mock_repository.objects.get_product_by_brand.assert_called_once_with('Dell')
            
        
        
if __name__ == '__main__':
    unittest.main()