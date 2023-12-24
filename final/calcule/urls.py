from django.urls import path
from . import views

app_name = 'calcule'
urlpatterns = [
path('', views.statistics, name='statistics'),
]