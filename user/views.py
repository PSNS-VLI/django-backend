from django.http import JsonResponse, HttpResponseForbidden
from .models import WeappUser
import requests
import json

# Create your views here.
# user 应用编码为 01


def login(request):
    # login 函数编码为 01
    if request.method == 'POST':
        try:
            # 获取wx.login code
            code = request.POST.get('code', '')
            url = 'https://api.weixin.qq.com/sns/jscode2session'
            params = {
                "appid": "wx011ff7e1feff75c6",
                "secret": "78b22eaa0e17b67816fe6e245e602c61",
                "js_code": code,
                "grant_type": "authorization_code"
            }
            r = requests.get(url=url, params=params)
            if r.status_code == 200:
                data = r.json()
                openid = data.get('openid', '')
                # 请求成功
                try:
                    user_info = json.loads(request.POST.get("userInfo", ""))
                    user_info["openid"] = openid
                    # 将用户明暂时设置为openid
                    user_info["username"] = openid
                    u = WeappUser.objects.filter(openid=openid)
                    if u:
                        # 用户存在，更新nickName
                        u = u[0]
                        u.nickName = user_info['nickName']
                        u.save()
                        user_info["gender"] = u.gender
                        user_info["name"] = u.name
                        user_info["SID"] = u.studentID
                        user_info["permission"] = u.permission
                    else:
                        WeappUser.objects.create(**user_info)
                    return JsonResponse({"status": 0, "data": user_info})
                except Exception as e:
                    # 服务器错误 错误编码为 02
                    print(e)
                    return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "010103"}})
            else:
                # 与腾讯服务器连接失败 错误编码为 02
                return JsonResponse({"status": 1, "statusInfo": {"error": "与腾讯服务器连接失败", "errorCode": "010102"}})
        except Exception as e:
            print(e)
            # 前端上传数据不正确 错误编码为 01
            return JsonResponse({"status": 1, "statusInfo": {"error": "code参数错误", "errorCode": "010101"}})
    else:
        return HttpResponseForbidden()
