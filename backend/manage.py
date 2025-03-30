#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from datetime import datetime , timezone
from mongoengine import connect
from inventory.models import ProductRepository , Category

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
# import django
# django.setup()



def migrate_product_categories():
    print("Starting product category migration....")
    
    connect('Inventory' , host='localhost' , port=27017)
    print("Database connected successfully.........")
    Category.seed_categories()
    print("Categories seeded")
    
    products = ProductRepository.objects()
    for product in products:
        if isinstance(product.category , list) and all(isinstance(cat , Category) for cat in product.category):
            print(f"Skipping product {product.product_id} (already migrated)")
            continue
        
        if isinstance(product.category , str):
            category_ref = Category.objects(category = product.category).first()
            
        if category_ref:
            product.category = [category_ref]
        else :
            product.category = []
            
        product.updated_at = datetime.now(timezone.utc)
        
        try:
            product.save()
        except Exception as e:
            print(f"Failed to migrate product {product.product_id}: {e}")
            


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    
    if "runserver" not in sys.argv:
        migrate_product_categories() 
    main()
