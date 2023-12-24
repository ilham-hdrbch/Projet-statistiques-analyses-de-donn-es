from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'matapp'
urlpatterns = [
    path('',views.upload,name="upload"),
]