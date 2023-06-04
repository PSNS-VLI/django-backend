from django.contrib import admin
from .models import Menu, Banner, Setting

# Register your models here.
admin.site.site_title = 'Ferryman Admin'
admin.site.site_header = 'Ferryman'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    fields = ['index', 'color', 'badge', 'name', 'enable',
              'target', 'login', 'permission']

    ordering = ['index']

    sortable_by = ['index']

    list_display = ['index', 'name', 'permission', 'enable',
                    'target', 'login']

    list_display_links = ['index', 'name']

    search_fields = ['name']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    fields = ['id', 'type', 'url', 'target', 'login']

    readonly_fields = ['id']

    ordering = ['id']

    sortable_by = ['id', 'date']

    list_display = ['id', 'type', 'date', 'login']

    list_display_links = ['id']

    search_fields = ['target']


# setting
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    fields = ['id', 'menuNum', 'bannerNum', 'comment']

    readonly_fields = ['id']

    list_display = ['id', 'menuNum', 'bannerNum','comment', 'update', 'operator']

    list_display_links = ['id']
