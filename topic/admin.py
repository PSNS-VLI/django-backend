from django.contrib import admin
from .models import Topic
import time


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # 可以修改的字段
    fields = ['name', 'introduction', 'visitor_num', 'heat', 'is_main',
              'recommend', 'commerce', 'top']

    # 排序方式
    ordering = ['-create_timestamp', '-visitor_num']
    # 排序方式
    sortable_by = ['create_timestamp', 'visitor_num']
    # 展示信息
    list_display = ['id', 'create_time', 'name', 'visitor_num', 'top', 'recommend', 'commerce']
    # 链接字段
    list_display_links = ['id', 'name']

    list_filter = ['create_time', 'recommend', 'commerce', 'top']
    # 每页数量
    list_per_page = 50

    list_max_show_all = 50
    # 搜索字段
    search_fields = ['name']
    # 日期选择器
    date_hierarchy = 'create_time'

    # def get_readonly_fields(self, request, obj=None):
    #
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     else:
    #         self.readonly_fields = ['content', 'visitor_num']
    #
    #     return self.readonly_fields
    def save_model(self, request, obj, form, change):
        if change:
            tag = '修改'
        else:
            tag = '新建'
        operator = request.user.username
        log = operator + tag + '了：' + str(obj.pk) + '\n'
        with open('topic.txt', 'a', encoding='utf-8') as logs:
            logs.write(log)
        timestamp = int(time.time())
        obj.create_timestamp = timestamp
        obj.update_timestamp = timestamp
        super().save_model(request, obj, form, change)
