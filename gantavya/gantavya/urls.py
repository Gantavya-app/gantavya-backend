"""
URL configuration for gantavya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import base.views as views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('base.api.urls.user_urls')),
    path("", views.landmark_list, name="list_landmarks"),
    path("create_landmark", views.create_landmark, name="create_landmark"),
    path('landmark/<int:landmark_id>/', views.landmark_detail, name='landmark_detail'),
    path('upload_photo/<int:landmark_id>/', views.upload_photo, name='upload_photo'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('predict/', views.prediction_view, name='prediction'),



    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

