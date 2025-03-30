from django.db import models
from .constants import NUMBER_OF_PRODUCTS__PER_PAGE
from mongoengine import * 
import uuid
from enum import Enum
from datetime import datetime , timezone

from mongoengine import connect


class CATEGORY(Enum):
    ELECTRONICS = "Electronics"
    GROCERIES = "Groceries"
    LIFESTYLE = "Lifestyle"
    FASHION = "Fashion"
    

class ProductQuerySet(QuerySet):
    
    def fetch_all_products(self , page_number):
        offset = (page_number - 1) * NUMBER_OF_PRODUCTS__PER_PAGE
        return list(self.skip(offset).limit(NUMBER_OF_PRODUCTS__PER_PAGE))  # Returns all products as a list
    
    def get_product_by_id(self, product_id):
        return self.filter(product_id=product_id).first()

    def get_product_by_brand(self, brand_name):
        return list(self.filter(brand=brand_name)) 
    
    def update_product(self , product_id , data):

        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        update_data = {f"set__{k}": v for k, v in data.items()} 
        return self.filter(product_id=product_id).first().update(**update_data)
    
    def delete_product(self , product_id):
        return self.filter(product_id=product_id).delete()
    
    def get_all_products_belonging_to_a_category(self , category):
        category_name = Category.objects(category=category).first()
        return self.filter(category__in=[category_name])
    
    def remove_a_product_from_a_category(self , product_id , category):
        product = self.filter(product_id = product_id).first()
        category_ref = Category.objects(category=category).first()
        if category_ref in product.category:
            product.category.remove(category_ref)
            product.updated_at = datetime.now(timezone.utc)
            product.save()
            
    def add_a_product_to_a_category(self , product_id , category):
        product = self.filter(product_id = product_id).first()
        category_ref = Category.objects(category = category).first()
        
        if category_ref not in product.category:
            product.category.append(category_ref)
            product.updated_at = datetime.now(timezone.utc)
            product.save()
            
    def fetch_product_on_the_basis_of_multiple_filters(self , categories , min_price , max_price):
        category_list = [cat.strip() for cat in categories.split(',')]
        
        category_references = list(Category.objects(category__in=category_list))
                
        
        filters = {
            "category__in": category_references,
            "price__gte": min_price,
            "price__lte": max_price,
            "isAvailable": True
        }
        
        return list(self.filter(**filters))
    

class Category(Document):
    category = EnumField(CATEGORY)

    @classmethod
    def seed_categories(self):
        for enum_item in CATEGORY:
            if not self.objects(category=enum_item.value).first():
                self(category=enum_item.value).save()
                print(f"Added category: {enum_item.value}")
            else:
                print(f"Category already exists: {enum_item.value}")


    

class ProductRepository(Document):
    product_id = StringField(default=lambda: str(uuid.uuid4()), unique=True, required=True)
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = ListField(ReferenceField(Category))
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
    def add_product(cls, name, description, category, price, brand, quantity):
        product = cls(
            name=name,
            description=description,
            category=category,
            price=price,
            brand=brand,
            quantity=quantity,
            created_at = datetime.now(timezone.utc),
            updated_at = datetime.now(timezone.utc),
            isAvailable = True if quantity > 0 else False
        )
        product.save()
        return product