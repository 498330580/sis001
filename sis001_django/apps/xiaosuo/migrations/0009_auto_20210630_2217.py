# Generated by Django 3.2.4 on 2021-06-30 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiaosuo', '0008_auto_20210630_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertovisithistory',
            name='lishi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='xiaosuo.visithistory', verbose_name='访问网址ID'),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='url',
            field=models.URLField(db_index=True, unique=True, verbose_name='URL'),
        ),
    ]
