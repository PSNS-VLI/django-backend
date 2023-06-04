from django.db import models
from ckeditor.fields import RichTextField
from user.models import WeappUser

# Create your models here.


class ArticleTag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField("标签名字", max_length=5)
    num = models.IntegerField("引用次数", default=0)
    date = models.DateTimeField("创建日期", auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"


class Article(models.Model):

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField("发布日期", auto_now=True)
    title = models.CharField("标题", max_length=30)
    content = RichTextField("文章内容")
    preview = models.TextField("文章预览", max_length=60)
    origin = models.TextField("文章来源", max_length=20)
    cover = models.CharField("封面链接", max_length=200)
    visitor = models.IntegerField("浏览数量", default=0)
    like = models.IntegerField("点赞数量", default=0)
    author = models.ForeignKey(WeappUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ArticleTag)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"


class ArticleComment():
    pass
