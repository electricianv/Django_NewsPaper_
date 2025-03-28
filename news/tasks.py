from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from news.models import Category, Post


@shared_task
def send_new_post_email(title, text, recipient_list):
    """
    Отправляет email-письмо подписчикам при создании новой новости.
    Тема письма равна заголовку новости.
    HTML-содержимое письма формируется через шаблон, который включает:
      - Заголовок новости.
      - Первые 50 символов текста.
      - Сообщение: «Здравствуй, username. Новая статья в твоём любимом разделе!».
    """
    html_message = render_to_string('emails/new_post_notification.html', {
        'post_title': title,
        'preview': text[:50],
    })
    send_mail(
        subject=title,
        message="",  # оставляем пустым, т.к. используется html_message
        from_email='your_email@example.com',  # замените на ваш реальный email отправителя
        recipient_list=recipient_list,
        html_message=html_message,
    )


@shared_task
def send_weekly_news():
    """
    Отправляет еженедельный дайджест подписчикам каждой категории.
    Для каждой категории выбираются статьи типа 'Статья' (Post.ARTICLE),
    опубликованные за последние 7 дней. Для каждого подписчика отправляется email,
    содержащий перечень новых статей и ссылки на них.
    """
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    for category in Category.objects.all():
        # Выбираем статьи типа "Статья", созданные за последние 7 дней
        articles = category.posts.filter(post_type=Post.ARTICLE, date_created__gte=one_week_ago)
        if articles.exists():
            subject = f"Недельный дайджест для категории {category.name}"
            message_lines = [f"Новые статьи в категории {category.name} за последнюю неделю:"]
            for article in articles:
                # Формируем полный URL к статье (убедитесь, что get_absolute_url возвращает корректный относительный путь)
                url = f"http://127.0.0.1:8000{article.get_absolute_url()}"
                message_lines.append(f"{article.title}: {url}")
            message = "\n".join(message_lines)
            for subscriber in category.subscribers.all():
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                )
