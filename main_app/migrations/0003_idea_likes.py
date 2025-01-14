# Generated by Django 5.1.3 on 2024-11-07 18:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_idea_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_ideas', to=settings.AUTH_USER_MODEL),
        ),
    ]
