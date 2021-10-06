from django.db import models

# Create your models here.
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import datetime as dt

from django.db.models.fields import IntegerField


"""USER MODEL"""
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(" User must have an email address")
        if not username:
            raise ValueError(" User must have an username!")    
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username=username,
        )
        user.email = email
        user.is_admin = True 
        user.is_staff = True 
        user.is_superuser = True 
        user.save(using=self._db)
        return user
        
class Users(AbstractBaseUser):
    name = models.CharField( max_length=200)  
    username = models.CharField( max_length=200, blank=True)  
    email = models.CharField( max_length=100, unique=True)
    bio = models.TextField(null=True)
    phone_number = models.CharField(max_length = 15,blank =True)
    profile_photo = CloudinaryField('image', default='image/upload/v1631717620/default_uomrne.jpg') 
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(default=dt.datetime.now)
    is_active = models.BooleanField(default=True)
    is_storeadmin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username']
    
    objects=MyAccountManager()
     
    def _str_(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name_plural='Users'


"""ITEM"""
class Deliveries(models.Model):
    item_code = models.CharField(max_length=50) 
    item_name = models.CharField(max_length=50)  
    status = models.BooleanField(default=False)
    items_received = models.IntegerField(default=0)
    items_spoiled = models.IntegerField(default=0)
    date_delivered = models.DateTimeField(default=dt.datetime.now)


class Item(models.Model):
    item_code = models.CharField(max_length=50) 
    item_name = models.CharField(max_length=50)  
    number_of_items = models.IntegerField(default=0)
    buying_price=models.FloatField(default=0.0)
    selling_price=models.FloatField(default=0.0)


class Request(models.Model):
    item_name = models.CharField(max_length=50)  
    number_of_items = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    clerk = models.ForeignKey("Users",on_delete=models.CASCADE)

