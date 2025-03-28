from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Author, Category
from .forms import PostForm  # Убедитесь, что в форме нет поля post_type
from .tasks import send_new_post_email
from .filters import PostFilter


# --------------------
# Class-based views
# --------------------

class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.NEWS  # Устанавливаем тип "новость"
        if self.request.user.is_authenticated:
            # Предполагается, что у пользователя есть связанный объект Author
            post.author = self.request.user.author
        post.save()
        form.save_m2m()
        messages.success(self.request, "Новость успешно создана!")
        # Отправляем уведомление подписчикам; замените email-адреса на реальные или настройте сбор адресов из подписчиков
        send_new_post_email.delay(post.title, post.text, ['test1@example.com', 'test2@example.com'])
        return super().form_valid(form)


class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE  # Устанавливаем тип "статья"
        if self.request.user.is_authenticated:
            post.author = self.request.user.author
        post.save()
        form.save_m2m()
        messages.success(self.request, "Статья успешно создана!")
        send_new_post_email.delay(post.title, post.text, ['test1@example.com', 'test2@example.com'])
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('news_list')


# --------------------
# Functional views
# --------------------

def news_search(request):
    qs = Post.objects.all().order_by('-date_created')
    post_filter = PostFilter(request.GET, queryset=qs)
    return render(request, 'news/news_search.html', {'filter': post_filter})


def news_list(request):
    news_queryset = Post.objects.all().order_by('-date_created')
    paginator = Paginator(news_queryset, 10)  # 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj, 'paginator': paginator})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'news/post_detail.html', {'post': post})


def home(request):
    return render(request, 'home.html')


def create_post(request):
    """
    Функциональное представление для создания новости.
    Использует шаблон 'news/news_create.html'.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post_type = Post.NEWS
            if request.user.is_authenticated:
                new_post.author = request.user.author
            new_post.save()
            form.save_m2m()
            messages.success(request, "Новость успешно создана!")
            send_new_post_email.delay(new_post.title, new_post.text, ['test1@example.com', 'test2@example.com'])
            return redirect('news_list')
        else:
            messages.error(request, "Ошибка! Проверьте корректность заполнения формы.")
    else:
        form = PostForm()
    return render(request, 'news/news_create.html', {'form': form})


def create_article(request):
    """
    Функциональное представление для создания статьи.
    Использует шаблон 'articles/post_create.html'.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.post_type = Post.ARTICLE
            if request.user.is_authenticated:
                new_post.author = request.user.author
            new_post.save()
            form.save_m2m()
            messages.success(request, "Статья успешно создана!")
            send_new_post_email.delay(new_post.title, new_post.text, ['test1@example.com', 'test2@example.com'])
            return redirect('news_list')
        else:
            messages.error(request, "Ошибка! Проверьте корректность заполнения формы.")
    else:
        form = PostForm()
    return render(request, 'articles/post_create.html', {'form': form})


def best_info(request):
    best_author = Author.objects.order_by('-rating').first()
    best_article = Post.objects.filter(post_type=Post.ARTICLE).order_by('-rating').first()
    article_comments = best_article.comments.all() if best_article else []
    context = {
        'best_author': best_author,
        'best_article': best_article,
        'article_comments': article_comments,
    }
    return render(request, 'news/best_info.html', context)


@login_required
def subscribe_category(request, pk):
    """
    Представление для подписки на категорию.
    Пользователь добавляется в поле subscribers категории.
    """
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.add(request.user)
    messages.success(request, f"Вы успешно подписались на категорию '{category.name}'!")
    return redirect('category_detail', pk=category.pk)


def category_detail(request, pk):
    """
    Отображает страницу категории с перечнем новостей и кнопкой подписки.
    """
    category = get_object_or_404(Category, pk=pk)
    # Используем related_name 'posts' для получения постов данной категории
    posts = category.posts.all().order_by('-date_created')
    return render(request, 'news/category_detail.html', {'category': category, 'posts': posts})
