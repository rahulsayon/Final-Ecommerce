from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save,m2m_changed

import math
User = settings.AUTH_USER_MODEL
# Create your models here.

class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id",None)
        qs = Cart.objects.filter(id=cart_id)
        if qs.count() ==1:
            cart_obj = qs.first()
            new_obj = False
            if cart_obj.user is None and request.user.is_authenticated:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new()
            request.session['cart_id'] = cart_obj.id
            new_obj = True
        return cart_obj,new_obj
    
    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)
        
        
class Cart(models.Model):
    user = models.ForeignKey(User, null=True,blank=True ,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(default=0.00 , max_digits=100,decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(default=0.0,max_digits=100,decimal_places=2)
    
    objects = CartManager()
    
    def __str__(self):
        return str(self.id)
    
    
    

def m2m_save_cart_receiver(sender,action,instance,*args,**kwargs):
    print("action",action)
    if action =="post_add" or action =="post_remove" or action =="post_clear":   
        products = instance.products.all()
        total = 0
        print("products",products)
        for x in products:
            total += x.price
            print("priceeeeeeeeeeeeee",total)
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
    
m2m_changed.connect(m2m_save_cart_receiver,sender=Cart.products.through)


def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    if instance.subtotal > 10:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00
        
pre_save.connect(pre_save_cart_receiver,sender=Cart)