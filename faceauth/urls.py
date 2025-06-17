from django.contrib import admin
from django.urls import path
from .import views



urlpatterns = [
 
    path('faceregister/', views.register_page, name='face_register'),
    path('facelogin/', views.login_user, name='login_user'),
    
   
]