from django.db import models
from feed.models import Feed
from comment.models import FeedComment, ArticleComment
from user.models import WeappUser, AnonmyousQQ

# Create your models here.


class Picture(models.Model):

    TYPE = (
        ("图片", 0),
        ("视频", 1)
    )

    id = models.AutoField(primary_key=True)
    tid = models.SmallIntegerField("图片顺序", default=1, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now=True)
    height = models.SmallIntegerField("高度", blank=True, null=True)
    width = models.SmallIntegerField("宽度", blank=True, null=True)
    type = models.SmallIntegerField("类型", default=0, choices=TYPE, null=True, blank=True)
    url = models.CharField("图片地址", max_length=200)
    is_external = models.BooleanField("来自外部", default=False, null=True, blank=True)
    fk_qquser = models.ForeignKey(AnonmyousQQ, on_delete=models.CASCADE, null=True, blank=True)
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class FeedCommentPicture(Picture):

    fk_feed_comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE, related_name='picture')

    class Meta:

        verbose_name = 'Feed评论图片'
        verbose_name_plural = 'Feed评论图片'


class ArticleCommentPicture(Picture):

    fk_article_comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Article评论图片'
        verbose_name_plural = 'Article评论图片'


class FeedPicture(Picture):

    fk_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='picture')

    class Meta:

        verbose_name = 'Feed图片'
        verbose_name_plural = 'Feed图片'
