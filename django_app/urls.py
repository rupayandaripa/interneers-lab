from django.contrib import admin
from django.urls import path , include
from django.http import HttpResponse
from django.http import JsonResponse

def hello_world(request):
    return HttpResponse("Hello fellow Rippterns!! Rupayan this side!!")

def hello_name(request):
    name = request.GET.get("name" , "World")
    return JsonResponse({"message": f"Hello , {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    path('' , include('inventory.urls'))
]
