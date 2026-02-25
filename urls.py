from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_app.api.urls')),
    path('', include('profil_app.api.urls')),
    path('', include('offers_app.api.urls')),
]
