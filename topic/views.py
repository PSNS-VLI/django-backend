from  django.http import JsonResponse, HttpResponseForbidden
from .models import Topic

# Create your views here.


def get_hot_table(request):
    # 函数编码 01
    # 获取热搜榜,默认返回50条
    if request.method == 'POST':
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 50))
        hot_list = []
        try:
            # 加载置顶数据
            top = Topic.objects.filter(top=True)
            if len(top) == 0:
                hot_list = get_hot_data(start, count)
            else:
                for hot in top:
                    data = {
                        "title": hot.name,
                        "visitor": hot.visitor_num,
                        "id": hot.id,
                        "top": hot.top,
                        "recommend": hot.recommend,
                        "commerce": hot.commerce
                    }
                    hot_list.append(data)
                hot_list = hot_list + get_hot_data(start, count)

            return JsonResponse({"status": 0, "data": hot_list})
        except Exception as e:
            # Feed 读库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030101"}})
    else:
        return HttpResponseForbidden()


def get_search_dynamic(request):
    # 函数编码 02
    # 搜索索引,默认返回10条
    if request.method == 'POST':
        entry = request.POST.get('entry', '')
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        try:
            topics = Topic.objects.filter(name__icontains=entry).order_by('-heat', '-create_timestamp')\
                         .all()[start:count]
            data = []
            for t in topics:
                item = {
                    "title": t.name,
                    "id": t.id
                }
                data.append(item)
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # Feed 读库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030201"}})
    else:
        return HttpResponseForbidden()


def get_search_recommend(request):
    # 函数编码 03
    # 获取搜索推荐,默认返回10条
    if request.method == 'POST':
        start = int(request.POST.get('start', 0))
        count = int(request.POST.get('count', 10))
        try:
            topics = Topic.objects.order_by('-heat', '-create_timestamp').all()[start:count]
            data = []
            for t in topics:
                item = {
                    "title": t.name,
                    "id": t.id,
                }
                data.append(item)
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # Feed 读库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "030301"}})
    else:
        return HttpResponseForbidden()


# 从数据库加载热点数据
def get_hot_data(start, count):
    # 从数据库加载热搜榜数据
    data_list = []
    # 获取前按日期排序前50
    hots = Topic.objects.filter(is_main=True).order_by('-create_timestamp', '-visitor_num')[start:count]
    for hot in hots:
        data = {
            "title": hot.name,
            "visitor": hot.visitor_num,
            "id": hot.id,
            "top": hot.top,
            "recommend": hot.recommend,
            "commerce": hot.commerce
        }
        data_list.append(data)

    return data_list
