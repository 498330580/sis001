# Generated by Django 3.2.4 on 2021-07-04 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiaosuo', '0013_auto_20210704_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncount',
            name='yikan',
            field=models.BooleanField(default=False, verbose_name='是否已看'),
        ),
    ]