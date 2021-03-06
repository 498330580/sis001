# Generated by Django 3.2.4 on 2021-06-30 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xiaosuo', '0007_auto_20210630_2040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visithistory',
            options={'ordering': ['-date_joined'], 'verbose_name': '用户已访问过的sis001网站网址', 'verbose_name_plural': '用户已访问过的sis001网站网址'},
        ),
        migrations.AlterField(
            model_name='collectioncount',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
