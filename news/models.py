from django.db import models
from django.shortcuts import reverse


class Article(models.Model):

    title = models.CharField(max_length=64)
    text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class News(models.Model):  # Kept for demonstration

    title = models.CharField(max_length=200)
    text = models.TextField()
    date_pub = models.DateField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(self.title)