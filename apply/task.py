# from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import json
import time
from .models import Apply, Carpool
from user.models import WeappUser
from notice.models import PersonalNotice

from_email = settings.DEFAULT_FROM_EMAIL


@shared_task
def create_email(title, openid, data):
    # 创建拼车时向创建者发送通知
    data = json.loads(data)
    sending = f"{data['qq']}@qq.com"
    name = data.get('name', '用户')
    sid = data.get('SID', '')
    start_date = data.get('startDate', '')
    start_time = data.get('startTime', '')
    station = data.get('station', '')
    current_num = data.get('currentNum', '1')
    max_num = data.get('maxNum', '')
    content = f"""
    <div>
    <table cellpadding="0" align="center"
           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
        <tbody>
        <tr>
            <th valign="middle"
                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title}（科大信息）</font>
            </th>
        </tr>
        <tr>
            <td>
                <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                            <font style="line-height: 22px; " size="4">
                                亲爱的 {name}</font>
                        </font>
                    </h2>
                    <p>您的账号：{sid}<br>
                        您的发车日期：<b>{start_date} {start_time}</b><br>
                        您的乘车地点：<b>{station}</b><br>
                        当前车队人数：<b>{current_num}/{max_num}</b><br>
                        <b>请您使用拼车系统时注意辨别信息真伪，谨防上当受骗！</b><br>
                        如果您有什么疑问可以通过小程序客服消息联系客服。</p>
                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                    <div style="width:100%;margin:0 auto;">
                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                            <p>此为系统邮件，请勿回复<br>
                            </p>
                            <p>©科大信息</p>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
    """
    try:
        msg = EmailMultiAlternatives(title, content, from_email, (sending,))
        msg.content_subtype = 'html'
        msg.send()
        # 发送到消息通知系统
        u = WeappUser.objects.get(openid=openid)
        PersonalNotice.objects.create(title=title, content=content, origin="科大拼车",
                                      timestamp=int(time.time() * 1000), _to=u)
        return '%s %s Success' % (name, sending)
    except Exception:
        # return '%s Exception' % user_name
        return '%s %s Fail' % (name, sending)


@shared_task
def delete_email(openid, mates):
    # 删除队伍时向创建者发送通知
    u = WeappUser.objects.get(openid=openid)
    mates = mates.split(',')
    name = u.name
    sid = u.studentID
    sending = u.email
    title = '您的队伍已删除！'
    content_h = f"""
    <div>
    <table cellpadding="0" align="center"
           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
        <tbody>
        <tr>
            <th valign="middle"
                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title}（科大信息）</font>
            </th>
        </tr>
        <tr>
            <td>
                <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                            <font style="line-height: 22px; " size="4">
                                亲爱的 {name}</font>
                        </font>
                    </h2>
                    <p>您的账号：{sid}<br>
                        <b>您的车队已经成功删除。</b><br>
                        感谢您的使用，如果您有任何建议，可以通过小程序 个人中心->反馈 向我们发送建议。<br>
                        如果您有什么疑问可以通过小程序客服消息联系客服。<br>
                        感谢您的使用！</p>
                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                    <div style="width:100%;margin:0 auto;">
                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                            <p>此为系统邮件，请勿回复<br>
                            </p>
                            <p>©科大信息</p>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
    """
    if sending:
        try:
            msg = EmailMultiAlternatives(title, content_h, from_email, (sending,))
            msg.content_subtype = 'html'
            msg.send()
            # 发送到消息通知系统
            PersonalNotice.objects.create(title=title, content=content_h, origin="科大拼车",
                                          timestamp=int(time.time() * 1000), _to=u)
            if len(mates) > 0:
                for mate in mates:
                    u = WeappUser.objects.get(openid=mate)
                    name_m = u.nickName
                    if u.name:
                        name_m = u.name
                    content_m = f"""
                    <div>
                    <table cellpadding="0" align="center"
                           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
                        <tbody>
                        <tr>
                            <th valign="middle"
                                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title}（科大信息）</font>
                            </th>
                        </tr>
                        <tr>
                            <td>
                                <div style="padding:25px 35px 40px; background-color:#fff;">
                                    <h2 style="margin: 5px 0px; ">
                                        <font color="#333333" style="line-height: 20px; ">
                                            <font style="line-height: 22px; " size="4">
                                                亲爱的 {name_m}</font>
                                        </font>
                                    </h2>
                                    <p>您的队伍已被队长解散<br>
                                        <b>您可以通过{sid}@tyust.edu.cn</b><br>
                                        前往企业微信联系队长<br>
                                        感谢您的使用，如果您有任何建议，可以通过小程序 个人中心->反馈 向我们发送建议。<br>
                                        如果您有什么疑问可以通过小程序客服消息联系客服。<br>
                                        感谢您的使用！</p>
                                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                                    <div style="width:100%;margin:0 auto;">
                                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                                            <p>此为系统邮件，请勿回复<br>
                                            </p>
                                            <p>©科大信息</p>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                    """
                    PersonalNotice.objects.create(title=title, content=content_m, origin="科大拼车",
                                                  timestamp=int(time.time() * 1000), _to=u)
            return '%s %s Success' % (name, sending)
        except Exception as e:
            # return '%s Exception' % user_name
            return '%s %s Fail' % (name, sending)
    else:
        return '%s Email None' % name


@shared_task
def join_email(title_h, carpool_id, openid):
    title_m = '加入队伍成功！'

    # 获取队长信息
    c = Carpool.objects.get(id=carpool_id)
    sending_h = c.user_id.email
    name_h = c.user_id.name
    sid_h = c.user_id.studentID

    # 获取拼车信息
    start_date = c.startDate
    start_time = c.startTime
    station = c.station
    current_num = c.currentNum
    max_num = c.maxNum

    # 获取队员列表
    mates = Apply.objects.filter(carpool_id=c)
    members = []
    gender_list = ['男', '女']
    for mate in mates:
        if mate.user_id.name:
            members.append(f'{mate.user_id.nickName}({mate.user_id.name})({gender_list[mate.user_id.gender]})<br>')
        else:
            members.append(f'{mate.user_id.nickName}(未实名)<br>')

    # 队长信息模板
    content_h = f"""
    <div>
    <table cellpadding="0" align="center"
           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
        <tbody>
        <tr>
            <th valign="middle"
                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title_h}（科大信息）</font>
            </th>
        </tr>
        <tr>
            <td>
                <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                            <font style="line-height: 22px; " size="4">
                                亲爱的 {name_h}</font>
                        </font>
                    </h2>
                    <p>您的账号：{sid_h}<br>
                        您的发车日期：<b>{start_date} {start_time}</b><br>
                        您的乘车地点：<b>{station}</b><br>
                        当前车队人数：<b>{current_num}/{max_num}</b><br>
                        当前车队成员：<b>{'、'.join(members)}</b><br>
                        <b>请前往小程序查看！</b><br>
                        <b>请您使用拼车系统时注意辨别信息真伪，谨防上当受骗！</b><br>
                        如果您有什么疑问可以通过小程序客服消息联系客服。</p>
                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                    <div style="width:100%;margin:0 auto;">
                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                            <p>此为系统邮件，请勿回复<br>
                            </p>
                            <p>©科大信息</p>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
    """

    # 加入者信息
    u = WeappUser.objects.get(openid=openid)
    sending_m = u.email
    name_m = u.name
    sid_m = u.studentID

    # 加入者信息模板
    content_m = f"""
    <div>
    <table cellpadding="0" align="center"
           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
        <tbody>
        <tr>
            <th valign="middle"
                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title_m}（科大信息）</font>
            </th>
        </tr>
        <tr>
            <td>
                <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                            <font style="line-height: 22px; " size="4">
                                亲爱的 {name_m}</font>
                        </font>
                    </h2>
                    <p>您的账号：{sid_m}<br>
                        您的队长：<b>{name_h}</b> 学号：{sid_h}<br>
                        您的发车日期：<b>{start_date} {start_time}</b><br>
                        您的乘车地点：<b>{station}</b><br>
                        当前车队人数：<b>{current_num}/{max_num}</b><br>
                        当前车队成员：<b>{'、'.join(members)}</b><br>
                        <b>请您使用拼车系统时注意辨别信息真伪，谨防上当受骗！</b><br>
                        如果您有什么疑问可以通过小程序客服消息联系客服。</p>
                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                    <div style="width:100%;margin:0 auto;">
                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                            <p>此为系统邮件，请勿回复<br>
                            </p>
                            <p>©科大信息</p>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
    """

    try:
        # 队长信息
        msg_h = EmailMultiAlternatives(title_h, content_h, from_email, (sending_h,))
        msg_h.content_subtype = 'html'
        msg_h.send()

        # 加入者信息
        msg_m = EmailMultiAlternatives(title_m, content_m, from_email, (sending_m,))
        msg_m.content_subtype = 'html'
        msg_m.send()


        # 发送到消息通知系统
        # 给队长发送通知
        PersonalNotice.objects.create(title=title_h, content=content_h, origin="科大拼车",
                                      timestamp=int(time.time() * 1000), _to=c.user_id)
        # 给加入者发送通知
        PersonalNotice.objects.create(title=title_m, content=content_m, origin="科大拼车",
                                      timestamp=int(time.time() * 1000), _to=u)

        return '%s %s %s %s Success' % (name_m, sending_m, name_h, sending_h)
    except Exception:
        # return '%s Exception' % user_name
        return '%s %s %s %s Fail' % (name_m, sending_m, name_h, sending_h)


@shared_task
def quit_email(dropout, operator, carpool_id):
    # 获取退出者信息
    u = WeappUser.objects.get(openid=dropout)
    # 获取队伍信息
    c = Carpool.objects.get(id=carpool_id)

    # 判断退出情况

    name = ''
    title = ''
    sending = ''
    message = ''
    contact = ''
    if dropout == operator:
        # 队员自己退出
        # 向队长发送信息
        title = '您有队员退出！'
        name = c.user_id.name
        sending = c.user_id.email
        gender_list = ['男', '女']
        if u.studentID:
            message = f'<b>{u.nickName}({u.name})({gender_list[u.gender]})</b>退出了队伍<br>'
            contact = f'您可以通过<b>{u.studentID}@tyust.edu.cn</b>前往企业微信联系对方<br>'
        else:
            message = f'<b>{u.nickName}(未实名)</b>退出了队伍<br>'

    else:
        # 队长删除
        # 向队员发送消息
        title = '您被队长移除！'
        if u.name:
            name = u.name
        else:
            name = u.nickName
        sending = u.email
        message = f'<b>{c.user_id.name}</b>将您移出了队伍<br>'
        contact = f'您可以通过<b>{c.user_id.studentID}@tyust.edu.cn</b>前往企业微信联系对方<br>'

    content = f"""
    <div>
    <table cellpadding="0" align="center"
           style="width: 100%; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
        <tbody>
        <tr>
            <th valign="middle"
                style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">{title}（科大信息）</font>
            </th>
        </tr>
        <tr>
            <td>
                <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                            <font style="line-height: 22px; " size="4">
                                亲爱的 {name}</font>
                        </font>
                    </h2>
                    <p>
                        {message}
                        {contact}
                        <b>请您使用拼车系统时注意辨别信息真伪，谨防上当受骗！</b><br>
                        如果您有什么疑问可以通过小程序客服消息联系客服。
                    </p>
                    <p align="right" style="margin-top: 50px">科大拼车系统</p>
                    <div style="width:100%;margin:0 auto;">
                        <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                            <p>此为系统邮件，请勿回复<br>
                            </p>
                            <p>©科大信息</p>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
        </tbody>
    </table>
    </div>
    """
    try:
        msg = EmailMultiAlternatives(title, content, from_email, (sending,))
        msg.content_subtype = 'html'
        msg.send()

        # 发送到消息通知系统
        if dropout == operator:
            # 给队长发送通知
            PersonalNotice.objects.create(title=title, content=content, origin="科大拼车",
                                          timestamp=int(time.time() * 1000), _to=c.user_id)
        else:
            # 给队员发送通知
            PersonalNotice.objects.create(title=title, content=content, origin="科大拼车",
                                          timestamp=int(time.time() * 1000), _to=u)

        return '%s %s Success' % (name, sending)
    except Exception:
        # return '%s Exception' % user_name
        return '%s %s Fail' % (name, sending)