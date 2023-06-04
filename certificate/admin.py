from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    fieldsets = (
        ('证书概览', {
            'fields': ('cer_name', 'cer_recommend_num', 'cer_recommend_score',
                       'cer_host_unit', 'cer_reach', 'cer_tags', 'cer_popularity',
                       'exam_class', 'exam_pass_rate')
        }),
        ('证书简介', {
            'fields': ('cer_introduction',)
        }),
        ('报考详情', {
            'fields': ('apply_time',  'apply_way', 'apply_fee', 'exam_time', 'exam_frequency',
                       'exam_place', 'exam_subjects', 'exam_form', 'exam_question_type',
                       'exam_info_check', 'exam_epidemic_prevention', 'exam_exempt',)
        }),
        ('考试建议', {
            'fields': ('apply_suggest', 'exam_suggest',)
        }),
        ('快速入口', {
            'fields': ('shortcut_info_collect', 'shortcut_official_website', 'shortcut_score_inquiry',)
        }),
        ('相关信息', {
            'fields': ('cer_follow', 'cer_manage', 'recommend_post')
        }),
        ('学习资源', {
            'fields': ('recommend_app', 'recommend_website',)
        }),
        ('其它', {
            'fields': ('scans', 'update_time', 'operator')
        }),
    )

    list_display = [
        'cer_name', 'cer_recommend_num', 'cer_recommend_score',
        'update_time', 'operator', 'create_time', 'scans', 'cer_tags'
    ]

    sortable_by = [
        'create_time', 'update_time', 'scans', 'cer_recommend_score'
    ]

    list_per_page = 20
    list_max_show_all = 20
    list_editable = ['scans', 'cer_tags']
    search_fields = ['cer_name', 'operator']
    date_hierarchy = 'create_time'

    def save_model(self, request, obj, form, change):
        obj.operator_id = request.user
        if change:
            tag = '修改'
        else:
            tag = '新建'
        operator = request.user.username
        cer_name = form.cleaned_data['cer_name']
        log = operator + tag + '了：' + cer_name + '\n'
        with open('log.txt', 'a', encoding='utf-8') as logs:
            logs.write(log)
        super().save_model(request, obj, form, change)