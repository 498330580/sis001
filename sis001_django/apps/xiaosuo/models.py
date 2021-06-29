from django.db import models
from users.models import UserProfile

# Create your models here.

TYPE = (
    (0, "无"),
    (1, "小说"),
    (2, "图片")
)

# Label = (
#     (0, "无"),
# )
#
# PLATE_TYPE = (
#     (0, "无"),
#     (1, "原创人生")
# )


# 分类
class Classification(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="标签", max_length=500)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


# 版块
class Plate(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="板块", max_length=500)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '板块'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.name


# 合集（BOOK)
class Collection(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", max_length=100, default="无")
    category = models.IntegerField(verbose_name="类别", choices=TYPE, default=0)
    classification = models.ForeignKey(Classification, verbose_name="分类", on_delete=models.SET_NULL, null=True, blank=True)
    plate = models.ForeignKey(Plate, verbose_name="板块", on_delete=models.SET_NULL, null=True, blank=True)
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


# 章节
class Chapter(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="添加人", on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(verbose_name="名称", max_length=500)
    authur = models.CharField(verbose_name="作者", max_length=100, default="无")
    category = models.IntegerField(verbose_name="类别", choices=TYPE, default=0)
    classification = models.ForeignKey(Classification, verbose_name="分类", on_delete=models.SET_NULL, null=True, blank=True)
    plate = models.ForeignKey(Plate, verbose_name="板块", on_delete=models.SET_NULL, null=True, blank=True)
    introduction = models.TextField(verbose_name="简介", default="无")
    is_look_count = models.IntegerField(verbose_name="点击次数", default=0, help_text="记录书本被点击的次数")
    content = models.TextField(verbose_name="内容", null=True, blank=True)
    url = models.URLField(verbose_name="URL")
    crawling_status = models.BooleanField(verbose_name="爬取状态", default=False, help_text="用于判断后台脚本是否已爬取内容")
    index = models.IntegerField(verbose_name="索引", default=0)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
        ordering = ["index", '-date_joined']

    def __str__(self):
        return self.name


# sis001已访问的网页
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


# 用户合集（BOOK）的收藏状态（对于自己的前端，判断是否加入收藏）
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


# # 用户合集（BOOK）的收藏状态（对于sis001网站，用于判断是否储存数据库）
# class CollectionCode(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, null=True, blank=True)
#     collection = models.ForeignKey(Collection, verbose_name="合集", on_delete=models.CASCADE, null=True, blank=True)
#
#     date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
#
#     class Meta:
#         verbose_name = '用户合集在sis001上的状态'
#         verbose_name_plural = verbose_name
#         ordering = ['count', '-date_joined']
#
#     def __str__(self):
#         return f"{self.user}-{self.collection}"


# 用户章节的状态（对于自己的前端）
class ChapterCode(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="访问人", on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, verbose_name="章节", on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(verbose_name="个人点击次数", default=0)
    dow_code = models.BooleanField(verbose_name="下载状态", default=False, help_text="用于判断用户是否使用脚本下载过该章节")
    look_code = models.FloatField(verbose_name="章节观看进度", null=True, blank=True, default=None)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户章节观看状态'
        verbose_name_plural = verbose_name
        ordering = ['count', '-date_joined']

    def __str__(self):
        return f"{self.user}-{self.chapter}-{self.count}"
