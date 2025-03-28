# Generated by Django 5.1.7 on 2025-03-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата записи')),
                ('client_name', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('message', models.TextField(verbose_name='Сообщение')),
            ],
        ),
    ]
