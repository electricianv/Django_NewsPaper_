import logging
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from news.models import Post, Category

logger = logging.getLogger(__name__)


# Задача для теста, выводящая сообщение каждые 10 секунд
def my_job():
    print('hello from job')


# Функция для удаления устаревших записей APScheduler
def delete_old_job_executions(max_age=604_800):
    """Удаляет записи APScheduler, старше max_age секунд (по умолчанию 1 неделя)."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


# Функция отправки еженедельного дайджеста подписчикам
def send_weekly_digest():
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
                # Формируем полный URL к статье; убедитесь, что get_absolute_url возвращает правильный относительный путь
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
                logger.info(f"Weekly digest sent to {subscriber.email} for category {category.name}")


class Command(BaseCommand):
    help = "Runs apscheduler jobs."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем тестовую задачу, выполняемую каждые 10 секунд
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        # Добавляем задачу удаления устаревших записей APScheduler каждую неделю в понедельник в 00:00
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        # Добавляем задачу еженедельного дайджеста каждую неделю в понедельник в 00:00
        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly digest job 'weekly_digest'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
