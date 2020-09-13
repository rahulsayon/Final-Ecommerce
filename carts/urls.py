
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  cart_home,cart_update,checkout_home,cart_success
from products.views import product_list_view

urlpatterns = [
    
    path('', cart_home, name="home"),
    path('update/', cart_update, name="update"),
    path('checkout/', checkout_home, name="checkout"),
    path('success/', cart_success , name="success" )  

] 
