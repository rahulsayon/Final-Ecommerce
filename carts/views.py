from django.shortcuts import render , redirect
from carts.models import Cart
from django.http import HttpResponse
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from accounts.forms import GuestForm
from addresss.forms import AddressForm
from addresss.models import Address
# Create your views here.

def cart_create():
    cart_obj = Cart.objects.create(user=None)
    return cart_obj

def cart_home(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    context = { 'cart':cart_obj }
    return render(request,"carts/cart_home.html",context)

def cart_update(request):
    product_id = request.POST.get('product_id')
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect("cart:home")
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_item'] = cart_obj.products.count()
    return redirect("cart:home")

def checkout_home(request):
    cart_obj , cart_create = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_create or cart_obj.products.count() == 0:
        return redirect("cart:home")
    form = LoginForm()
    guest_form  = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id',None)
    shipping_address_id = request.session.get('shipping_address_id',None)    
    billing_profile , billing_profile_created =BillingProfile.objects.new_or_get(request) 
    address_qs = None
    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        if request.user.is_authenticated:
            order_obj , order_obj_created = Order.objects.new_or_get(billing_profile=billing_profile, cart_obj=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_done()
            request.session['cart_id'] = 0
            del request.session['cart_id']
        return redirect("/cart/success")
    context={
        "object" : order_obj , 
        "billing_profile" : billing_profile ,
        "form" : form,
        "guest_form" : guest_form,
        "address_form" :address_form,
        "address_qs" : address_qs

        }
    return render(request,"carts/checkout.html",context)


def cart_success(request):
    return render(request,"carts/checkout-done.html")