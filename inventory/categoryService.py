from .models import ProductRepository

class CategoryServices:
    @staticmethod
    def get_product_by_category(category):
        return ProductRepository.objects.get_all_products_from_belonging_to_a_category(category)
    
    @staticmethod
    def remove_product_from_a_category(product_id , category):
        return ProductRepository.objects.remove_a_product_from_a_category(product_id , category)
    
    @staticmethod
    def add_product_to_a_category(product_id , category):
        return ProductRepository.objects.add_a_product_to_a_category(product_id , category)
    
    @staticmethod 
    def fetch_products_using_rich_filters(category , min_price , max_price):
        return ProductRepository.objects.fetch_product_on_the_basis_of_multiple_filters(category , min_price , max_price)