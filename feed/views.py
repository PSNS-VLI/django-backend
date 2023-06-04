import json
import time
from django.http import JsonResponse, HttpResponseForbidden
from .models import Feed, News
from user.models import AnonmyousQQ
from photo.models import FeedCommentPicture, FeedPicture
from comment.models import FeedComment
from topic.models import Topic
from comment.views import handle_feed_comment
from log.utils import get_like_queryset


# Create your views here.
# feed 应用编码为 03


# 上传新闻 04
def post_news(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', ' '))
        password = request.POST.get('password', ' ')
        if password == 'yhl@521' and data:
            try:
                # 从数据包中解析数据
                data = data['data']
                for item in data:
                    _id = item['id']
                    hot = News.objects.filter(id=_id)
                    if len(hot) != 0:
                        # 新闻为同一天发布
                        hot[0].visitor = item['visitor']
                        hot[0].save()
                    else:
                        hot_data = {
                            'id': _id,
                            'date': item['date'],
                            'cover': item['cover'],
                            'content': item['content'],
                            'title': item['title'],
                            'visitor': item['visitor'],
                            'origin': item['origin'],
                            'url': item['url']
                        }
                        News.objects.create(**hot_data)
                return JsonResponse({"status": 0})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030402"}})
        else:
            # 密码错误 01
            return JsonResponse({"status": 0, "statusInfo": {"error": "参数错误", "errorCode": "030401"}})
    else:
        return HttpResponseForbidden()


# 获取新闻榜 05
def get_news_table(request):
    if request.method == 'POST':
        start = request.POST.get('start', ' ')
        count = request.POST.get('count', ' ')
        hot_list = []
        try:
            # 去数据库检索数据
            top = News.objects.filter(top=True)
            if len(top) == 0:
                hot_list = get_news_data(30)
            else:
                for hot in top:
                    data = {
                        "title": hot.title,
                        "visitor": hot.visitor,
                        "id": hot.id,
                        "tag": hot.tag,
                        "top": hot.top,
                        "recommend": hot.recommend,
                        "commerce": hot.commerce
                    }
                    hot_list.append(data)
                hot_list = hot_list + get_news_data(30-len(top))

            return JsonResponse({"status": 0, "data": hot_list})
        except Exception as e:
            # Feed 读库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030501"}})
    else:
        return HttpResponseForbidden()


# 获取新闻 06
def get_news(request):
    if request.method == 'POST':
        _id = request.POST.get('id', ' ')
        if _id:
            # 存在id
            try:
                hot = News.objects.get(id=_id)
                assert isinstance(hot, News)
                data = {
                    "id": hot.id,
                    "date": hot.date,
                    "title": hot.title,
                    "content": hot.content,
                    "cover": hot.cover,
                    "visitor": hot.visitor,
                    "origin": hot.origin,
                    "recommend": hot.recommend,
                    "commerce": hot.commerce,
                    "top": hot.top,
                    "tag": hot.tag
                }
                return JsonResponse({"status": 0, "data": data})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030602"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030601"}})
    else:
        return HttpResponseForbidden()


# 从数据库加载新闻数据
def get_news_data(count):
    # 从数据库加载热搜榜数据
    data_list = []
    # 获取前按日期排序前50
    hots = News.objects.order_by('-id').all()[:count]
    for hot in hots:
        data = {
            "title": hot.title,
            "visitor": hot.visitor,
            "id": hot.id,
            "tag": hot.tag,
            "top": hot.top,
            "recommend": hot.recommend,
            "commerce": hot.commerce
        }
        data_list.append(data)

    return data_list


def get_feed_table(request):
    if request.method == 'POST':
        topic_id = request.POST.get('id', '')
        openid = request.POST.get('openid', '')
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if topic_id:
            # 存在 topic_id
            try:
                # 根据 topic_id 检索 topic 检索 feed
                topic = Topic.objects.get(id=topic_id)
                feeds = topic.feed_set.order_by('-create_time')[start: count]
                user_like = get_like_queryset(openid, 'fk_like', 'fk_collect') if openid else None
                data = []
                for feed in feeds:
                    data.append(get_feed_data(feed, model='part', user_like_queryset=user_like))
                return JsonResponse({"status": 0, "data": data})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030602"}})
        else:
            # 参数错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030601"}})
    else:
        return HttpResponseForbidden()


def get_feed(request):
    # 加载feed详细信息
    # 函数编码 02
    if request.method == 'POST':
        _id = request.POST.get('id', '')
        openid = request.POST.get('openid', '')
        if _id:
            # 存在id
            try:
                feed = Feed.objects.prefetch_related('fk_topic').get(id=_id)
                user_like = get_like_queryset(openid, 'fk_like', 'fk_collect') if openid else None
                data = get_feed_data(feed, model='full', user_like_queryset=user_like)
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


def search_feed(request):
    # 加载feed详细信息
    # 函数编码 02
    if request.method == 'POST':
        entry = request.POST.get('entry', '')
        openid = request.POST.get('openid', '')
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        if entry:
            # 存在entry
            try:
                feeds = Feed.objects.prefetch_related('fk_topic').filter(content__icontains=entry)\
                    .order_by('-create_timestamp')[start:count]
                user_like = get_like_queryset(openid, 'fk_like', 'fk_comment_like') if openid else None
                data = []
                for feed in feeds:
                    data.append(get_feed_data(feed, model='part', user_like_queryset=user_like))
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


def post_feed(request):
    # 函数编码 03
    if request.method == 'POST':
        feed_list = json.loads(request.POST.get('data', ''))
        password = request.POST.get('password', '')
        host_uin = request.POST.get('uin','')
        if password == '***' and feed_list:
            try:
                # 链接到对应表白墙的qq号码
                # 临时存储信息，避免频繁查库
                temp_pool = {}
                # 查询host
                host = AnonmyousQQ.objects.filter(qq=host_uin)
                if host:
                    temp_pool[int(host_uin)] = host[0]
                # 从数据包中解析数据
                for feed in feed_list:
                    f = Feed.objects.prefetch_related('fk_topic').filter(tid=feed['tid'])
                    if f:
                        # 存在数据更新 评论和浏览数量
                        f = f[0]
                        f.visitor_num = feed['visitor_num']
                        # 更新对应话题
                        if f.fk_topic:
                            for topic in f.fk_topic.all():
                                topic.visitor_num = feed['visitor_num']
                                topic.save()
                        # 筛选评论
                        if feed['comment_num'] > 0:
                            handle_feed_comment(feed['comment_list'], f)
                        feed['comment_num'] = FeedComment.objects.filter(fk_feed=f, is_reply=False).count()
                        f.save()
                    else:
                        # 不存在 新建数据
                        fk_user = None
                        if temp_pool.get(int(feed['uin']), ''):
                            # 存在host
                            fk_user = temp_pool[int(feed['uin'])]
                        else:
                            # 不存在创建一个
                            info = {
                                'qq': feed['uin'],
                                'name': feed['name'],
                                'convert_name': feed['name']
                            }
                            fk_user = AnonmyousQQ.objects.create(**info)
                            temp_pool[int(feed['uin'])] = fk_user
                        # 向数据库写入FEED
                        feed_data = {
                            'tid': feed['tid'],
                            'create_time': feed['create_time'],
                            'create_timestamp': feed['create_timestamp'],
                            'modify_timestamp': feed['modify_timestamp'],
                            'is_modified': feed['is_modified'],
                            'content': feed['content'],
                            'convert_content': feed['convert_content'],
                            'picture_num': feed['picture_num'],
                            'visitor_num': feed['visitor_num'],
                            'comment_num': feed['comment_num'],
                            'is_external': True,
                            'fk_qquser': fk_user
                        }
                        fk_feed = Feed.objects.create(**feed_data)
                        # 保存话题
                        if feed.get('topic', '') and len(feed['topic']) > 0:
                            fk_topic_list = []
                            for topic in feed['topic']:
                                if len(topic['title']) > 0:
                                    # 先向数据库查询话题
                                    t = Topic.objects.filter(name=topic['title'])
                                    if t:
                                        # 存在话题
                                        t = t[0]
                                        t.refer_num += 1
                                        t.heat += 100
                                        t.visitor_num += int(feed['visitor_num'])
                                        t.is_main = topic['main']
                                        t.save()
                                        fk_topic_list.append(t)
                                    else:
                                        # 不存在话题
                                        topic_data = {
                                            'create_time': time.strftime('%Y-%m-%d %H:%M:%S',
                                                                         time.localtime(feed['create_timestamp'])),
                                            'create_timestamp': feed['create_timestamp'],
                                            'update_timestamp': feed['modify_timestamp'],
                                            'name': topic['title'],
                                            'is_main': topic['main'],
                                            'refer_num': 1,
                                            'visitor_num': int(feed['visitor_num']),
                                            'heat': 100
                                        }
                                        t = Topic.objects.create(**topic_data)
                                        fk_topic_list.append(t)
                                else:
                                    t = Topic.objects.filter(name='大家怎么看')
                                    if t:
                                        fk_topic_list.append(t[0])
                            fk_feed.fk_topic.set(fk_topic_list)
                        # 保存图片
                        if feed['picture_num'] > 0:
                            i = 1
                            for image in feed['images']:
                                image_data = {
                                    'tid': i,
                                    'width': image['width'],
                                    'height': image['height'],
                                    'url': image['url'],
                                    'is_external': True,
                                    'fk_feed': fk_feed,
                                    'fk_qquser': fk_user
                                }
                                FeedPicture.objects.create(**image_data)
                                i += 1
                        # 保存评论
                        if feed['comment_num'] > 0:
                            handle_feed_comment(feed['comment_list'], fk_feed)
                return JsonResponse({"status": 0})
            except Exception as e:
                # 服务器异常 02
                print(e)
                return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030302"}})
        else:
            # 密码错误 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "参数错误", "errorCode": "030301"}})
    else:
        return HttpResponseForbidden()


def get_feed_data(feed, model='full', user_like_queryset=None):
    # 加载 feed 数据
    assert isinstance(feed, Feed)
    data = {
        'id': feed.id,
        'create_time': feed.create_time,
        'create_timestamp': feed.create_timestamp,
        'modify_timestamp': feed.modify_timestamp,
        'is_modified': feed.is_modified,
        'content': feed.content,
        'picture_num': feed.picture_num,
        'visitor_num': feed.visitor_num,
        'like_num': feed.like_num,
        'comment_num': feed.comment_num,
        'topic_list': [{'id': topic.id, 'name': topic.name} for topic in feed.fk_topic.all()],
        'user_like': False,
        'user_collect': False
    }
    # 加载话题
    # topics = Feed.objects.prefetch_related('fk_topic').all()
    # if topics:
    #     topic_list = []
    #     for topic in topics:
    #         topic_data = {
    #             'id': topic.id,
    #             'name': topic.name
    #         }
    #         topic_list.append(topic_data)
    #     data['topic_list'] = topic_list
    if feed.is_external:
        uin = feed.fk_qquser.qq
        data['user_info'] = {
            'name': feed.fk_qquser.name,
            'uin': uin,
            'avatar': f'http://qlogo1.store.qq.com/qzone/{uin}/{uin}/50'
        }
    if feed.picture_num > 0:
        p_l = []
        if model == 'part':
            # 加载不超过9张图片
            p_l = FeedPicture.objects.filter(fk_feed=feed).order_by('tid')[:9]
        else:
            # 加载全部
            p_l = FeedPicture.objects.filter(fk_feed=feed).order_by('tid')
        picture_list = []
        for p in p_l:
            assert isinstance(p, FeedPicture)
            picture_data = {
                'height': p.height,
                'width': p.width,
                'url': p.url,
                'type': p.type
            }
            picture_list.append(picture_data)
        data['images'] = picture_list
    if user_like_queryset:
        if user_like_queryset.fk_like.filter(object_id=feed.id):
            data['user_like'] = True
        if user_like_queryset.fk_collect.filter(object_id=feed.id):
            data['user_collect'] = True
    return data
