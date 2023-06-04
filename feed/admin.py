from django.contrib import admin
from .models import Feed, News


# Register your models here.


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    # 可以修改的字段
    fields = ['convert_content', 'visitor_num', 'fk_topic']
    filter_horizontal = ['fk_topic']
    # 排序方式
    ordering = ['-create_timestamp', '-visitor_num']
    # 排序方式
    sortable_by = ['create_timestamp', 'visitor_num']
    # 展示信息
    list_display = ['id', 'create_time', 'content', 'fk_qquser', 'visitor_num']
    # 链接字段
    list_display_links = ['id', 'content']

    list_filter = ['create_time']
    # 每页数量
    list_per_page = 50

    list_max_show_all = 50
    # 搜索字段
    search_fields = ['content']
    # 日期选择器
    # date_hierarchy = 'create_timestamp'

    def save_model(self, request, obj, form, change):
        if change:
            tag = '修改'
        else:
            tag = '新建'
        operator = request.user.username
        log = operator + tag + '了：' + str(obj.pk) + '\n'
        with open('hot_log.txt', 'a', encoding='utf-8') as logs:
            logs.write(log)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ['content', 'visitor_num', 'fk_topic']

        return self.readonly_fields


@admin.register(News)
class MewAdmin(admin.ModelAdmin):
    # 可以修改的字段
    fields = ['id', 'title', 'content', 'recommend', 'url'
              'commerce', 'top', 'tag', 'visitor']
    readonly_fields = ['id', 'url']
    # 排序方式
    ordering = ['-date', '-visitor']
    # 排序方式
    sortable_by = ['date', 'visitor']
    # 展示信息
    list_display = ['id', 'title', 'tag', 'origin', 'date',
                    'recommend', 'commerce', 'top', 'visitor']
    # 链接字段
    list_display_links = ['id', 'title']

    list_filter = ['spiderDate', 'origin']
    # 每页数量
    list_per_page = 50

    list_max_show_all = 50
    # 搜索字段
    search_fields = ['id', 'title', 'content']
    # 日期选择器
    date_hierarchy = 'spiderDate'
