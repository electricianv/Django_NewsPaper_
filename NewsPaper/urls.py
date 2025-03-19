from django.contrib import admin
from django.urls import path, include
from news.views import home  # ← Импортируем домашнюю страницу

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', home, name='home'),  # ← Главная страница
]
