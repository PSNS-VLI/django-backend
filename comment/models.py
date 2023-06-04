from django.db import models
from ckeditor.fields import RichTextField
from user.models import WeappUser, AnonmyousQQ
from article.models import Article
from feed.models import Feed


class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    tid = models.IntegerField("序号(第几条评论)", null=True, blank=True)
    content = RichTextField("评论内容", null=True, blank=True)
    convert_content = RichTextField("转换后内容(剔除表情符号)", null=True, blank=True)
    timestamp = models.IntegerField("时间戳", null=True, blank=True)
    create_time = models.CharField("创建时间", max_length=20, null=True, blank=True)
    is_reply = models.BooleanField("是否评论的回复", default=False, null=True, blank=True)
    reply_num = models.IntegerField("回复数量", default=0, null=True, blank=True)
    picture_num = models.SmallIntegerField("图片数量", default=0, null=True, blank=True)
    like_num = models.IntegerField("点赞数量", default=0, null=True, blank=True)
    to_id = models.IntegerField("回复ID", null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:

        abstract = True


class ArticleComment(Comment):

    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE)
    fk_article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:

        verbose_name = "文章评论"
        verbose_name_plural = "文章评论"


class FeedComment(Comment):

    is_external = models.BooleanField("第三方", default=True, null=True, blank=True)
    fk_qquser = models.ForeignKey(AnonmyousQQ, on_delete=models.CASCADE, null=True, blank=True)
    fk_weappuser = models.ForeignKey(WeappUser, on_delete=models.CASCADE, null=True, blank=True)
    fk_feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:

        verbose_name = "Feed评论"
        verbose_name_plural = "Feed评论"
