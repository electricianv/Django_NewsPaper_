from django.urls import path
from . import views

urlpatterns = [
    # Список новостей и детальный просмотр
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),

    # Создание новостей – оба подхода с разными именами (функциональное и CBV)
    path('create/', views.create_post, name='create_post'),
    path('news_create/', views.NewsCreateView.as_view(), name='news_create'),


    # Редактирование и удаление новостей (CBV)
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),

    # Поиск новостей
    path('search/', views.news_search, name='news_search'),

    # Лучшие новости/авторы и т.п.
    path('best/', views.best_info, name='best_info'),

    # Маршруты для создания, редактирования и удаления статей (отдельно)
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='articles_delete'),

    path('categories/<int:pk>/subscribe/', views.subscribe_category, name='subscribe_category'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
]
