from django.urls import path
from base.api.views import landmark_view as views


urlpatterns = [
    path('',views.landmark_list, name='get_all_landmarks'),
    path('upload_photo/<str:pk>', views.upload_photo, name='photo_upload'),
    path('delete_photo/<str:pk>', views.delete_photo, name="photo_delete"),
    
    path('landmark/<str:pk>', views.landmark_detail, name='landmark'),
    path('create/', views.create_landmark, name='create_landmark'),
    path('saved_by/', views.save_landmark, name="saved_by"),

    path('prediction/', views.prediction, name='prediction'),

]