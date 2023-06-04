from django.contrib import admin
from .models import WeappUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(WeappUser)
class WeappUserAdmin(UserAdmin):

    list_display = ['username', 'nickName', 'qq', 'mobile', 'school',
                    'academy', 'major', 'grade', 'apartment', 'floor',
                    'dormitoryID', 'studentID', 'openid']

    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (_('Personal info'),
                    {'fields': ('first_name', 'last_name', 'email', 'mobile',
                                'qq', 'nickName', 'school', 'academy',
                                'major', 'grade', 'apartment', 'floor',
                                'dormitoryID', 'studentID', 'permission')})
