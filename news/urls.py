# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # ← просто пустая строка!
    path('<int:id>/', views.article_detail, name='article_detail'),
]
