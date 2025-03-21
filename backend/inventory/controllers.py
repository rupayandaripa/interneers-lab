from .productService import ProductServices
from .categoryService import CategoryServices
from .models import Category
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CATEGORY
from datetime import datetime , timezone
from bson import json_util
from bson import ObjectId

def serialize_product(product):
    
    product_dict = product.to_mongo().to_dict()

    
    product_dict['_id'] = str(product.pk)
    product_dict['product_id'] = str(product.product_id)

   
    if isinstance(product_dict.get('created_at'), datetime):
        product_dict['created_at'] = product_dict['created_at'].isoformat()
    if isinstance(product_dict.get('updated_at'), datetime):
        product_dict['updated_at'] = product_dict['updated_at'].isoformat()

    if 'category' in product_dict:
        product_dict['category'] = [
            Category.objects.with_id(cat.id).category.value if isinstance(cat, ObjectId) else cat.category.value
            for cat in product.category
        ]

    return product_dict


def all_products(request , page_number):
    try:
        allProducts = ProductServices.fetch_all_products(page_number)
    except Exception as e:
            import traceback
            print("ERROR:", traceback.format_exc())
            return JsonResponse({"error": f"Error fetching product: {str(e)}"}, status=500)
    
    return JsonResponse({
            "products": [
                {**product.to_mongo().to_dict(), "_id": str(product.id)}
                for product in allProducts
            ]
        }, status=200)
    
def product_by_id(request, product_id):
    try:
        products = ProductServices.get_product_by_id(product_id)

        if products is None:
            return JsonResponse({"error": "Product does not exist"}, status=404)

        return JsonResponse({
            "product": [
                {**product.to_mongo().to_dict(), "_id": str(product.id)}
                for product in products
            ]
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    
def product_by_brand(request , brand_name):
    try:
        allProducts = ProductServices.get_product_by_brand(brand_name)
    except Exception as e:
            import traceback
            print("ERROR:", traceback.format_exc())
            return JsonResponse({"error": f"Error fetching products of this brand: {str(e)}"}, status=500)
    
    return JsonResponse({
            "products": [
                {**product.to_mongo().to_dict()}
                for product in allProducts
                
            ]
        }, status=200)
    

def product_by_category(request, category):
    try:
        products = CategoryServices.get_product_by_category(category)

        if products is None:
            return JsonResponse({"error": "Product does not exist"}, status=404)
        
        
        product_list = [serialize_product(product) for product in products]

        return JsonResponse({
            "product": product_list
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def add_product(request):
    if request.method == "POST":
        try:
            data = request.POST
            
            name = data.get("name")
            description = data.get("description")
            category = data.get("category")
            price = data.get("price")
            brand = data.get("brand")
            quantity = data.get("quantity")
            isAvailable = data.get("isAvailable")
            created_at = datetime.now(timezone.utc)
            updated_at = datetime.now(timezone.utc)
            
            if None in [name, description, category, price, brand, quantity, isAvailable]:
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            category_list = [cat.strip() for cat in category.split(',')]
            
            valid_categories = {e.value for e in CATEGORY}
            
            invalid_categories = [cat for cat in category_list if cat not in valid_categories]
            
            if invalid_categories:
                return JsonResponse({
                    "error": f"Invalid categories: {invalid_categories}. Allowed values: {list(valid_categories)}"
                }, status=400)
            
            price = float(price)
            quantity = int(quantity)
            isAvailable = isAvailable.lower() == "true"  
            
            category_references = []
            for cat_name in category_list:
                category = Category.objects(category=cat_name).first()
                if category:
                    category_references.append(category)
            
                    
            if not category_references:
                return JsonResponse({"error": "No valid categories found"}, status=400)
            
            product = ProductServices.add_product(
                name, description, category_references, price, brand, quantity, isAvailable , created_at , updated_at
            )
            
            return JsonResponse({
                "success": "Product added successfully",
                "product": {
                    "product_id": product.product_id,
                    "name": product.name,
                    "description": product.description,
                    "category": [cat.category.value for cat in category_references],
                    "price": product.price,
                    "brand": product.brand,
                    "quantity": product.quantity,
                    "isAvailable": product.isAvailable,
                    "created_at" : str(product.created_at),
                    "updated_at" : str(product.updated_at)
                }
            }, status=201)
        
        except Exception as e:
            return JsonResponse({"error": f"Error adding product: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def update_product(request, product_id):
    if request.method == "PUT":
        try:
            raw_data = request.body.decode("utf-8")  # Decode bytes to string
            data = json.loads(raw_data)  # Parse JSON
            
            if "category" in data and data["category"] not in {e.value for e in CATEGORY}:
                return JsonResponse({"error": f"Invalid category. Allowed values: {[e.value for e in CATEGORY]}"}, status=400)
            
            data["updated_at"] = datetime.now(timezone.utc)

            updated_count = ProductServices.update_product(product_id, data)
            
            if updated_count == 0:
                return JsonResponse({"error": "Product not found or no changes made"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=400)

        return JsonResponse({
            "success": "Product details updated successfully",
        }, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def delete_product(request , product_id):
    if request.method == "DELETE":
        try:
            return_data_after_deletion = ProductServices.delete_product(product_id)
            print(type(return_data_after_deletion))
        except:
            return JsonResponse({"error": "Invalid product name"} , status = 404)
        
        return JsonResponse({"success": "Product deleted sucessfully" , "data": return_data_after_deletion} ,status = 200)
    
    return JsonResponse(
        {"error": "Invalid request method",} , 
        status = 400)
    
@csrf_exempt
def remove_product_from_a_category(request , product_id , category):
    if request.method == "DELETE":
        try:
            return_value = CategoryServices.remove_product_from_a_category(product_id , category)
        except Exception as e:
            return JsonResponse({"error": f"Some error occured: {str(e)}"} , status = 400)
        
    return JsonResponse({"success": "Product successfully removed from category"} , status = 200)

@csrf_exempt
def add_product_to_a_category(request , product_id , category):
    try:
        return_value = CategoryServices.add_product_to_a_category(product_id , category)
    except Exception as e:
        return JsonResponse({"error": f"Some error occured: {str(e)}"} , status = 400)
    
    return JsonResponse({"success": "Product successfully added to the category"} , status = 200)
        


def all_products_with_rich_filters(request):
    if request.method == "GET":
        try:
            categories = request.GET.get("categories" , "")
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            allProducts = CategoryServices.fetch_products_using_rich_filters(categories , min_price , max_price)
        except Exception as e:
                import traceback
                print("ERROR:", traceback.format_exc())
                return JsonResponse({"error": f"Error fetching product: {str(e)}"}, status=500)
        
        product_list = [serialize_product(product) for product in allProducts]

        return JsonResponse({
            "product": product_list
        }, status=200)
        
    
    

    