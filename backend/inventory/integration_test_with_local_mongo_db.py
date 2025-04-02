import unittest
import requests
from mongoengine import connect, disconnect
from inventory.models import Category
from inventory.models import ProductRepository
from datetime import datetime , timezone

BASE_URL = "http://127.0.0.1:8000"

def seed_products():
    print("Seeding products...")

    ProductRepository.objects.delete()

    electronics_category = Category.objects(category='Electronics').first()
    fashion_category = Category.objects(category='Fashion').first()

    
    if electronics_category and fashion_category:
        ProductRepository(
            product_id='101',
            name='Laptop',
            description='A high-performance laptop',
            category=[electronics_category],
            price=999.99,
            brand='Dell',
            quantity=10,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ).save()

        ProductRepository(
            product_id='104',
            name='Chair',
            description='Comfortable office chair',
            category=[fashion_category],
            price=199.99,
            brand='Ikea',
            quantity=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ).save()

        print("Products seeded successfully!")

    else:
        print("Categories not found. Please run `seed_categories()` first.")

class IntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('test_db' , host='localhost' , port=27017)
        seed_products()
        

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_get_product_by_id(self):
        
        response = requests.get(f'{BASE_URL}/products/id/101/')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['product']['product_id'], '101')


    def test_filter_products(self):
        
        response = requests.get(f"{BASE_URL}/products/filters?categories=Electronics&min_price=500&max_price=1500")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data['product'][0]['name'], 'Laptop')


    def test_add_product(self):
        
        new_product = {
            "name": "Table",
            "description": "Wooden dining table",
            "category": ["Lifestyle"],
            "price": 499.99,
            "brand": "Ikea",
            "quantity": 8
        }

        response = requests.post(f"{BASE_URL}/products/add_product/", data=new_product)
        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data['product']['name'], new_product['name'])

    def test_update_product(self):
       
        product_id = "101"
        update_data = {
            "price": 1200,
            "quantity": 15
        }

        response = requests.put(f"{BASE_URL}/products/update/{product_id}/", json=update_data)
        self.assertEqual(response.status_code, 200)

        response = requests.get(f"{BASE_URL}/products/id/{product_id}/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['product']['price'], 1200)
        self.assertEqual(data['product']['quantity'], 15)

    
    def test_delete_product(self):
        product_id = "102"

        response = requests.delete(f"{BASE_URL}/products/delete/{product_id}/")
        self.assertEqual(response.status_code, 200)

        response = requests.get(f"{BASE_URL}/products/id/{product_id}/")
        self.assertEqual(response.status_code, 404)

    def test_add_product_to_category(self):
        
        product_id = "101"
        category = "Fashion"

        response = requests.post(f"{BASE_URL}/products/add/{product_id}/{category}/")
        self.assertEqual(response.status_code, 200)

        response = requests.get(f"{BASE_URL}/products/id/{product_id}/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("Fashion", data['product']['category'])

if __name__ == "__main__":
    unittest.main()