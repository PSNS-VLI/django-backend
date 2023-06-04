from django.db import models
from user.models import WeappUser

# Create your models here.


class Carpool(models.Model):

    STATE = (
        ('0', '报名中'),
        ('1', '被申请'),
        ('2', '满员'),
        ('3', '完成拼车'),
        ('4', '已解散')
    )

    MAX = (
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    )

    STATION = (
        ('太原南站', '太原南站'),
        ('太原站', '太原站'),
        ('武宿机场', '武宿机场')
    )

    id = models.AutoField(primary_key=True)
    create_date = models.DateTimeField("创建时间", auto_now=True)
    user_id = models.ForeignKey(WeappUser, on_delete=models.CASCADE)
    openid = models.CharField('openid', max_length=28)
    startDate = models.CharField("发车日期", max_length=8)
    startTime = models.CharField("发车时间", max_length=5)
    timestamp = models.CharField("发车时间戳", max_length=13)
    station = models.CharField("乘车站点", default="太原南站", max_length=5, choices=STATION)
    state = models.CharField("状态码", max_length=1, choices=STATE)
    maxNum = models.SmallIntegerField("最大人数", default=2, choices=MAX)
    currentNum = models.SmallIntegerField("现在人数", default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "拼车队列"
        verbose_name_plural = "拼车队列"


class Apply(models.Model):

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField("创建时间", auto_now=True)
    carpool_id = models.ForeignKey(Carpool, on_delete=models.CASCADE, verbose_name="车队ID")
    user_id = models.ForeignKey(WeappUser, on_delete=models.CASCADE, verbose_name="队员ID")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "报名管理"
        verbose_name_plural = "报名管理"
