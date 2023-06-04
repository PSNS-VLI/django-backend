import time
import json
from django.http import JsonResponse, HttpResponseForbidden
from feed.models import Feed
from feed.views import get_feed_data
from article.models import Article
from comment.models import FeedComment, ArticleComment
from user.models import WeappUser
from .models import HistoryLog, LikeLog, CommentLikeLog, CollectLog
from django.db.models.query import Prefetch


# Create your views here.


def post_history(request):
    # 提交历史记录
    # 函数编码为01
    if request.method == 'POST':
        # 0 写入 1 删除
        action_list = request.POST.get('action_list', '')
        openid = request.POST.get('openid', '')
        if openid and action_list:
            # 数据上传正确
            action_list = json.loads(action_list)
            try:
                # 获取USER
                fk_user = WeappUser.objects.get(openid=openid)
                for item in action_list:
                    if item['action_type'] == 0:
                        # 写操作
                        # 去重判断
                        h = HistoryLog.objects.filter(object_type=item['object_type'], object_id=item['object_id'])
                        if not h:
                            data = {
                                'create_timestamp': int(time.time()),
                                'object_type': item['object_type'],
                                'object_id': item['object_id'],
                                'fk_weappuser': fk_user,
                            }
                            if item['object_type'] == 0:
                                fk = Feed.objects.get(id=item['object_id'])
                                data['fk_feed'] = fk
                                fk.visitor_num += 1
                                fk.save()
                            elif item.object_type == 1:
                                fk = Article.objects.get(id=item['object_id'])
                                fk.visitor += 1
                                fk.save()
                                data['fk_article'] = fk
                            HistoryLog.objects.create(**data)
                        else:
                            # 更新时间
                            h[0].create_timestamp = int(time.time())
                            h[0].save()
                    else:
                        # 删除操作
                        if item['object_type'] == 0:
                            fk = Feed.objects.get(id=item['object_id'])
                            fk.visitor_num -= 1
                            fk.save()
                        elif item.object_type == 1:
                            fk = Article.objects.get(id=item['object_id'])
                            fk.visitor -= 1
                            fk.save()
                        l = HistoryLog.objects.filter(object_id=item['object_id'])
                        if l:
                            l[0].delete()
                return JsonResponse({"status": 0, "data": "ok"})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def get_history(request):
    # 返回十条历史记录
    # 函数编码为01
    if request.method == 'POST':
        openid = request.POST.get('openid', '')
        object_type = int(request.POST.get('object_type', 0))
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if openid:
            # 数据上传正确
            try:
                # 获取USER
                user = WeappUser.objects.prefetch_related('fk_history').get(openid=openid)
                data = []
                if object_type == 0:
                    # 博客
                    h_l = user.fk_history.prefetch_related(
                        Prefetch('fk_feed', queryset=Feed.objects.prefetch_related('picture', 'fk_weappuser', 'fk_qquser'))
                        ).filter(object_type=object_type).order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h = h.fk_feed
                        h_d = {
                            'id': h.id,
                            'content': h.content[:60],
                            'picture_num': h.picture_num,
                            'images': [{'height': item.height, 'width': item.width, 'type': item.type, 'url': item.url}\
                                       for item in h.picture.all()[:5]] if h.picture_num > 0 else [],
                        }
                        if h.is_external:
                            uin = h.fk_qquser.qq
                            h_d['user_info'] = {
                                'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50',
                                'name': h.fk_qquser.name,
                                'uin': uin
                            }
                        data.append(h_d)
                elif object_type == 1:
                    # 文章
                    h_l = user.fk_history.prefetch_related('fk_article').filter(object_type=object_type)\
                              .order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h = h.fk_article
                        h_d = {
                            'id': h.id,
                            'title': h.title,
                            'preview': h.preview,
                            'cover': h.cover,
                            'origin': h.origin
                        }
                        data.append(h_d)
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


def post_collect(request):
    # 提交收藏
    # 函数编码为01
    if request.method == 'POST':
        # 0 写入 1 删除
        action_list = request.POST.get('action_list', '')
        openid = request.POST.get('openid', '')
        if openid and action_list:
            # 数据上传正确
            action_list = json.loads(action_list)
            try:
                # 获取USER
                fk_user = WeappUser.objects.get(openid=openid)
                for item in action_list:
                    if item['action_type'] == 0:
                        # 写操作
                        data = {
                            'create_timestamp': int(time.time()),
                            'object_type': item['object_type'],
                            'object_id': item['object_id'],
                            'fk_weappuser': fk_user,
                        }
                        if item['object_type'] == 0:
                            fk = Feed.objects.get(id=item['object_id'])
                            data['fk_feed'] = fk
                        elif item.object_type == 1:
                            fk = Article.objects.get(id=item['object_id'])
                            data['fk_article'] = fk
                        CollectLog.objects.create(**data)
                    else:
                        # 删除操作
                        l = CollectLog.objects.filter(object_id=item['object_id'])
                        if l:
                            l[0].delete()
                return JsonResponse({"status": 0, "data": "ok"})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def get_collect(request):
    # 返回十条收藏
    # 函数编码为01
    if request.method == 'POST':
        openid = request.POST.get('openid', '')
        object_type = int(request.POST.get('object_type', 0))
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if openid:
            # 数据上传正确
            try:
                # 获取USER
                user = WeappUser.objects.prefetch_related('fk_history', 'fk_like').get(openid=openid)
                data = []
                if object_type == 0:
                    # 博客
                    h_l = user.fk_collect.prefetch_related(
                        Prefetch('fk_feed', queryset=Feed.objects.prefetch_related('picture', 'fk_weappuser', 'fk_qquser'))
                        ).filter(object_type=object_type).order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h = h.fk_feed
                        data.append(get_feed_data(h, model='part', user_like_queryset=user))
                elif object_type == 1:
                    # 文章
                    h_l = user.fk_collect.prefetch_related('fk_article').filter(object_type=object_type)\
                              .order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h = h.fk_article
                        h_d = {
                            'id': h.id,
                            'title': h.title,
                            'preview': h.preview,
                            'cover': h.cover,
                            'origin': h.origin
                        }
                        data.append(h_d)
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


def post_like(request):
    # 提交历史记录
    # 函数编码为01
    if request.method == 'POST':
        # 0 写入 1 删除
        action_list = request.POST.get('action_list', '')
        openid = request.POST.get('openid', '')
        if openid and action_list:
            # 数据上传正确
            action_list = json.loads(action_list)
            try:
                # 获取USER
                fk_user = WeappUser.objects.get(openid=openid)
                for item in action_list:
                    if item['action_type'] == 0:
                        # 写操作
                        data = {
                            'create_timestamp': int(time.time()),
                            'object_type': item['object_type'],
                            'object_id': item['object_id'],
                            'fk_weappuser': fk_user,
                        }
                        if item['object_type'] == 0:
                            fk = Feed.objects.get(id=item['object_id'])
                            data['fk_feed'] = fk
                            fk.like_num += 1
                            fk.save()
                        elif item.object_type == 1:
                            fk = Article.objects.get(id=item['object_id'])
                            fk.visitor += 1
                            fk.save()
                            data['fk_article'] = fk
                        LikeLog.objects.create(**data)
                    else:
                        # 删除操作
                        if item['object_type'] == 0:
                            fk = Feed.objects.get(id=item['object_id'])
                            fk.like_num -= 1
                            fk.save()
                        elif item.object_type == 1:
                            fk = Article.objects.get(id=item['object_id'])
                            fk.visitor -= 1
                            fk.save()
                        l = LikeLog.objects.filter(object_id=item['object_id'])
                        if l:
                            l[0].delete()
                return JsonResponse({"status": 0, "data": "ok"})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def post_comment_like(request):
    # 提交历史记录
    # 函数编码为01
    if request.method == 'POST':
        # 0 写入 1 删除
        action_list = request.POST.get('action_list', '')
        openid = request.POST.get('openid', '')
        if openid and action_list:
            # 数据上传正确
            action_list = json.loads(action_list)
            try:
                # 获取USER
                fk_user = WeappUser.objects.get(openid=openid)
                print(action_list)
                for item in action_list:
                    if item['action_type'] == 0:
                        # 写操作
                        data = {
                            'create_timestamp': int(time.time()),
                            'object_type': item['object_type'],
                            'object_id': item['object_id'],
                            'fk_weappuser': fk_user,
                        }
                        if item['object_type'] == 0:
                            fk = FeedComment.objects.get(id=item['object_id'])
                            data['fk_feed_comment'] = fk
                            fk.like_num += 1
                            fk.save()
                        elif item.object_type == 1:
                            fk = ArticleComment.objects.get(id=item['object_id'])
                            data['fk_article_comment'] = fk
                        CommentLikeLog.objects.create(**data)
                    else:
                        # 删除操作
                        if item['object_type'] == 0:
                            fk = FeedComment.objects.get(id=item['object_id'])
                            fk.like_num -= 1
                            fk.save()
                        elif item.object_type == 1:
                            fk = ArticleComment.objects.get(id=item['object_id'])
                            fk.like_num -= 1
                            fk.save()
                        l = CommentLikeLog.objects.filter(object_id=item['object_id'])
                        if l:
                            l[0].delete()
                return JsonResponse({"status": 0, "data": "ok"})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030202"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


# 带纠正
def get_like(request):
    # 返回十条历史记录
    # 函数编码为01
    if request.method == 'POST':
        openid = request.POST.get('openid', '')
        object_type = int(request.POST.get('object_type', 0))
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if openid:
            # 数据上传正确
            try:
                # 获取USER
                user = WeappUser.objects.prefetch_related('history').get(openid=openid)
                data = []
                if object_type == 0:
                    # 博客
                    h_l = user.like.prefetch_related('fk_weappuser', 'fk_qquser', 'picture').filter(
                        object_type=object_type).order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h_d = {
                            'id': h.id,
                            'title': h.content[:30],
                            'images': [{'height': item.height, 'width': item.width, 'type': item.type, 'url': item.urll} \
                                       for item in h.picture.all()[:5]] if h.picture_num > 0 else [],
                        }
                        if h.is_external:
                            uin = h.fk_qquser.qq
                            h_d['user_info'] = {
                                'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50',
                                'name': h.fk_qquser.name,
                                'uin': uin
                            }
                        data.append(h_d)
                elif object_type == 1:
                    # 文章
                    pass
                else:
                    pass
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


# 待纠正
def get_comment_like(request):
    # 返回十条历史记录
    # 函数编码为01
    if request.method == 'POST':
        openid = request.POST.get('openid', '')
        object_type = int(request.POST.get('object_type', 0))
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if openid:
            # 数据上传正确
            try:
                # 获取USER
                user = WeappUser.objects.prefetch_related('history').get(openid=openid)
                data = []
                if object_type == 0:
                    # 博客
                    h_l = user.history.prefetch_related('fk_weappuser', 'fk_qquser', 'picture').filter(
                        object_type=object_type).order_by('-create_timestamp').all()[start:count]
                    for h in h_l:
                        h_d = {
                            'id': h.id,
                            'title': h.content[:30],
                            'images': [{'height': item.height, 'width': item.width, 'type': item.type, 'url': item.urll} \
                                       for item in h.picture.all()[:5]] if h.picture_num > 0 else [],
                        }
                        if h.is_external:
                            uin = h.fk_qquser.qq
                            h_d['user_info'] = {
                                'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50',
                                'name': h.fk_qquser.name,
                                'uin': uin
                            }
                        data.append(h_d)
                elif object_type == 1:
                    # 文章
                    pass
                else:
                    pass
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
