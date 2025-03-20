from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm
from .tasks import send_new_post_email

def news_list(request):
    articles = Article.objects.all().order_by('-date_pub')
    return render(request, 'news/news_list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'news/article_detail.html', {'article': article})

def home(request):
    return render(request, 'home.html')

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_post = form.save()
            # Пока без модели подписчиков — добавим вручную:
            subscriber_emails = ['test1@example.com', 'test2@example.com']
            send_new_post_email.delay(new_post.title, new_post.text, subscriber_emails)
            return redirect('news_list')
    else:
        form = ArticleForm()
    return render(request, 'news/article_create.html', {'form': form})
