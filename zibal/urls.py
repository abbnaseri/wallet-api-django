from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('accounts.urls')),
    path('api/', include('my_app.urls')),
    path('o/', include('oauth2_provider.urls')),
    path('admin/', admin.site.urls),
]
