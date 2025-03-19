# news/models.py
from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'id': self.pk})
