from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound

# Create your views here.

QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 30

QUESTIONS = [
    {'title': 'What do you think: is a pink colour for men?',
     'description': 'My friends laugh at me, because I like pink... Help me...',
     'answers': 5,
     'question_id': i + 1}
    for i in range(100)
]

ANSWERS = [
    {'title': 'What do you think: is a pink colour for men?',
     'description': 'My friends laugh at me, because I like pink... Help me...',
     'answers': 5,
     'question_id': i + 1}
    for i in range(120)
]


def paginate(objects, que_per_page, page):
    pages = Paginator(objects, que_per_page)
    return pages.get_page(page)


def index(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        return HttpResponseNotFound('Bad request')
    if page > len(QUESTIONS) / QUESTIONS_PER_PAGE or page < 1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, QUESTIONS_PER_PAGE, page), 'isLogIn': False,
                                          'pages': range(1, 6), 'sort_by': 'new'})


def hot(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        return HttpResponseNotFound('Bad request')
    if page > len(QUESTIONS) / QUESTIONS_PER_PAGE or page < 1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, QUESTIONS_PER_PAGE, page), 'isLogIn': False,
                                          'pages': range(1, 6), 'sort_by': 'hot'})


def tag(request, tag_name):
    try:
        page = int(request.GET.get('page', 1))
    except:
        return HttpResponseNotFound('Bad request')
    if page > len(QUESTIONS) / QUESTIONS_PER_PAGE or page < 1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, QUESTIONS_PER_PAGE, page), 'isLogIn': True,
                                          'pages': range(1, 6), 'sort_by': 'tag', 'tag_name': tag_name})


def login(request):
    return render(request, 'login.html', {'isLogIn': False})


def question(request, question_id):
    try:
        page = int(request.GET.get('page', 1))
    except:
        return HttpResponseNotFound('Bad request')
    if page > len(ANSWERS) / ANSWERS_PER_PAGE or page < 1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'question.html', {'answers': paginate(ANSWERS, ANSWERS_PER_PAGE, page), 'isLogIn': True,
                                             'pages': range(1, 5)})


def signup(request):
    return render(request, 'signup.html', {'isLogIn': False})


def ask(request):
    return render(request, 'ask.html', {'isLogIn': True})
