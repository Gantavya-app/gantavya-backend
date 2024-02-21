from django.urls import path
from base.api.views import landmark_view as views


urlpatterns = [
    path('',views.landmark_list, name='get_all_landmarks'),
    

]