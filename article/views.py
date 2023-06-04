from django.http import JsonResponse, HttpResponseForbidden
from .models import Article

# Create your views here.
# article 应用编码为 05


# 加载推荐文章 01
def recommend_article(request):
    if request.method == 'POST':
        try:
            # 随便返回三篇文章
            # 获取skip和num
            skip = request.POST.get('skip', 0)
            num = request.POST.get('num', 3)
            a_l = Article.objects.prefetch_related('tags').all()[int(skip):int(skip)+int(num)]
            data = []
            for a in a_l:
                data.append({
                    "id": a.id,
                    "title": a.title,
                    "cover": a.cover,
                    "preview": a.preview,
                    "tags": [item.name for item in a.tags.all()]
                })
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "050101"}})
    else:
        return HttpResponseForbidden()


# 02
def get_article(request):
    if request.method == 'POST':
        try:
            _id = request.POST.get("id")
            a = Article.objects.get(id=_id)
            data = {
                "id": a.id,
                "title": a.title,
                "content": a.content,
                "origin": a.origin,
                "visitor": a.visitor,
                "cover": a.cover
            }
            return JsonResponse({"status": 0, "data": data})
        except Exception as e:
            # 01
            print(e)
            return JsonResponse({"status": 1, "statusInfo": {"error": "服务器异常", "errorCode": "050201"}})
    else:
        return HttpResponseForbidden()