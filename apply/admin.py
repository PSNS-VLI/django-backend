from django.contrib import admin
from .models import Apply, Carpool

# Register your models here.


@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):

    fields = ['carpool_id', 'user_id']

    list_display = ['id', 'carpool_id', 'user_id', 'date']

    list_per_page = 50

    list_max_show_all = 50

    date_hierarchy = 'date'


@admin.register(Carpool)
class CarpoolAdmin(admin.ModelAdmin):

    fields = ['state', 'maxNum', 'station', 'startDate', 'startTime']

    # 排序方式
    ordering = ['-create_date', '-state']
    # 排序方式
    sortable_by = ['create_date', 'state']

    list_display_links = ['id', 'station']

    list_display = ['id', 'station', 'state', 'startDate', 'startTime',
                    'create_date']

    list_per_page = 50

    list_max_show_all = 50

    # 搜索字段
    search_fields = ['create_date', 'station', 'state']

    date_hierarchy = 'create_date'

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            self.readonly_fields = []
        else:
            self.readonly_fields = ['state', 'currentNum', 'maxNum', 'station']

        return self.readonly_fields
