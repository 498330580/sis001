# Generated by Django 3.2.4 on 2021-06-30 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xiaosuo', '0004_auto_20210627_1056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chaptercode',
            options={'ordering': ['count', '-date_joined'], 'verbose_name': '用户章节观看状态（个人进度）', 'verbose_name_plural': '用户章节观看状态（个人进度）'},
        ),
        migrations.AlterModelOptions(
            name='collectioncount',
            options={'ordering': ['count', '-date_joined'], 'verbose_name': '用户合集状态（书架）', 'verbose_name_plural': '用户合集状态（书架）'},
        ),
        migrations.AlterField(
            model_name='chapter',
            name='crawling_status',
            field=models.BooleanField(default=False, help_text='用于判断后台脚本是否已爬取内容', verbose_name='爬取状态'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='plate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='xiaosuo.plate', verbose_name='板块'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='plate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='xiaosuo.plate', verbose_name='板块'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='plate',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
    ]
