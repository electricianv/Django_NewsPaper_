
from django.shortcuts import render, get_object_or_404
from .models import Article

def news_list(request):
    articles = Article.objects.all().order_by('-date_pub')  # Сортировка по дате
    context = {'articles': articles}
    return render(request, 'news/news_list.html', context)

def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    context = {'article': article}
    return render(request, 'news/article_detail.html', context)
def home(request):
    return render(request, 'home.html')