from django.contrib import admin

# Register your models here.

from .models import *

admin.site.site_title = 'sis001资源后台'
admin.site.site_header = "sis001资源后台"


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'authur', 'collection', 'category', 'classification', 'plate', 'index', 'user', 'crawling_status']

    search_fields = ['name', 'collection__name', 'authur', 'introduction', 'content', 'url']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'authur', 'category', 'classification', 'plate', 'introduction', 'is_look_count']

    search_fields = ['name', 'authur', 'introduction']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']

    search_fields = ['name']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Classification, ClassificationAdmin)
