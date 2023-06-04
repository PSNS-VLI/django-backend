from django.contrib import admin
from .models import Article, ArticleTag

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 可以修改的字段
    fields = ['id', 'title', 'content', 'preview' ,'cover',
              'tags', 'origin', 'author', 'visitor', 'like']
    # 排序方式
    ordering = ['-date', '-visitor']
    # 排序方式
    sortable_by = ['date', 'visitor']
    # 展示信息
    list_display = ['id', 'title', 'visitor', 'like', 'date']
    # 链接字段
    list_display_links = ['id', 'title']

    list_filter = ['date']
    # 每页数量
    list_per_page = 20

    list_max_show_all = 50
    # 搜索字段
    search_fields = ['id', 'title', 'author']
    # 日期选择器
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            self.readonly_fields = ['id']
        else:
            self.readonly_fields = ['id', 'visitor', 'like'
                                    'author']

        return self.readonly_fields


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):

    # 可以修改的字段
    fields = ['id', 'name','num']
    readonly_fields = ['id', 'num']
    # 排序方式
    ordering = ['-date', '-num']
    # 排序方式
    sortable_by = ['date', 'num']
    # 展示信息
    list_display = ['id', 'name', 'num']
    # 链接字段
    list_display_links = ['id', 'name']

    list_filter = ['date']
    # 每页数量
    list_per_page = 20

    list_max_show_all = 50
    # 搜索字段
    search_fields = ['id', 'name']
    # 日期选择器
    date_hierarchy = 'date'
