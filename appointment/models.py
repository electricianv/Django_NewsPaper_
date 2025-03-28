from django.db import models

class Appointment(models.Model):
    date = models.DateTimeField(verbose_name="Дата записи")
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    message = models.TextField(verbose_name="Сообщение")

    def __str__(self):
        return f"{self.client_name} на {self.date.strftime('%d.%m.%Y')}"
from django.db import models

# Create your models here.
