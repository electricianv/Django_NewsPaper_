from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    """
    Модель автора, связанная с пользователем.
    Рейтинг автора рассчитывается на основе лайков его постов и комментариев.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def update_rating(self):
        """
        Обновляет рейтинг автора по формуле:
          суммарный рейтинг всех постов * 3 +
          суммарный рейтинг комментариев автора +
          суммарный рейтинг комментариев к постам автора.
        """
        posts_rating = self.post_set.aggregate(total=Sum('rating'))['total'] or 0
        user_comments_rating = self.user.comment_set.aggregate(total=Sum('rating'))['total'] or 0
        # Локальный импорт для предотвращения циклических зависимостей
        from .models import Comment
        posts_comments_rating = Comment.objects.filter(post__author=self)\
                                               .aggregate(total=Sum('rating'))['total'] or 0
        self.rating = posts_rating * 3 + user_comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    """
    Модель категории новостей/статей.
    Поле subscribers содержит пользователей, подписанных на данную категорию.
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="Название")
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_categories', verbose_name="Подписчики")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    """
    Модель поста (новости или статьи).
    Содержит заголовок, текст, дату создания, рейтинг, тип поста и связь с категориями через промежуточную модель.
    """
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE, verbose_name="Тип поста")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts', verbose_name="Категории")
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def like(self):
        """Увеличивает рейтинг поста на 1."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг поста на 1."""
        self.rating -= 1
        self.save()

    def preview(self):
        """Возвращает первые 124 символа текста с многоточием."""
        return f'{self.text[:124]}...'

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostCategory(models.Model):
    """
    Промежуточная модель для связи постов с категориями.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'

    class Meta:
        verbose_name = "Категория поста"
        verbose_name_plural = "Категории постов"


class Comment(models.Model):
    """
    Модель комментария к посту.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def __str__(self):
        return f'Комментарий {self.pk} к {self.post.title}'

    def like(self):
        """Увеличивает рейтинг комментария на 1."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг комментария на 1."""
        self.rating -= 1
        self.save()

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
