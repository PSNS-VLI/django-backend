from user.models import WeappUser


def get_like_queryset(openid, *args):
    # 查询用户点赞信息
    try:
        return WeappUser.objects.prefetch_related(*args).get(openid=openid)
    except Exception:
        return None