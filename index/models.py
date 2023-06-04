from django.db import models
from user.models import WeappUser

# Create your models here.


class Menu(models.Model):

    PERMISSION = (
        (0, '访客'),
        (1, '用户'),
        (2, '班级'),
        (3, '学院'),
        (4, '特殊权限'),
        (5, '超管')
    )

    BADGE = (
        (0, '无消息提示'),
        (1, '展示圆点')
    )

    id = models.AutoField(primary_key=True)
    icon = models.CharField("菜单图标", max_length=20)
    index = models.IntegerField("菜单索引")
    color = models.CharField("菜单颜色", max_length=10)
    badge = models.IntegerField("消息图标", default=0, choices=BADGE)
    name = models.CharField("菜单名称", max_length=10)
    enable = models.BooleanField("是否启用", default=False)
    target = models.CharField("目标页面", max_length=25)
    login = models.BooleanField("需要登录", default=True)
    permission = models.IntegerField("最低权限", default=0, choices=PERMISSION)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "首页菜单"
        verbose_name_plural = "首页菜单"


class Banner(models.Model):

    TYPE = (
        ('image', '图片'),
        ('media', '视频')
    )

    id = models.AutoField(primary_key=True)
    type = models.CharField("媒体类型", default='image', max_length=6)
    url = models.CharField("媒体地址", max_length=200)
    target = models.CharField("目标页面", max_length=50, null=True)
    login = models.BooleanField("需要登录", default=False)
    date = models.DateTimeField("创建日期", auto_now=True, null=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "首页轮播"
        verbose_name_plural = "首页轮播"


class Setting(models.Model):

    id = models.AutoField(primary_key=True)
    menuNum = models.IntegerField("菜单数量", default=8, unique=True)
    bannerNum = models.IntegerField("轮播数量", default=4, unique=True)
    comment = models.BooleanField("开启评论", default=False, unique=True)
    operator = models.OneToOneField(WeappUser, on_delete=models.CASCADE)
    update = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '菜单数量：%d，轮播数量：%d' % (self.menuNum, self.bannerNum)

    class Meta:
        verbose_name = "设置信息"
        verbose_name_plural = "设置信息"
