from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail


User = settings.AUTH_USER_MODEL
# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        guest_Eamil_id = request.session.get('guest_email_id')
        user = request.user
        created = False
        obj = None
        if user.is_authenticated:
            """  login user  """
            obj,created = BillingProfile.objects.get_or_create(user=user,email=user.email)
            print("objfffffffffffff" , obj)
        elif guest_Eamil_id is not None:
            """  guest user  """
            guest_obj = GuestEmail.objects.get(id=guest_Eamil_id)
            obj ,created = BillingProfile.objects.get_or_create(email=guest_obj.email)
        else:
            pass
        return obj,created
    

class BillingProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email = models.CharField(max_length=120  , blank=True,null=True)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = BillingProfileManager()
    
    def __str__(self):
        return self.email
    

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=created,email=instance.email)
        
        
post_save.connect(user_created_receiver,sender=User)