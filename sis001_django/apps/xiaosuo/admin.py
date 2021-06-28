from django.contrib import admin

# Register your models here.

from .models import *

admin.site.site_title = 'sis001资源后台'
admin.site.site_header = "sis001资源后台"


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'collection', 'category', 'classification', 'plate', 'index', 'user', 'crawling_status']

    search_fields = ['name', 'collection__name', 'authur', 'introduction', 'content', 'url']

    date_hierarchy = 'date_joined'

    list_select_related = True  # 减少数据库查询开销
    list_per_page = 25  # 列表显示数据条数


admin.site.register(Chapter, ChapterAdmin)