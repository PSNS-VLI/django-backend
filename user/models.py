from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.


class WeappUser(AbstractUser):

    openid = models.CharField('openid', max_length=28, unique=True)
    unionid = models.CharField('unionid', max_length=29, null=True, blank=True)
    permission = models.IntegerField('权限', default=0)
    nickName = models.CharField('微信昵称', max_length=100, null=True, blank=True)
    name = models.CharField('姓名', default='',  max_length=50, null=True, blank=True)
    gender = models.SmallIntegerField('性别', default=0, null=True, blank=True)
    avatarUrl = models.CharField('微信头像', max_length=150, null=True, blank=True)
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    qq = models.CharField('QQ号', max_length=16, null=True, blank=True)
    school = models.CharField('学校', max_length=20, null=True, blank=True)
    academy = models.CharField('学院', max_length=20, null=True, blank=True)
    major = models.CharField('专业', max_length=20, null=True, blank=True)
    grade = models.CharField('班级', max_length=10, null=True, blank=True)
    apartment = models.CharField('宿舍楼', max_length=5, null=True, blank=True)
    floor = models.CharField('楼层', max_length=2, null=True, blank=True)
    dormitoryID = models.CharField('宿舍号', max_length=5, null=True, blank=True)
    studentID = models.CharField('学号', max_length=12, null=True, blank=True)

    def __str__(self):
        return '%s-%s-%s-%s' % (self.academy, self.major, self.grade, self.username)

    class Meta:
        verbose_name = "微信用户"
        verbose_name_plural = "微信用户"


class AnonmyousQQ(models.Model):

    id = models.AutoField(primary_key=True)
    qq = models.IntegerField('QQ号')
    name = models.CharField('QQ昵称', max_length=100, null=True, blank=True)
    convert_name = RichTextField('格式化昵称', null=True, blank=True)

    def __str__(self):
        return str(self.qq)

    class Meta:
        verbose_name = "QQ用户"
        verbose_name_plural = "QQ用户"
