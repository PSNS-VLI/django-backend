from django.db import models
from user.models import WeappUser
from feed.models import Feed
from article.models import Article
from comment.models import ArticleComment, FeedComment
import django.utils.timezone as timezone


# Create your models here.


class Log(models.Model):
    CONTENT_TYPE = (
        # ('博客', 'blog'),
        # ('文章', 'article'),
        # ('视频', 'video'),
        ('博客', 0),
        ('文章', 1),
        ('视频', 2),
        ('评论', 3)
    )

    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField("创建时间", default=timezone.now)
    create_timestamp = models.CharField("创建时间戳", max_length=10)
    object_type = models.SmallIntegerField("行为对象类型", choices=CONTENT_TYPE, null=True, blank=True)
    object_id = models.IntegerField("行为对象ID", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class ActionLog(Log):
    TYPE = (
        # ('浏览', 'view'),
        # ('点赞', 'like'),
        # ('转发', 'forward'),
        # ('评论', 'comment'),
        # ('收藏', 'collect'),
        # ('跟随', 'follow'),
        # ('发布', 'publish'),
        ('浏览', 0),
        ('点赞', 1),
        ('转发', 2),
        ('评论', 3),
        ('收藏', 4),
        ('跟随', 5),
        ('发布', 6)
    )

    action_type = models.SmallIntegerField("行为类型", choices=TYPE, null=True, blank=True)
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "行为日志"
        verbose_name_plural = "行为日志"


class HistoryLog(Log):
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, related_name='fk_history')
    fk_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    fk_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "浏览历史"
        verbose_name_plural = "浏览历史"


class CollectLog(Log):
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, related_name='fk_collect')
    fk_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='fk_collect', null=True, blank=True)
    fk_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='fk_collect', null=True, blank=True)

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = "收藏"


class LikeLog(Log):
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, related_name='fk_like')
    fk_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='fk_like', null=True, blank=True)
    fk_article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='fk_like', null=True, blank=True)

    class Meta:
        verbose_name = "文章点赞"
        verbose_name_plural = "文章点赞"


class CommentLikeLog(Log):

    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, related_name='fk_comment_like')
    fk_feed_comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE, related_name='fk_comment_like', null=True, blank=True)
    fk_article_comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='fk_comment_like', null=True, blank=True)

    class Meta:
        verbose_name = "评论点赞"
        verbose_name_plural = "评论点赞"
