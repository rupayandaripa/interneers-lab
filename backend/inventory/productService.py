from .models import ProductRepository

class ProductServices:
    @staticmethod   
    def get_all_products_service(page_number):
        # print(ProductRepository.__dict__.get("objects"))  # Check if it's overridden
        # print(ProductRepository.objects.all())  # Should return a QuerySet
        return ProductRepository.objects.get_all_products_from_mongodb(page_number)
    
    @staticmethod
    def get_product_by_id_service(product_id):
        return ProductRepository.objects.get_product_by_id_from_mongodb(product_id)
    
    @staticmethod
    def get_product_by_brand_service(brand_name):
        return ProductRepository.objects.get_product_by_brand_from_mongodb(brand_name)
    
    @staticmethod
    def add_product_service(name, description, category, price, brand, quantity, isAvailable , created_at , updated_at):
        return ProductRepository.add_product_in_mongodb(name, description, category, price, brand, quantity, isAvailable , created_at , updated_at)
    
    @staticmethod
    def update_product_service(product_id, data):
        return ProductRepository.objects.update_product_in_mongodb(product_id, data)
    
    @staticmethod
    def delete_product_service(product_id):
        return ProductRepository.objects.delete_product_in_mongodb(product_id)
    