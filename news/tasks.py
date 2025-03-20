from celery import shared_task
from django.core.mail import send_mail
from .models import Article
from datetime import timedelta, datetime

@shared_task
def send_new_post_email(post_title, post_content, subscriber_emails):
    subject = f'Новая публикация: {post_title}'
    message = post_content
    from_email = 'electricianv@gmail.com'
    send_mail(subject, message, from_email, subscriber_emails)

@shared_task
def send_weekly_news():
    from_email = 'electricianv@gmail.com'
    subject = 'Еженедельная подборка новостей'

    # Выбираем статьи за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    articles = Article.objects.filter(date_pub__gte=week_ago)

    if articles.exists():
        news_list = '\n\n'.join([f"{article.title}\n{article.text}" for article in articles])
    else:
        news_list = 'Новых статей за последнюю неделю нет.'

    message = f'Здравствуйте!\n\nВот свежие новости:\n\n{news_list}'
    subscriber_emails = ['1309306@gmail.com', 'test2@example.com']  # Здесь должны быть реальные подписчики

    send_mail(subject, message, from_email, subscriber_emails)
