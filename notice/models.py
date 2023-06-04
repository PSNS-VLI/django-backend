from django.db import models
from ckeditor.fields import RichTextField
from user.models import WeappUser

# Create your models here.


class GlobalNotice(models.Model):

    ORIGIN = (
        ('科大信息', '科大信息'),
        ('科大拼车', '科大拼车')
    )

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    timestamp = models.IntegerField("时间戳")
    title = models.CharField("通知标题", max_length=20)
    content = RichTextField("通知内容")
    origin = models.CharField("通知来源", choices=ORIGIN, max_length=10)
    operator = models.ForeignKey(WeappUser, on_delete=models.CASCADE)
    visitor = models.IntegerField("浏览量", default=0)


    def __str__(self):

        return self.title

    class Meta:

        verbose_name = '全局通知'
        verbose_name_plural = '全局通知'


class PersonalNotice(models.Model):

    ORIGIN = (
        ('科大信息', '科大信息'),
        ('科大拼车', '科大拼车')
    )

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now=True)
    timestamp = models.IntegerField("时间戳")
    title = models.CharField("通知标题", max_length=20)
    content = RichTextField("通知内容")
    origin = models.CharField("通知来源", choices=ORIGIN, max_length=10)
    _to = models.ForeignKey(WeappUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '个人通知'
        verbose_name_plural = '个人通知'