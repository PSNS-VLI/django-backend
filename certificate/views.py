from django.http import JsonResponse
from .models import Certificates

# Create your views here.


def getCer(request, cerid):
    if request.method == 'GET':
        if cerid >= 0:
            try:
                # initial the instance of the Certificate
                cer = Certificates.objects.get(id=cerid)
                result = {
                    'cer_name' : cer.cer_name, 'cer_recommend_num' : cer.cer_recommend_num,
                    'cer_recommend_score' : cer.cer_recommend_score, 'cer_popularity' : cer.cer_popularity,
                    'cer_host_unit' : cer.cer_host_unit, 'cer_reach' : cer.cer_reach,
                    'cer_introduction' : cer.cer_introduction, 'cer_tags' : cer.cer_introduction,
                    'cer_follow' : cer.cer_follow, 'cer_manage' : cer.cer_manage,
                    'apply_fee' : cer.apply_fee, 'apply_condition' : cer.apply_condition,
                    'apply_time' : cer.apply_time, 'apply_way' : cer.apply_way,
                    'apply_suggest' : cer.apply_suggest, 'exam_suggest' : cer.exam_suggest,
                    'exam_exempt' : cer.exam_exempt, 'exam_pass_rate' : cer.exam_pass_rate,
                    'exam_class' : cer.exam_class, 'exam_time' : cer.exam_time,
                    'exam_frequency' : cer.exam_frequency, 'exam_place' : cer.exam_place,
                    'exam_subjects' : cer.exam_subjects, 'exam_form' : cer.exam_form,
                    'exam_question_type' : cer.exam_question_type, 'exam_info_check' : cer.exam_info_check,
                    'exam_epidemic_prevention' : cer.exam_epidemic_prevention,
                    'shortcut_info_collect' : cer.shortcut_info_collect,
                    'shortcut_official_website' : cer.shortcut_official_website,
                    'shortcut_score_inquiry' : cer.shortcut_score_inquiry, 'recommend_app' : cer.recommend_app,
                    'recommend_website' : cer.recommend_website, 'recommend_post' : cer.recommend_post,
                    'scans' : cer.scans, 'create_time': cer.create_time , 'update_time' : cer.update_time,
                    'operator' : cer.operator
                }
                return JsonResponse(result, safe=False)
            except Exception as e:
                print(e)
                return JsonResponse('ok', safe=False)


def getHot(request):
    if request.method == 'GET':
        try:
            cer = Certificates.objects.order_by('-scans')[:6]
            result= []
            for i in list(range(6)):
                result.append({'id': cer[i].id, 'scans': cer[i].scans, 'cer_name': cer[i].cer_name})
            data = {'status': 'ok', 'data': result}
            return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            data = {'status': 'error', 'code': '500'}
            return JsonResponse(data, safe=False)