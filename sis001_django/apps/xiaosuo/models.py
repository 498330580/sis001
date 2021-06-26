from django.db import models
from users.models import UserProfile

# Create your models here.

TYPE = (
    (0, "无"),
    (1, "小说"),
    (2, "图片")
)

Label = (
    (0, "无")
)

PLATE_TYPE = (
    (0, "无"),
    (1, "原创人生")
)


class Collection(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", default="无")
    category = models.IntegerField(verbose_name="类别", default=0)
    label = models.IntegerField(verbose_name="标签", default=0)
    plate = models.IntegerField(verbose_name="板块", default=0)
    introduction = models.TextField(verbose_name="简介", default="无")
    is_look_count = models.IntegerField(verbose_name="点击次数", default=0, help_text="记录书本被点击的次数")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '合集'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


class Chapter(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", default="无")
    category = models.IntegerField(verbose_name="类别", default=0)
    label = models.IntegerField(verbose_name="标签", default=0)
    plate = models.IntegerField(verbose_name="板块", default=0)
    introduction = models.TextField(verbose_name="简介", default="无")
    is_look_count = models.IntegerField(verbose_name="点击次数", default=0, help_text="记录书本被点击的次数")
    content = models.TextField(verbose_name="内容")
    url = models.URLField(verbose_name="URL")
    crawling_status = models.BooleanField(verbose_name="下载状态", default=False, help_text="用于判断后台脚本是否已爬取内容")
    index = models.IntegerField(verbose_name="索引", default=0)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ["index", '-start', '-date_joined']

    def __str__(self):
        return self.name


class VisitHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(verbose_name="URL")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = 'sis001网站访问历史'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.user


class CollectionCount(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, null=True, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(verbose_name="个人点击次数", default=0)
    collect = models.BooleanField(verbose_name="是否收藏", default=False)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户合集状态'
        verbose_name_plural = verbose_name
        ordering = ['count', '-date_joined']

    def __str__(self):
        return f"{self.user}-{self.collection}-{self.count}"


class ChapterCode(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, verbose_name="章节", on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(verbose_name="个人点击次数", default=0)
    dow_code = models.BooleanField(verbose_name="下载状态", default=False, help_text="用于判断用户是否使用脚本下载过该章节")
    look_code = models.FloatField(validators="章节观看进度", default=0)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户章节观看状态'
        verbose_name_plural = verbose_name
        ordering = ['count', '-date_joined']

    def __str__(self):
        return f"{self.user}-{self.chapter}-{self.count}"


