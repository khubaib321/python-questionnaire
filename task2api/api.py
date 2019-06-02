from django.shortcuts import render
from django.http import JsonResponse
from . helpers import dirHelper, chatHelper
from django.views.decorators.csrf import csrf_exempt


def list(request):
    data = getQuestionnairesData()
    response = []
    for key in data:
        response.append(key)
    return JsonResponse(response, safe=False)


@csrf_exempt
def chat(request):
    if request.method != 'POST':
        return JsonResponse('This Method Only Serves POST Requests.', safe=False)
    dirHelper.ensureDirectoryExist('task2api/assets/conversations')
    response = chatHelper.initializeChat(request)
    return JsonResponse(response, safe=False)


def getQuestionnairesData():
    return dirHelper.readDataFromJsonFile('task2api/res/questionnaires.json')
