# Generated by Django 4.2.13 on 2024-07-14 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_text_new_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date_pub', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='New',
            new_name='Article',
        ),
    ]
