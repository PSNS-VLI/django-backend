from django.contrib import admin
from .models import GlobalNotice, PersonalNotice
import time

# Register your models here.


@admin.register(GlobalNotice)
class GlobalNoticeAdmin(admin.ModelAdmin):

    fields = ['title', 'content', 'origin']
    # 排序方式
    ordering = ['-date']
    # 排序方式
    sortable_by = ['date']

    list_display = ['id', 'title', 'origin', 'date']

    list_display_links = ['id', 'title']

    list_filter = ['date']
    # 每页数量
    list_per_page = 20

    list_max_show_all = 50

    search_fields = ['id', 'title']
    # 日期选择器
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.operator = request.user
            obj.timestamp = int(time.time() * 1000)
        super().save_model(request, obj, form, change)


@admin.register(PersonalNotice)
class PersonalNoticeAdmin(admin.ModelAdmin):

    fields = ['title', 'content', 'origin', '_to']
    # 排序方式
    ordering = ['-date']
    # 排序方式
    sortable_by = ['date']

    list_display = ['id', 'title', 'origin', 'date']

    list_display_links = ['id', 'title']

    list_filter = ['date']
    # 每页数量
    list_per_page = 20

    list_max_show_all = 50

    search_fields = ['id', 'title']
    # 日期选择器
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.timestamp = int(time.time() * 1000)
        super().save_model(request, obj, form, change)