from django.shortcuts import render,get_object_or_404,Http404
from . models import Product
from django.views.generic import ListView,DetailView
import ipdb
from django.db.models.signals import pre_save
from carts.models import Cart
# Create your views here.

class ProductFeatureView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"
    
    def get_queryset(self,*args,**kwargs):
        return Product.objects.all().featured()
    
    

class ProductFeatureDetailView(DetailView):
    template_name = "products/feature-details.html"
    queryset = Product.objects.all().featured()
        
        

class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"
    
    # def get_context_data(self,*args,**kwargs):
    #     context = super(ProductListView,self).get_context_data(*args,**kwargs)
    #     print("context", context)
    #     return context
    def get_queryset(self,*args,**kwargs):
        return Product.objects.all()
    
    

def product_list_view(request):
    queryset = Product.objects.all()
    context = { "object_list" : queryset }
    return render(request , "products/list.html" ,context)
        
    
class ProductSlugViewDetail(DetailView):
    template_name = "products/details.html"
    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductSlugViewDetail,self).get_context_data(*args,**kwargs)
        cart_obj , new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
     
    def get_object(self,*args,**kwargs):
        slug = self.kwargs.get('slug')
        # return get_object_or_404(Product,slug=slug)
        try:
            instance = Product.objects.get(active=True,slug=slug)
        except Product.DoesNotExist:
            raise Http404()
        except Product.MultipleObjectsReturned:
            obj = Product.objects.featured(active=True,slug=slug)
            instance = obj.first()
            print("instanceinstance" ,instance)
        return instance
        
    

class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/details.html"
    
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        print("context", context)
        return context
    
    # def get_object(self,*args,**kwargs):
    #     id = self.kwargs.get('pk')
    #     print("ifddddddddddddddddd" , id)
    #     instance = Product.objects.get_by_id(id=id)
    #     if instance is None:
    #         return Http404()
    #     return instance
    
    def get_queryset(self,*args,**kwargs):
        pk = self.kwargs.get('pk')
        obj =   Product.objects.filter(id=pk)
        return obj
    
    


def product_detail_view(request,pk=None,*args,**kwargs):
    # instance  = Product.objects.get(pk=pk)
    instance = get_object_or_404(Product,pk=pk)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("no product here")
    #     raise Http404()
    # except:
    #     print("Hueeee")
    # object = Product.objects.filter(id=pk)
    object = Product.objects.get_by_id(id=pk)
    print("objectobject",object)
    # if object.exists() and object.count() ==1:
    #     instance = object.first()
    context = { "object" : instance }
    return render(request , "products/details.html" ,context)
        
