from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import User
from base.serializers import UserSerializer,  UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re
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
        # Validate name is not empty
        if not data.get('name'):
            raise ValidationError("Name name cannot be empty.")
        
        # Validate name contains only alphabets and spaces
        if not re.match(r'^[a-zA-Z\s]+$', data['name']):
            raise ValidationError("Name can only contain alphabetical words and space between them")

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data.get('email')):
            raise ValidationError("Invalid email format.")

        # # Validate username format (alphanumeric characters and underscores only)
        # if not re.match(r'^[a-zA-Z0-9_]+$', data.get('username')):
        #     raise ValidationError("Username must contain only letters, numbers, or underscores.")

        # Validate password length and complexity
        password = data.get('password')
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?`~' for char in password):
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one digit, and one special character.")

        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            username=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    # error message is of form:   {detail:"['Invalid email format']"}
    # Changing the format to:     {detail:"Invalid email format"}  
    except ValidationError as e:
        error_message = str(e)
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e).strip("[]").strip("'")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


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



@api_view(['DELETE']) # api call with http request - DELETE
@permission_classes([IsAuthenticated])
def deleteUserProfile(request): # function to delete user when requested by themselves
    userForDeletion = request.user
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
    user.name = data['name']
    user.email = data['email']
    user.username = data['username']
    user.is_staff = data['isAdmin']
    
    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request): 

    try:
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)
        data = request.data

        # Validate name is not empty
        if 'name' in data and data['name']:
            user.name = data['name']

        # Validate email format and update
        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
                raise ValidationError("Invalid email format.")
            user.email = data['email']

        # Save user object
        user.save()
        
        return Response(serializer.data)
    
    except ValidationError as e:
        error_message = str(e)
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e).strip("[]").strip("'")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#  User requesting their profile 
@api_view(['GET']) # api call with http request - GET
@permission_classes([IsAuthenticated]) # function decorator to check whether the requesting user is authenticated or not
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def changePassword(request):

    try:
        user = request.user
        data = request.data

        # Fetch old password and compare
        old_password = data.get('old_password', None)
        if not old_password or not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")

        # Validate new password
        new_password = data.get('new_password', None)
        if not new_password or len(new_password) < 8 or not any(char.isupper() for char in new_password) or not any(char.isdigit() for char in new_password) or not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?`~' for char in new_password):
            raise ValidationError("New password must be at least 8 characters long and contain at least one uppercase letter, one digit, and one special character.")
        
        # Ensure new password is different from old password
        if old_password == new_password:
            raise ValidationError("New password must be different from old password.")

        # Update password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully."})
    
    except ValidationError as e:
        error_message = str(e)
        return Response({"detail": error_message.strip("[]").strip("'")}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e).strip("[]").strip("'")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)