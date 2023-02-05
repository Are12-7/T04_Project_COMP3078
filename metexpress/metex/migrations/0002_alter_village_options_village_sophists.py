# Generated by Django 4.1.4 on 2023-02-05 01:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metex', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='village',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='village',
            name='sophists',
            field=models.ManyToManyField(blank=True, related_name='sophists', to=settings.AUTH_USER_MODEL),
        ),
    ]
