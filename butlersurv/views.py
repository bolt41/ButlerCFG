from django.shortcuts import render
from .models import SystemSurv, PartitionSurv, QuestionSurv, AnswerSurv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .engine import *

@login_required
def index(request):
    return render(request, 'main.html', {})



@login_required
def check_content(request): #выборка вопросов из БД
    if request.method == 'POST':
        sys = request.POST
        preobraz = dict(sys)
        del preobraz['csrfmiddlewaretoken']
        link_file = sent_to_file(preobraz)
        return render(request, 'good.html', {'file': link_file})

    #Получаем список словарей с поросами, вида [{'partition__type__name': 'Базовые подсистемы автоматизации', 'partition__name': 'Управление освещением', 'question': 'Тип управления светильниками'}
    qlist_question = QuestionSurv.objects.filter(is_use=True, partition__is_use=True, partition__type__is_use=True).values("partition__type__name", "partition__name", "question", "id")
    #Получаем список из значений QuerySeta
    list_question = list(qlist_question)
    results = {}
 #   print(list_question)
    #Получаем словарь разделов по подсистемам
    for el in list_question:
#        print(el)
        variable = AnswerSurv.objects.filter(question__id=el['id'], is_use=True).values_list("variable", flat=True)
        temp_list = list(variable)
        el['variable'] = temp_list

        if el['partition__type__name'] in results.keys():
            if el['partition__name'] in results[el['partition__type__name']].keys():
                results[el['partition__type__name']][el['partition__name']][el['id']] =[el['question'],el['variable']]
            else:
                results[el['partition__type__name']][el['partition__name']] = {}
                results[el['partition__type__name']][el['partition__name']][el['id']] = [el['question'], el['variable']]
        else:
            results[el['partition__type__name']] = {}
            results[el['partition__type__name']][el['partition__name']] = {}
            results[el['partition__type__name']][el['partition__name']][el['id']] = [el['question'],el['variable']]
#    print(results)
 #   response = JsonResponse(results, safe=False)
    # print(response.content)
    # print(html.unescape(response))
    return render(request, 'check.html', {'question': results})

