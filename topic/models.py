from django.db import models
import django.utils.timezone as timezone


class Topic(models.Model):

    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField("创建时间", default=timezone.now)
    create_timestamp = models.IntegerField("创建时间戳")
    update_timestamp = models.IntegerField("更新时间戳")
    name = models.CharField("话题名称", max_length=100, unique=True)
    introduction = models.CharField("导语", default="", max_length=150, null=True, blank=True)
    is_main = models.BooleanField("是否主索引", default=True, null=True, blank=True)
    refer_num = models.IntegerField("引用次数", default=0, null=True, blank=True)
    visitor_num = models.IntegerField("阅读次数", default=0, null=True, blank=True)
    heat = models.IntegerField("热度", default=0, null=True, blank=True)
    recommend = models.BooleanField("推荐热搜", default=False, null=True, blank=True)
    commerce = models.BooleanField("商业热搜", default=False, null=True, blank=True)
    top = models.BooleanField("置顶热搜", default=False, null=True, blank=True)

    def __str__(self):
        return f'%d-%s' % (self.id, self.name)

    class Meta:
        verbose_name = "话题"
        verbose_name_plural = "话题"
