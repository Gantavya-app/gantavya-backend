from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=15, unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




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
    


