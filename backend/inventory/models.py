from django.db import models
from .constants import NUMBER_OF_PRODUCTS__PER_PAGE
from mongoengine import * 
import uuid
from enum import Enum
from datetime import datetime , timezone


class CATEGORY(Enum):
    ELECTRONICS = "Electronics"
    GROCERIES = "Groceries"
    LIFESTYLE = "Lifestyle"
    FASHION = "Fashion"
    

class ProductQuerySet(QuerySet):
    
    def get_all_products_from_mongodb(self , page_number):
        offset = (page_number - 1) * NUMBER_OF_PRODUCTS__PER_PAGE
        return list(self.skip(offset).limit(NUMBER_OF_PRODUCTS__PER_PAGE))  # Returns all products as a list
    
    def get_product_by_id_from_mongodb(self, product_id):
        return self.filter(product_id=product_id)

    def get_product_by_brand_from_mongodb(self, brand_name):
        return list(self.filter(brand=brand_name)) 
    
    def update_product_in_mongodb(self , product_id , data):
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        
        print(type(data))
        update_data = {f"set__{k}": v for k, v in data.items()} 
        print(f"Converted update data: {update_data}")
        return self.filter(product_id=product_id).update(**update_data)
    
    def delete_product_in_mongodb(self , product_id):
        return self.filter(product_id=product_id).delete()
    
    
class ProductRepository(Document):
    product_id = StringField(default=lambda: str(uuid.uuid4()), unique=True, required=True)
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = EnumField(CATEGORY)
    price = FloatField(required=True)
    brand = StringField(max_length=150)
    quantity = IntField()
    isAvailable = BooleanField(default=True)
    created_at = DateTimeField(default= lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default= lambda: datetime.now(timezone.utc))
    meta = {'queryset_class': ProductQuerySet}
    
    @queryset_manager
    def objects(cls, queryset):
        return queryset 

    @classmethod
    def add_product_in_mongodb(cls, name, description, category, price, brand, quantity, isAvailable , created_at , updated_at):
        product = cls(
            name=name,
            description=description,
            category=category,
            price=price,
            brand=brand,
            quantity=quantity,
            isAvailable=isAvailable,
            created_at=created_at,
            updated_at=updated_at
        )
        product.save()
        return product
    
