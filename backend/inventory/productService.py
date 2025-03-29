from .models import ProductRepository

class ProductServices:
    @staticmethod   
    def fetch_all_products(page_number):
        # print(ProductRepository.__dict__.get("objects"))  # Check if it's overridden
        # print(ProductRepository.objects.all())  # Should return a QuerySet
        return ProductRepository.objects.fetch_all_products(page_number)
    
    @staticmethod
    def get_product_by_id(product_id):
        return ProductRepository.objects.get_product_by_id(product_id)
    
    @staticmethod
    def get_product_by_brand(brand_name):
        return ProductRepository.objects.get_product_by_brand(brand_name)
    
    @staticmethod
    def add_product(name, description, category, price, brand, quantity):
        return ProductRepository.add_product(name, description, category, price, brand, quantity)
    
    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.objects.update_product(product_id, data)
    
    @staticmethod
    def delete_product(product_id):
        return ProductRepository.objects.delete_product(product_id)
        
    