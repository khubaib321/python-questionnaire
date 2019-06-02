import json
import random
from . import dirHelper
from pprint import pprint


def initializeChat(request):
    response = {}
    data = json.loads(request.body.decode('utf-8'))
    conversationID = data['cid']
    questionnaireName = data['questionnaire']
    if not conversationID:
        return response
    if (int(conversationID) < 1):
        conversationID = random.randint(1, 1000000)
        dirHelper.writeDataToJsonFile('../assets/conversations/' +
                                      str(conversationID) + questionnaireName + '.json', {}, False)
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
    dirHelper.writeDataToJsonFile('../assets/conversations/' + str(conversationID) +
                                  questionnaireName + '.json', chatHistory, True)
    # return next question
    return nextQuestion


def getChatHistory(conversationID, questionnaireName):
    if (int(conversationID) < 1):
        return {}
    return dirHelper.readDataFromJsonFile('../assets/conversations/' + str(conversationID) + questionnaireName + '.json')


def getNextQuestion(chatHistory, questionnaireName):
    nextQuestion = {}
    questionnaires = dirHelper.readDataFromJsonFile(
        '../res/questionnaires.json')
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
        printHistory(chatHistory, questionnaireName)
        return conversationPart
    # otherwise return the next question in conversation
    if hasattr(conversationPart, 'items'):
        for key, value in conversationPart.items():
            nextQuestion = {key: value}
            return nextQuestion
    return ''


def printHistory(chatHistory, questionnaireName):
    questionnaires = dirHelper.readDataFromJsonFile(
        '../res/questionnaires.json')
    conversationPart = questionnaires[questionnaireName]
    chatHistoryString = ''
    if hasattr(chatHistory, 'items'):
        for key, value in chatHistory.items():
            if not chatHistoryString:
                chatHistoryString += key + '->' + value
            else:
                chatHistoryString += '->' + key + '->' + value
    print(questionnaireName)
    print(chatHistoryString)
