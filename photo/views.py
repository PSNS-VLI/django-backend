from django.http import JsonResponse, HttpResponseForbidden
from feed.models import Feed

# Create your views here.


def get_feed_picture(request):
    # 函数编码 01
    # 获取热搜榜,默认返回20条
    if request.method == 'POST':
        feed_id = request.POST.get('id', '')
        start = request.POST.get('start', 0)
        count = request.POST.get('count', 9)
        try:
            feed = Feed.objects.prefetch_related('picture').get(id=feed_id)
            data = [
                {'type': item.type, 'height': item.height, 'width': item.width, 'url': item.url} \
                for item in feed.picture.order_by('tid').all()[int(start):int(count)]
            ]
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # Feed 读库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030101"}})
    else:
        return HttpResponseForbidden()