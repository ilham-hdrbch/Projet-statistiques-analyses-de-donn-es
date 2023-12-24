from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('calcule/', include('calcule.urls')),
    path('matapp/', include('matapp.urls')),
    path('analyse/', include('analyse.urls')),
    path('proba/', include('proba.urls')),
    path('', include('calcule.urls')),
]
