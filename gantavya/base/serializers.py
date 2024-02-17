# Serilaize data so that it helps to send json formatted data in api endpoint

from base.models import Landmark, Photos
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# serializes all objects of user model
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True) # name of the user
    _id = serializers.SerializerMethodField(read_only=True) # unique id of the user
    isAdmin = serializers.SerializerMethodField(read_only=True) # admin status of the user

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin'] # fields to be serialized

    def get__id(self, obj): # function to get above mentioned "_id"
        return obj.id # obj is the instance of the User 

    def get_isAdmin(self, obj): # function to get above mentioned "admin status"
        return obj.is_staff

    def get_name(self, obj): # function to get above mentioned "name"
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
    

# This serializes all objects of User model with JSON Web Token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True) # token for the user
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj): # function that generates token for user
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    



class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        exclude = ['upload_date']



class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        exclude = ['created', 'updated']
