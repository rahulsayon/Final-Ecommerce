from django.db import models
import random
import os
from  django.db.models.signals import pre_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q
# Create your models here.
def get_file_extension(filepath):
    base_name = os.path.basename(filepath)
    print("ssss",base_name)
    name,ext  = os.path.splitext(base_name)
    return name,ext


def upload_image_path(instance,filepath):
    newfile_name = random.randint(1,393003030)
    name,ext = get_file_extension(filepath)
    finalname = f'{newfile_name}{ext}'
    return f'products/{newfile_name}/{finalname}'

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)
    
    


class ProductManage(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def featured(self,*args,**kwargs):
        return self.get_queryset().featured()
    
    def all(self,*args,**kwargs):
        return self.get_queryset().active()
       
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
        
    def search(self,query):
        lookup =  (Q(title__icontains=query) | Q(description__icontains=query)
                   |Q(tag__title__icontains=query) | Q(tag__slug__icontains=query)   )
        return self.get_queryset().active().filter(lookup).distinct()
    
    
    
class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2 ,max_digits=10 ,default=39.9)
    image = models.ImageField(upload_to=upload_image_path , null=True,blank=True)
    featured = models.BooleanField(default=True)
    active  = models.BooleanField(default=True)
    
    objects = ProductManage()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return f"/products/{self.slug}"
        return reverse("products:detail" , kwargs={"slug" : self.slug})
    
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)