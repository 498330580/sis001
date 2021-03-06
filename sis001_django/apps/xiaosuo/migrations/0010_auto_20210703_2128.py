# Generated by Django 3.2.4 on 2021-07-03 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xiaosuo', '0009_auto_20210630_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xiaosuo.collection', verbose_name='合集'),
        ),
        migrations.AlterField(
            model_name='chaptercode',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xiaosuo.chapter', verbose_name='章节'),
        ),
        migrations.AlterField(
            model_name='chaptercode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='访问人'),
        ),
        migrations.AlterField(
            model_name='collectioncount',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xiaosuo.collection', verbose_name='合集'),
        ),
        migrations.AlterField(
            model_name='collectioncount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='usertovisithistory',
            name='lishi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xiaosuo.visithistory', verbose_name='访问网址ID'),
        ),
        migrations.AlterField(
            model_name='usertovisithistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile', verbose_name='访问人'),
        ),
    ]
