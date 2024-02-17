from django.db import models
from django.contrib.auth.models import AbstractUser #, UserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


# class UserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("Email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
        
#         extra_fields.setdefault("username", None)


#         return self._create_user(email, password, **extra_fields)







class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=15, unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





class Landmark(models.Model):
    name = models.CharField(max_length=300,blank=False, null=False) # Pumdikot Shiva Statue
    address = models.CharField(max_length=300,blank=False, null=False) # Pumdikot
    type = models.CharField(max_length=300,blank=False, null=False) # Temple
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_place(self):
        return self.name+ "," +self.address
    
    def get_info(self):
        return self.description
    

class Photos(models.Model):
    place = models.ForeignKey(Landmark, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    


