from .productService import ProductServices
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CATEGORY
from datetime import datetime , timezone

def all_products(request , page_number):
    try:
        allProducts = ProductServices.get_all_products_service(page_number)
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
        products = ProductServices.get_product_by_id_service(product_id)

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
        allProducts = ProductServices.get_product_by_brand_service(brand_name)
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
            
            # Check for missing fields
            if None in [name, description, category, price, brand, quantity, isAvailable]:
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            if "category" in data and data["category"] not in {e.value for e in CATEGORY}:
                return JsonResponse({"error": f"Invalid category. Allowed values: {[e.value for e in CATEGORY]}"}, status=400)
            
            price = float(price)
            quantity = int(quantity)
            isAvailable = isAvailable.lower() == "true"  
            
            product = ProductServices.add_product_service(
                name, description, category, price, brand, quantity, isAvailable , created_at , updated_at
            )
            
            return JsonResponse({
                "success": "Product added successfully",
                "product": {
                    "product_id": product.product_id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category.value,
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

            updated_count = ProductServices.update_product_service(product_id, data)
            
            if updated_count == 0:
                return JsonResponse({"error": "Product not found or no changes made"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=400)

        return JsonResponse({
            "success": "Product details updated successfully",
            "updated_count": updated_count
        }, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def delete_product(request , product_id):
    if request.method == "DELETE":
        try:
            return_data_after_deletion = ProductServices.delete_product_service(product_id)
            print(type(return_data_after_deletion))
        except:
            return JsonResponse({"error": "Invalid product name"} , status = 404)
        
        return JsonResponse({"success": "Product deleted sucessfully" , "data": return_data_after_deletion} ,status = 200)
    
    return JsonResponse(
        {"error": "Invalid request method",} , 
        status = 400)
    
    

    