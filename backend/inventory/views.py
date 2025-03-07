from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token

# Create your views here.
products = [
    {
        "name": "iPhone 15 Pro",
        "description": "Latest Apple smartphone with A17 Bionic chip and titanium design.",
        "category": "Electronics",
        "price": 999.99,
        "brand": "Apple",
        "quantity": 50,
        "isAvailable": True,
    },
    {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "High-end Android smartphone with 200MP camera and S Pen.",
        "category": "Electronics",
        "price": 1199.99,
        "brand": "Samsung",
        "quantity": 30,
        "isAvailable": True,
    },
    {
        "name": "Sony WH-1000XM5",
        "description": "Premium noise-canceling wireless headphones with superior sound quality.",
        "category": "Audio",
        "price": 399.99,
        "brand": "Sony",
        "quantity": 20,
        "isAvailable": True,
    },
    {
        "name": "Nike Air Force 1",
        "description": "Classic white sneakers with a timeless design.",
        "category": "Footwear",
        "price": 120.00,
        "brand": "Nike",
        "quantity": 100,
        "isAvailable": True,
    },
    {
        "name": "Dell XPS 15",
        "description": "Powerful laptop with Intel Core i9 and 32GB RAM, ideal for professionals.",
        "category": "Laptops",
        "price": 1999.99,
        "brand": "Dell",
        "quantity": 15,
        "isAvailable": True,
    },
    {
        "name": "The Alchemist",
        "description": "Inspirational novel by Paulo Coelho about following one's dreams.",
        "category": "Books",
        "price": 15.99,
        "brand": "HarperCollins",
        "quantity": 75,
        "isAvailable": True,
    },
    {
        "name": "Logitech MX Master 3",
        "description": "Ergonomic wireless mouse with precision control and customizable buttons.",
        "category": "Accessories",
        "price": 99.99,
        "brand": "Logitech",
        "quantity": 40,
        "isAvailable": True,
    },
    {
        "name": "Adidas Ultraboost",
        "description": "High-performance running shoes with energy return technology.",
        "category": "Footwear",
        "price": 180.00,
        "brand": "Adidas",
        "quantity": 50,
        "isAvailable": True,
    },
    {
        "name": "Bose SoundLink Revolve+",
        "description": "Portable Bluetooth speaker with 360-degree sound and deep bass.",
        "category": "Audio",
        "price": 249.99,
        "brand": "Bose",
        "quantity": 25,
        "isAvailable": True,
    },
    {
        "name": "PlayStation 5",
        "description": "Next-gen gaming console with ultra-fast SSD and 4K gaming.",
        "category": "Gaming",
        "price": 499.99,
        "brand": "Sony",
        "quantity": 10,
        "isAvailable": True,
    },
]

def get_csrf_token(request):
    return JsonResponse({"csrfToken" : get_token(request)})

def fetch_all_objects(request):
    return JsonResponse(products , safe=False)

def fetch_product_by_name(request , product_name):
    
    for product in products:
        if product["name"].lower() == product_name.lower() : 
            return JsonResponse(product , status=200)
        
    return JsonResponse({"error": "Product not found"} , status=404)

def fetch_products_by_brand(request , brand_name):
    filtered_products = [product for product in products if product["brand"].lower() == brand_name.lower()]
    return JsonResponse(filtered_products , safe=False)


#csrf-exempt not used in this case as I am generating a csrf token and passing it in my header
def add_product(request):
    #global products 
    if request.method == "POST":
        try:
            data = request.POST #Form data here
            products.append(data)
            return JsonResponse({"message": "Product added successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def update_product(request , product_name):
    #global products
    if request.method == "PUT":
        try:
            data = json.loads(request.body)  #JSON data here
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        for product in products:
            if product["name"] == product_name:
                product.update(data)
                return JsonResponse({"message": "Product updated successfully"})
        return JsonResponse({"error": "Product not found"} , status=404)
    return JsonResponse({"error": "Invalid request"} , status=400)

@csrf_exempt
def delete_product(request , product_name):
    if request.method == "DELETE":
        global products
        products = [product for product in products if product["name"] != product_name]
        return JsonResponse({"message": "Product deleted successfully"})
    return JsonResponse({"error": "Invalid request"} , status=400)
    
    

