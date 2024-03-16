from django.contrib import admin
from django.urls import path,include
from information import views

urlpatterns = [
    path('',views.upload_file,name='upload_file'),
    # path('text/',views.extract,name='extract'),
   
]
