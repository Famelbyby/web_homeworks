from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from app import settings


# Create your views here.


def index(request):
    context = settings.paginate(request, 'index')
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context)


def hot(request):
    context = settings.paginate(request, 'hot')
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context)


def tag(request, tag_name):
    context = settings.paginate(request, 'tag', tag_name)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html', {'isLogIn': False})


def question(request, question_id):
    context = settings.certain_question(request, question_id)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'question.html', context)


def signup(request):
    return render(request, 'signup.html', {'isLogIn': False})


def ask(request):
    return render(request, 'ask.html', {'isLogIn': True})
