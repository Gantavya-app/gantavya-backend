from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.serializers import UserSerializer,  UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status
# Create your views here



@api_view(["GET"])
def homeUser(request):
    api_list = {
        'login':'api/users/'
    }
    return Response(api_list)


## LOGIN with JWT authentication
# refer documentation
class MyTokenObtainPairSerializer(TokenObtainPairSerializer): # class that returns user with token
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView): # to login the user
    serializer_class = MyTokenObtainPairSerializer



## Register user
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            username = data['username'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':"The user with given credentials already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    


# Admin to look at all users
@api_view(['GET'])
@permission_classes([IsAdminUser]) # function decorator to check whether requesting user is authenticated and admin or not
def getUsers(request): # function to get all users in the database
    # getting all users
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



# Delete a user (For admin only)
@api_view(['DELETE']) # api call with http request - DELETE
@permission_classes([IsAdminUser])
def deleteUser(request, pk): # function to delete user by id
    # getting user by id
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')



# Get user by their unique id (For admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk): # function to get details of a user by id
    # getting user by id
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# Admin can update user by their id
@api_view(['PUT']) # api call with http request - PUT
@permission_classes([IsAdminUser])
def updateUser(request, pk): 
    # getting user by id
    user = User.objects.get(id=pk)
    # getting data from request and updating
    data = request.data
    user.first_name = data['name']
    user.email = data['email']
    user.username = data['username']
    user.is_staff = data['isAdmin']
    
    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



# Update user (By user themselves)
@api_view(['PUT']) # api call with http request - PUT
@permission_classes([IsAuthenticated]) # function decorator to check whether the requesting user is authenticated or not
def updateUserProfile(request): 
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    # updating user details
    user.first_name = data['name']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])
    # saving user object
    user.save()
    
    return Response(serializer.data)


#  User requesting other users profile 
@api_view(['GET']) # api call with http request - GET
@permission_classes([IsAuthenticated]) # function decorator to check whether the requesting user is authenticated or not
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)