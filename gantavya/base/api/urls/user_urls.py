from django.urls import path
from base.api.views import user_views as views


urlpatterns = [
    path('',views.homeUser, name='home_user'),
    
    path('getusers/', views.getUsers, name="users"), # api url route to get all users
    path('login/', views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"), # api url route to login and get auth token

    path('register/', views.registerUser, name="register"), # api url route to register new user

    path('profile/', views.getUserProfile, name="users-profile"), # api url route to get profile details
    path('profile/update/', views.updateUserProfile, name="user-profile-update"), # api url route to update profile
    path('profile/delete', views.deleteUserProfile, name='user-profile-delete'), # delete user by user themselves

    path('<str:pk>/', views.getUserById, name='user'), # api url route to get details of a user using "id"
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'), # api url route to delete a user
    path('update/<str:pk>/', views.updateUser, name='user-update'), # api url route to update user details
    

]
