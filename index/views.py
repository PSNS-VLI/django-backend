from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from .models import Menu, Banner, Setting


# Create your views here.
# index应用编码为 02


def init_setting(request):
    # init_setting 函数编码为 01
    # 加载banner与menu
    if request.method == 'POST':
        # 从Setting加载配置信息
        try:
            setting = Setting.objects.all()[0]
            menus = Menu.objects.order_by('index').all()[:setting.menuNum]
            banners = Banner.objects.all()[:setting.bannerNum]
            menu_list = []
            banner_list = []
            for menu in menus:
                data = {
                    "icon": menu.icon,
                    "index": menu.index,
                    "color": menu.color,
                    "badge": menu.badge,
                    "name": menu.name,
                    "enable": menu.enable,
                    "target": menu.target,
                    "login": menu.login,
                    "permission": menu.permission
                }
                menu_list.append(data)

            for banner in banners:
                data = {
                    "id": banner.id,
                    "type": banner.type,
                    "url": banner.url,
                    "target": banner.target
                }
                banner_list.append(data)

            data = {"menuList": menu_list, "bannerList": banner_list, "comment": setting.comment}
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            print(e)
            # 读写数据异常 错误码 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "020101"}})
    else:
        return HttpResponseForbidden()


def pag_not_found(request, exception):
    return render(request, 'index_erp.html', status=200)
