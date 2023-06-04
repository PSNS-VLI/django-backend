import json

from django.http import JsonResponse, HttpResponseForbidden
from .models import FeedComment
from feed.models import Feed
from photo.models import FeedCommentPicture
from user.models import AnonmyousQQ, WeappUser
from log.utils import get_like_queryset


# Create your views here.
# comment 应用编码为 07


def get_feed_comment(request):
    # 加载评论信息
    # 函数编码为01
    if request.method == 'POST':
        feed_id = request.POST.get('feed_id', '')
        openid = request.POST.get('openid', '')
        start = request.POST.get('start', 0)
        count = request.POST.get('count', 20)
        if feed_id:
            # 存在id
            try:
                feed = Feed.objects.get(id=feed_id)
                comments = feed.feedcomment_set.prefetch_related('picture', 'fk_qquser', 'fk_weappuser') \
                               .filter(is_reply=False).order_by('tid').all()[int(start):int(count)]
                replys = feed.feedcomment_set.prefetch_related('picture', 'fk_qquser', 'fk_weappuser') \
                    .filter(is_reply=True)
                user_like = get_like_queryset(openid, 'fk_comment_like') if openid else None
                data = []
                for comment in comments:
                    data_item = get_comment_data(comment, user_like_queryset=user_like)
                    if comment.reply_num > 0:
                        reply_list = []
                        replys = replys.filter(to_id=comment.id).order_by('tid').all()
                        for reply in replys:
                            reply_item = get_comment_data(reply)
                            reply_list.append(reply_item)
                        # 评论数量矫正
                        if comment.reply_num != len(replys):
                            comment.reply_num = len(replys)
                            comment.save()
                        data_item['reply_list'] = reply_list

                    data.append(data_item)
                return JsonResponse({"status": 0, "data": data})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def post_feed_comment(request):
    # 加载评论信息
    # 函数编码为01
    if request.method == 'POST':
        openid = request.POST.get('openid', '')
        comment_data = request.POST.get('data', '')
        if openid:
            # 存在openid
            try:
                c_d = json.loads(comment_data)
                fk_user = WeappUser.objects.get(openid=openid)
                fk_feed = Feed.objects.get(id=c_d['feed_id'])
                data= {
                    'tid': c_d['tid'],
                    'content': c_d['content'],
                    'convert_content': c_d['content'],
                    'timestamp': c_d['timestamp'],
                    'create_time': c_d['create_time'],
                    'is_reply': c_d['is_reply'],
                    'to_id': c_d['to_id'],
                    'is_external': False,
                    'fk_weappuser': fk_user,
                    'fk_feed': fk_feed
                }
                if c_d['is_reply']:
                    fk_reply = FeedComment.objects.get(id=c_d['to_id'])
                    fk_reply.reply_num += 1
                    fk_reply.save()
                else:
                    fk_feed.comment_num += 1
                    fk_feed.save()
                f_m = FeedComment.objects.create(**data)
                return JsonResponse({"status": 0, "data": {"id":f_m.id}})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def get_feed_reply(request):
    # 加载回复信息
    # 函数编码为02
    if request.method == 'POST':
        _id = request.POST.get('comment_id', '')
        start = request.POST.get('start', 0)
        count = request.POST.get('count', 10)
        if _id:
            # 存在id
            try:
                data = []
                c_l = FeedComment.objects.filter(to_id=_id, is_reply=True).order_by('tid')[start:count]
                for c in c_l:
                    item = {
                        'id': c.id,
                        'tid': c.tid,
                        'content': c.content,
                        'create_time': c.create_time,
                        'reply_num': c.reply_num,
                        'picture_num': c.picture_num,
                        'like_num': c.like_num
                    }
                    if c.is_external:
                        # 是否来自外部
                        uin = c.fk_user.qq
                        item['userinfo'] = {
                            'name': c.fk_user.name,
                            'uin': uin,
                            'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50'
                        }
                    if c.picture_num > 0:
                        p_l = FeedCommentPicture.objects.filter(fk_comment=c.id)
                        picture_list = []
                        for p in p_l:
                            assert isinstance(p, FeedCommentPicture)
                            picture_data = {
                                'height': p.height,
                                'width': p.width,
                                'url': p.url,
                                'type': p.type
                            }
                            picture_list.append(picture_data)
                        item['images'] = picture_list
                    data.append(item)
                return JsonResponse({"status": 0, "data": data})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def get_comment_data(comment, user_like_queryset=None):
    # 处理comment数据
    data = {
        'id': comment.id,
        'tid': comment.tid,
        'content': comment.content,
        'create_time': comment.create_time,
        'reply_num': comment.reply_num,
        'picture_num': comment.picture_num,
        'images': [{'type': item.type, 'height': item.height, 'height': item.height, 'url': item.url} \
                   for item in comment.picture.all()] if comment.picture_num > 0 else [],
        'like_num': comment.like_num,
        'user_like': False,
        'reply_list': []
    }
    user = None
    if comment.is_external:
        # 来自外部的数据
        user = comment.fk_qquser
        uin = user.qq
        data['user_info'] = {
            'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50',
            'name': user.name,
            'uin': uin
        }
    else:
        user = comment.fk_weappuser
        data['user_info'] = {
            'avatar': user.avatarUrl,
            'name': user.nickName,
            'uin': user.openid
        }

    if user_like_queryset:
        if user_like_queryset.fk_comment_like.filter(object_id=comment.id):
            data['user_like'] = True

    return data


# 爬虫数据处理
def handle_feed_comment(comment_list, fk_feed):
    for comment in comment_list:
        fk_comment = check_feed_comment(comment, fk_feed) # c[0]
        # 评论回复
        if comment['reply_num'] > 0:
            for reply in comment['reply_list']:
                check_feed_comment(reply, fk_feed, fk_comment)


def handle_comment_data(comment, fk_feed, fk_comment=None):
    # 查找用户
    # if comment['is_external']:
    fk_user = AnonmyousQQ.objects.filter(qq=comment['uin'])
    if fk_user:
        fk_user = fk_user[0]
    else:
        # 数据库没有创建
        info = {
            'qq': comment['uin'],
            'name': comment['name'],
            'convert_name': comment['convert_name']
        }
        fk_user = AnonmyousQQ.objects.create(**info)
    comment_data = {
        'tid': comment['tid'],
        'content': comment['content'],
        'convert_content': comment['convert_content'],
        'timestamp': comment['timestamp'],
        'create_time': comment['create_time'],
        'reply_num': comment['reply_num'],
        'picture_num': comment['picture_num'],
        'fk_feed': fk_feed,
        'fk_qquser': fk_user
    }
    if fk_comment:
        comment_data['is_reply'] = True
        comment_data['to_id'] = fk_comment.id

    fk_comment = FeedComment.objects.create(**comment_data)
    # 评论图片
    if comment['picture_num'] > 0:
        i = 1
        for image in comment['images']:
            image_data = {
                'tid': i,
                'width': image['width'],
                'height': image['height'],
                'url': image['url'],
                'is_external': True,
                'fk_feed_comment': fk_comment,
                'fk_qquser': fk_user
            }
            FeedCommentPicture.objects.create(**image_data)
            i += 1
    return fk_comment


def check_feed_comment(comment, fk_feed, fk_comment=None):
    # 检验评论数据是否已经存在
    if fk_comment:
        # 回复评论
        reply = FeedComment.objects.filter(fk_feed=fk_feed, tid=comment['tid'], is_reply=True)
        if reply:
            # 存在数据，取消写库
            return
        else:
            # 不存在数据，进行写库
            handle_comment_data(comment, fk_feed, fk_comment)
    else:
        # 评论
        c = FeedComment.objects.filter(fk_feed=fk_feed, tid=comment['tid'], is_reply=False)
        if c:
            # 存在评论，返回对对象
            reply_num = FeedComment.objects.filter(to_id=comment['tid'], is_reply=True, is_external=True).count()
            c[0].reply_num = comment['reply_num'] + reply_num
            c[0].save()
            return c[0]
        else:
            # 不存在对象，写库
            return handle_comment_data(comment, fk_feed)
