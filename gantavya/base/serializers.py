# Serilaize data so that it helps to send json formatted data in api endpoint

from base.models import Landmark, Photos
from rest_framework import serializers
from base.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# serializes all objects of user model
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True) # name of the user
    isAdmin = serializers.SerializerMethodField(read_only=True) # admin status of the user

    class Meta:
        model = User
        fields = ['id','username', 'email', 'name', 'isAdmin'] # fields to be serialized

    def get_id(self, obj): # function to get above mentioned "_id"
        return obj.id # obj is the instance of the User 

    def get_isAdmin(self, obj): # function to get above mentioned "admin status"
        return obj.is_staff

    def get_name(self, obj): # function to get above mentioned "name"
        name = obj.name
        if name == '':
            name = obj.email
        return name
    

# This serializes all objects of User model with JSON Web Token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True) # token for the user
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj): # function that generates token for user
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    



class PhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Photos
        exclude = ['upload_date']

    def get_photo_url(self, photo):
        request = self.context.get('request')
        photo_url = request.build_absolute_uri(photo.photo.url)
        photo_url = request.build_absolute_uri(photo.photo.url)
        # Replace '/images/' with '/static/images/' in the URL
        photo_url = photo_url.replace('/images/', '/static/images/')
        return photo_url



class LandmarkSerializer(serializers.ModelSerializer):

    photos = serializers.SerializerMethodField()

    class Meta:
        model = Landmark
        fields = ['id', 'name', 'address', 'type', 'description', 'facts', 'longitude', 'latitude', 'photos']

    def get_photos(self, landmark):
        photos = landmark.photos.all()
        photo_urls = [self.context['request'].build_absolute_uri(photo.photo.url) for photo in photos]
        photo_urls = [photo_url.replace('/images/', '/static/images/') for photo_url in photo_urls]
        return photo_urls
    