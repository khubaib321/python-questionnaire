from django.urls import path, include
from . import questionnaires

urlpatterns = [
    path('', questionnaires.list, name='questionnaires-list'),
    path('chat/', questionnaires.chat, name='questionnaires-chat')
]
