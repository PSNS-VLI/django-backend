from django.db import models
from user.models import WeappUser

# Create your models here.


class Certificates(models.Model):
    TAGS = (
        ('通用类', '通用类'),
        ('工业工程', '工业工程'),
        ('会计学', '会计学'),
        ('经济学', '经济学'),
        ('信息管理与信息系统', '信息管理与信息系统'),
    )

    OPERATOR = (
        ('于宏亮', '于宏亮'),
        ('巩亚轩', '巩亚轩'),
        ('权怡凝', '权怡凝'),
        ('杨柠柽', '杨柠柽'),
        ('马冲', '马冲'),
    )

    id = models.AutoField(primary_key=True, verbose_name='ID')
    operator_id = models.ForeignKey(WeappUser,on_delete=models.CASCADE, verbose_name='外键-用户')
    cer_name = models.CharField(max_length=50, verbose_name='证书名称', help_text='至多50字符')
    cer_recommend_num = models.BigIntegerField(verbose_name='打分人数', help_text='初始化0人')
    cer_recommend_score = models.FloatField(verbose_name='推荐指数', help_text='初始化10分' )
    cer_popularity = models.CharField(max_length=50, verbose_name='热门程度', null=True, blank=True,
                                      help_text='反应近年报考热门程度')
    cer_host_unit = models.CharField(max_length=50, verbose_name='主办(认证)单位')
    cer_reach = models.CharField(max_length=10, verbose_name='作用范围')
    cer_introduction = models.CharField(max_length=200, verbose_name='证书简介')
    cer_tags = models.CharField(max_length=50, verbose_name='证书分类标签', default='通用类', choices=TAGS)
    cer_follow = models.CharField(max_length=200, verbose_name='证书后续', null=True, blank=True)
    cer_manage = models.CharField(max_length=200, verbose_name='证书管理', null=True, blank=True)
    #考试类别
    #证书类别
    #通过率
    #免试申请与审核(可选)
    apply_fee = models.FloatField(verbose_name='报名费用', help_text='eg(99.0),加一位小数', default=0.00)
    apply_condition = models.CharField(max_length=200, verbose_name='报名条件')
    apply_time = models.CharField(max_length=50, verbose_name='报名时间')
    apply_way = models.CharField(max_length=200, verbose_name='报名方式')
    apply_suggest = models.CharField(max_length=200, verbose_name='报考建议', null=True, blank=True, )
    exam_suggest = models.CharField(max_length=200, verbose_name='参考建议', null=True, blank=True)
    exam_exempt = models.CharField(max_length=200, verbose_name='免试申请与审核', null=True, blank=True)
    exam_pass_rate = models.FloatField(verbose_name='通过率', null=True, blank=True)
    exam_class = models.CharField(max_length=50, verbose_name='考试类别', null=True, blank=True)
    exam_time = models.CharField(max_length=50, verbose_name='考试时间')
    exam_frequency = models.CharField(max_length=200, verbose_name='考试频率')
    exam_place = models.CharField(max_length=100, verbose_name='考试地点')
    exam_subjects = models.CharField(max_length=200, verbose_name='考试科目以及时长',
                                     help_text="'【】'表头,' / '分隔列,' ; '分隔行")
    exam_form = models.CharField(max_length=50, verbose_name='考试形式')
    exam_question_type = models.CharField(max_length=1024, verbose_name='考试题型')#表格
    exam_info_check = models.CharField(max_length=200, verbose_name='必备证件', null=True, blank=True)
    exam_epidemic_prevention = models.CharField(max_length=100, verbose_name='防疫要求', null=True, blank=True)
    #考试建议[报考建议(可选)、参考建议（可选）)]
    #相关信息[证书后续、证书管理]
    shortcut_info_collect = models.CharField(max_length=50, verbose_name='信息采集', null=True, blank=True)
    shortcut_official_website = models.CharField(max_length=50, verbose_name='报名官网', null=True, blank=True)
    shortcut_score_inquiry = models.CharField(max_length=50, verbose_name='成绩查询网址', null=True, blank=True)
    recommend_app = models.CharField(max_length=100, verbose_name='推荐软件', null=True, blank=True)
    recommend_website = models.CharField(max_length=100, verbose_name='推荐网课', null=True, blank=True)
    recommend_post = models.CharField(max_length=50, verbose_name='推荐职位', null=True, blank=True)
    #推荐教材
    #对应岗位职业
    scans = models.BigIntegerField(verbose_name='浏览数')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
    operator = models.CharField(max_length=50, verbose_name='操作员', choices=OPERATOR)

    def __str__(self):
        return self.cer_name

    class Meta:
        verbose_name = '证书信息'
        verbose_name_plural = '证书信息'
