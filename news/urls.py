
# urls.py in your Django app
from django.urls import path
from .import views
from .views import article_detail

urlpatterns = [
    path('news/', views.news_list, name='news_list'),  # сопостовляем
    path('news/<slug:slug>/', article_detail, name='article_detail'),
    ]