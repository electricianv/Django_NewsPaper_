from django.contrib import admin
from django.urls import path, include
from news.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),


]
