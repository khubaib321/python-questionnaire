import os
import json
import random
from pprint import pprint
from collections import OrderedDict
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def list(request):
    data = getQuestionnairesData()
    response = []
    for key in data:
        response.append(key)
    return JsonResponse(response, safe=False)

@csrf_exempt
def chat(request):
    if (request.method != 'POST'):
        return JsonResponse('This Method Only Serves POST Requests.', safe=False)
    response = initializeChat(request)
    return JsonResponse(response, safe=False)

def getNextQuestion(chatHistory, questionnaireName):
    nextQuestion = {}
    questionnaires = getQuestionnairesData()
    conversationPart = questionnaires[questionnaireName]
    # if chat history is empty it means chat is just starting
    if not hasattr(chatHistory, 'items'):
        for key, value in conversationPart.items():
            nextQuestion = {key, value}
            return nextQuestion
    # get to last conversation item in history and return if found
    for key, value in chatHistory.items():
        if value and value in conversationPart:
            conversationPart = conversationPart[value]
    # if only last response is remaining means chat has ended
    if type(conversationPart) is str:
        return conversationPart
    # otherwise return the next question in conversation
    if hasattr(conversationPart, 'items'):
        for key, value in conversationPart.items():
            nextQuestion = {key: value}
            return nextQuestion
    return ''

def getFullPath(relativePath):
    fileDir = os.path.dirname(__file__)
    absolutePath = os.path.join(fileDir, relativePath)
    return absolutePath

def readDataFromJsonFile(relativePath):
    data = {}
    fullPath = getFullPath(relativePath)
    try:
        with open(fullPath, 'r') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)
    except IOError:
        print("Could not open file for reading: '" + relativePath + "'")
    return data

def writeDataToJsonFile(relativePath, data, checkExisting):
    fullPath = getFullPath(relativePath)
    if checkExisting:
        try:
            with open(fullPath, 'r') as file:
                pass
        except IOError:
            print("Could not open file for reading: '" + relativePath + "'")
            return
    try:
        with open(fullPath, 'w') as file:
            file.write(json.dumps(data))
    except IOError:
        print("Could not open file for writing: '" + relativePath + "'")


def getQuestionnairesData():
    return readDataFromJsonFile('res/questionnaires.json')

def initializeChat(request):
    response = {}
    data = json.loads(request.body.decode('utf-8'))
    conversationID = data['cid']
    questionnaireName = data['questionnaire']
    if not conversationID:
        return response
    if (int(conversationID) < 1):
        conversationID = random.randint(1, 1000000)
        writeDataToJsonFile('assets/conversations/' + str(conversationID) + questionnaireName + '.json', {}, False)
    # get next question and send back in response with conversation id
    nextQuestion = continueChat(data)
    response = {
        'cid': conversationID,
        'name': questionnaireName,
        'response': nextQuestion,
    }
    return response

def continueChat(data):
    if not 'cid' in data or not 'questionnaire' in data or not 'question' in data or not 'answer' in data:
        print('Data missing in request')
        return {}
    conversationID = data['cid']
    questionnaireName = data['questionnaire']
    questionAsked = data['question']
    answerGiven = data['answer']
    # get chat history and next question
    chatHistory = getChatHistory(conversationID, questionnaireName)
    # update chat history
    if questionAsked:
        chatHistory[questionAsked] = answerGiven
    nextQuestion = getNextQuestion(chatHistory, questionnaireName)
    writeDataToJsonFile('assets/conversations/' + str(conversationID) + questionnaireName + '.json', chatHistory, True)
    # return next question
    return nextQuestion

def getChatHistory(conversationID, questionnaireName):
    if (int(conversationID) < 1):
        return {}
    return readDataFromJsonFile('assets/conversations/' + str(conversationID) + questionnaireName + '.json')
