from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
import json
from .models import Carpool, Apply
from user.models import WeappUser
from .task import create_email, delete_email,  join_email, quit_email


# Create your views here.
# apply 应用编码为 04


# 创建车队 01
def create_carpool(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data'))
            openid = data.get('openid')
            user = WeappUser.objects.get(openid=openid)
            print(data['gender'])
            if not user.studentID:
                # 数据库不存在数据
                user.studentID = data['SID']
                user.name = data['name']
                user.qq = data['qq']
                user.email = f"{data['qq']}@qq.com"
                user.gender = data['gender']
                user.save()
            # 查找state=2
            carpool = Carpool.objects.filter(user_id=user, state__lte=2)
            if not carpool:
                carpool_data = {
                    "user_id": user,
                    "startDate": data['startDate'],
                    "startTime": data['startTime'],
                    "timestamp": data['timestamp'],
                    "state": data['state'],
                    "maxNum": data['maxNum'],
                    "station": data['station'],
                    "openid": data['openid']
                }
                c = Carpool.objects.create(**carpool_data)
                create_email.delay('车队创建成功！',openid, json.dumps(data, ensure_ascii=False))
                return JsonResponse({"status": 0, "data": c.id})
            else:
                # 已经拥有车队 02
                return JsonResponse({"status": 1, "statusInfo": {"error": "已有车队", "errorCode": "040102"}})
        except Exception as e:
            # 服务器读写数据库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040101"}})
    else:
        return HttpResponseForbidden()


# 删除车队 02
def delete_carpool(request):
    if request.method == 'POST':
        try:
            # 获取目标车队的ID和申请者ID
            carpool_id = request.POST.get('carpool_id')
            openid = request.POST.get('openid')
            c = Carpool.objects.get(id=carpool_id)
            if int(c.state) < 2 and c.openid == openid:
                # 获取队员列表
                a_l = Apply.objects.filter(carpool_id=c)
                mates = []
                if a_l:
                    for a in a_l:
                        mates.append(a.user_id.openid)
                c.delete()
                # 发送消息
                delete_email.delay(openid, ','.join(mates))
                return JsonResponse({"status": 0})
            else:
                # 操作五权限或车队满员 02
                return JsonResponse({"status": 1, "statusInfo": {"error": "车队已有成员", "errorCode": "040202"}})
        except Exception as e:
            # 读写数据库异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040201"}})

    else:
        return HttpResponseForbidden()


# 加入车队 03
def join_carpool(request):
    if request.method == 'POST':
        try:
            # 获取目标车队的ID和申请者ID
            carpool_id = request.POST.get('carpool_id')
            openid = request.POST.get('openid')
            # 获取申请者team信息
            has_team = request.POST.get('hasTeam')
            c = Carpool.objects.get(id=carpool_id)
            if int(c.state) < 2:
                # 目标车队状态正常
                # 获取申请人信息
                u = WeappUser.objects.get(openid=openid)
                # 判断申请人是否拥有team
                if has_team == 'true':
                    # 申请人有队伍
                    # 获取申请人队伍
                    _c = Carpool.objects.get(user_id=u)
                    # 保存状态暂时设置队伍解散
                    state = _c.state
                    _c.state = '4'
                    _c.save()
                    if _c.currentNum + c.currentNum <= c.maxNum:
                        # 符合目标人数要求
                        # 数据库事务，设置目标车队人数减少
                        current = c.currentNum
                        c.currentNum = _c.currentNum + c.currentNum
                        c.save()
                        try:
                            # 将数据库该队伍队员转移
                            a_l = Apply.objects.filter(carpool_id=_c)
                            for a in a_l:
                                a.carpool_id = c
                                a.save()
                            # 将申请人加入目标队伍
                            Apply.objects.create(carpool_id=c, user_id=u)
                            # 判断总人数是否达到最大
                            if c.currentNum == c.maxNum:
                                c.state = '2'
                                c.save()
                            # 删除申请人创建的队伍
                            _c.delete()
                            # 异步发送消息
                            join_email.delay("您有新的成员加入！", carpool_id, openid)
                            return JsonResponse({"status": 0})
                        except Exception as e:
                            # 发生异常数据库回滚 06
                            c.currentNum = current
                            c.save()
                            _c.state = state
                            _c.save()
                            print(e)
                            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040306"}})
                    else:
                        # 人数超过要求 05
                        _c.state = state
                        _c.save()
                        return JsonResponse({"status": 1, "statusInfo": {"error": "人数超过要求", "errorCode": "040305"}})
                else:
                    # 申请人无队伍,加入队伍
                    current = c.currentNum
                    # 数据库事务
                    c.currentNum = c.currentNum+1
                    c.save()
                    try:
                        Apply.objects.create(carpool_id=c, user_id=u)
                        # 修改数据库对应状态
                        if c.currentNum == c.maxNum:
                            c.state = '2'
                            c.save()
                        # 创建成功
                        # 异步发送邮件
                        join_email.delay("您有新的成员加入！", carpool_id, openid)
                        return JsonResponse({"status": 0})
                    except Exception as e:
                        # 数据回滚 04
                        c.currentNum = current
                        c.save()
                        print(e)
                        return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040304"}})
            else:
                # 对方队伍满员 03
                return JsonResponse({"status": 1, "statusInfo": {"error": "目标车队已满", "errorCode": "040303"}})
        except Carpool.DoesNotExist as e:
            # 目标车队被删除 02
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "目标车队已解散", "errorCode": "040302"}})
        except Exception as e:
            # 服务器异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040301"}})
    else:
        return HttpResponseForbidden()


# 退出车队 04
def quit_carpool(request):
    if request.method == 'POST':
        # 获取退出人openid
        dropout = request.POST.get('dropout')
        operator = request.POST.get('openid')
        carpool_id = request.POST.get('carpool_id')
        try:
            c = Carpool.objects.get(id=carpool_id)
            u = WeappUser.objects.get(openid=dropout)
            c.currentNum = c.currentNum - 1
            a = Apply.objects.filter(user_id=u, carpool_id=c)
            if a:
                a.delete()
                if c.state == '2':
                    c.state = '1'
                c.save()
                if dropout == operator:
                    # 自己退出，向队长发送消息
                    quit_email.delay(dropout, operator, carpool_id)
                else:
                    # 队长删除，向成员发送通知
                    quit_email(dropout, operator, carpool_id)
                return JsonResponse({"status": 0})
            else:
                # 队长已经进行移除操作
                return JsonResponse({"status": 0})
        except Exception as e:
            # 服务器异常 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040401"}})
    else:
        return HttpResponseForbidden()


# 加载车队信息 05
def get_carpool(request):
    if request.method == 'POST':
        try:
            station_list = ['太原南站', '太原站', '武宿机场']
            sort_list = ['timestamp', '-timestamp']
            data = json.loads(request.POST.get('data'))
            station = data.get('station')
            sort = data.get('sort')
            skip = data.get('skip')
            openid = data.get('openid')
            carpool_list = []
            if station == 0:
                # 全部站点
                c_l = Carpool.objects.order_by(sort_list[sort])\
                    .filter(~Q(openid=openid), state__lt=2)[skip:10]
                for c in c_l:
                    carpool_data = {
                        "id": c.id,
                        "station": c.station,
                        "startDate": c.startDate,
                        "startTime": c.startTime,
                        "timestamp": c.timestamp,
                        "maxNum": c.maxNum,
                        "currentNum": c.currentNum,
                        "avatarUrl": c.user_id.avatarUrl,
                        "name": c.user_id.name,
                        "qq": c.user_id.qq,
                        "SID": c.user_id.studentID
                    }
                    carpool_list.append(carpool_data)
            else:
                # 过滤站点
                c_l = Carpool.objects.order_by(sort_list[sort])\
                    .filter(~Q(openid=openid), state__lt=2, station=station_list[station-1])[skip:10]
                for c in c_l:
                    carpool_data = {
                        "id": c.id,
                        "station": c.station,
                        "startDate": c.startDate,
                        "startTime": c.startTime,
                        "timestamp": c.timestamp,
                        "maxNum": c.maxNum,
                        "currentNum": c.currentNum,
                        "avatarUrl": c.user_id.avatarUrl,
                        "name": c.user_id.name,
                        "qq": c.user_id.qq,
                        "SID": c.user_id.studentID
                    }
                    carpool_list.append(carpool_data)
            return JsonResponse({"status": 0, "data": carpool_list})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040501"}})
    else:
        return HttpResponseForbidden()


# 加载个人拼车数据 06
def get_personal(request):
    if request.method == 'POST':
        try:
            openid = request.POST.get('openid')
            u = WeappUser.objects.get(openid=openid)
            c = Carpool.objects.filter(user_id=u)
            carpool_data = {}
            if c:
                # 创建了拼车数据
                # 返回拼车数据与车友列表
                c = c[0]
                m_l = Apply.objects.filter(carpool_id=c)
                mate_list = []
                if m_l:
                    for m in m_l:
                        m_d = {
                            "avatarUrl": m.user_id.avatarUrl,
                            "nickName": m.user_id.nickName,
                            "SID": m.user_id.studentID,
                            "name": m.user_id.name,
                            "openid": m.user_id.openid,
                            "gender": m.user_id.gender
                        }
                        mate_list.append(m_d)
                carpool_data = {
                    "id": c.id,
                    "station": c.station,
                    "startDate": c.startDate,
                    "startTime": c.startTime,
                    "timestamp": c.timestamp,
                    "maxNum": c.maxNum,
                    "currentNum": c.currentNum,
                    "avatarUrl": c.user_id.avatarUrl,
                    "openid": c.user_id.openid,
                    "gender": c.user_id.gender,
                    "name": c.user_id.name,
                    "SID": c.user_id.studentID,
                    "state": c.state,
                    "mate_list": mate_list
                }
            else:
                # 没有拼车数据
                a = Apply.objects.filter(user_id=u)
                if a:
                    # 参与了拼车
                    c = a[0].carpool_id
                    m_l = Apply.objects.filter(carpool_id=c)
                    mate_list = []
                    if m_l:
                        for m in m_l:
                            m_d = {
                                "avatarUrl": m.user_id.avatarUrl,
                                "nickName": m.user_id.nickName,
                                "SID": m.user_id.studentID,
                                "name": m.user_id.name,
                                "openid": m.user_id.openid,
                                "gender": m.user_id.gender
                            }
                            mate_list.append(m_d)
                    carpool_data = {
                        "id": c.id,
                        "station": c.station,
                        "startDate": c.startDate,
                        "startTime": c.startTime,
                        "timestamp": c.timestamp,
                        "maxNum": c.maxNum,
                        "currentNum": c.currentNum,
                        "avatarUrl": c.user_id.avatarUrl,
                        "openid": c.user_id.openid,
                        "gender": c.user_id.gender,
                        "name": c.user_id.name,
                        "SID": c.user_id.studentID,
                        "state": c.state,
                        "mate_list": mate_list
                    }
            if carpool_data:
                return JsonResponse({"status": 0, "data": carpool_data})
            else:
                # 02
                return JsonResponse({"status": 1, "statusInfo": {"error": "还没有拼车数据丫！", "errorCode": "040602"}})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "040601"}})
    else:
        return HttpResponseForbidden()
