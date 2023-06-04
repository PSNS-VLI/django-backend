from django.db import models
from ckeditor.fields import RichTextField
from topic.models import Topic
from user.models import WeappUser, AnonmyousQQ

# Create your models here.


class Feed(models.Model):

    id = models.AutoField(primary_key=True)
    spider_date = models.DateTimeField("爬取时间", auto_now=True)
    tid = models.CharField("第三方平台ID", null=True, blank=True, max_length=25)
    create_time = models.CharField("发布时间", max_length=20)
    create_timestamp = models.IntegerField("创建时间戳")
    modify_timestamp = models.IntegerField("修改时间戳")
    is_modified = models.BooleanField("是否已修改", default=False)
    content = RichTextField("说说内容")
    convert_content = RichTextField("转换后内容(剔除表情符号)")
    picture_num = models.IntegerField("媒体数量", default=0, null=True, blank=True)
    visitor_num = models.IntegerField("浏览量", default=0, null=True, blank=True)
    like_num = models.IntegerField("点赞量", default=0, null=True, blank=True)
    forward_num = models.IntegerField("转发数", default=0, null=True, blank=True)
    comment_num = models.IntegerField("评论数", default=0, null=True, blank=True)

    is_external = models.BooleanField("来自第三方", default=False, null=True, blank=True)

    fk_topic = models.ManyToManyField(Topic)
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, null=True, blank=True)
    fk_qquser = models.ForeignKey(AnonmyousQQ, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):

        return str(self.id)

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = "博客"


class News(models.Model):

    TAG = (
        ('hot', '热点'),
        ('news', '新闻'),
        ('article', '文章'),
    )

    id = models.IntegerField(primary_key=True)
    date = models.CharField("发布时间", max_length=20)
    title = models.CharField("热点标题", default='', max_length=20)
    content = RichTextField("说说内容")
    visitor = models.IntegerField("浏览量")
    spiderDate = models.DateTimeField("爬取时间", auto_now=True)
    origin = models.CharField("新闻来源", max_length=20, null=True, blank=True)
    cover = models.CharField("封面链接", max_length=200)
    url = models.CharField("原文链接", max_length=200, null=True, blank=True)
    recommend = models.BooleanField("推荐热搜", default=False)
    commerce = models.BooleanField("商业热搜", default=False)
    top = models.BooleanField("置顶热搜", default=False)
    tag = models.CharField("信息类型", default="news", choices=TAG, max_length=10)

    def __str__(self):

        return self.title

    class Meta:
        verbose_name = "学校新闻"
        verbose_name_plural = "学校新闻"

