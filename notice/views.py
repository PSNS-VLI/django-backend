from django.http import JsonResponse, HttpResponseForbidden
from .models import PersonalNotice, GlobalNotice
from user.models import WeappUser

# Create your views here.
# notice 应用编码为 06


# 函数编码 01
def get_notice_list(request):
    if request.method == 'POST':
        # 加载全局通知和本地通知
        try:
            timestamp = request.POST.get("timestamp", 0)
            openid = request.POST.get("openid")
            notice_list = []
            u = WeappUser.objects.get(openid=openid)
            g_l = GlobalNotice.objects.filter(timestamp__gte=timestamp)
            p_l = PersonalNotice.objects.filter(_to=u, timestamp__gte=timestamp)
            if timestamp == 0:
                g_l = g_l[:5]
                p_l = p_l[:5]
            if g_l:
                # 存在全局通知
                for g in g_l:
                    date = str(g.date)
                    notice = {
                        "id": g.id,
                        "title": g.title,
                        "date": f'{date[:10]} {date[11:16]}',
                        "tag": "g"
                    }
                    notice_list.append(notice)
            if p_l:
                # 存在个人通知
                for p in p_l:
                    date = str(p.date)
                    notice = {
                        "id": p.id,
                        "title": p.title,
                        "date": f'{date[:10]} {date[11:16]}',
                        "tag": "p"
                    }
                    notice_list.append(notice)
            return JsonResponse({"status": 0, "data": notice_list})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "060101"}})
    else:
        return HttpResponseForbidden


# 02
def get_notice_num(request):
    if request.method == 'POST':
        # 加载全局通知和本地通知
        try:
            timestamp = request.POST.get("timestamp", 0)
            openid = request.POST.get("openid")
            u = WeappUser.objects.get(openid=openid)
            g_l = GlobalNotice.objects.filter(timestamp__gte=timestamp)
            p_l = PersonalNotice.objects.filter(_to=u, timestamp__gte=timestamp)
            if timestamp == 0:
                g_l = g_l[:5]
                p_l = p_l[:5]
            notice_num = len(g_l) + len(p_l)
            return JsonResponse({"status": 0, "data": notice_num})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "060201"}})
    else:
        return HttpResponseForbidden


# 03
def get_notice(request):
    if request.method == 'POST':
        # 加载全局通知和本地通知
        try:
            _id = request.POST.get("id")
            tag = request.POST.get("tag")
            data = {}
            if tag == 'g':
                # 全局消息
                g = GlobalNotice.objects.get(id=_id)
                date = str(g.date)
                data = {
                    "title": g.title,
                    "content": g.content,
                    "origin": g.origin,
                    "date": f'{date[:10]} {date[11:16]}'
                }
            if tag=='p':
                # 个人消息
                p = PersonalNotice.objects.get(id=_id)
                date = str(p.date)
                data = {
                    "title": p.title,
                    "content": p.content,
                    "origin": p.origin,
                    "date": f'{date[:10]} {date[11:16]}'
                }
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "060301"}})
    else:
        return HttpResponseForbidden
