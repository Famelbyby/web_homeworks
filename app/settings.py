from django.contrib.auth import authenticate, login

from stackoverflow.models import Profile, Question, Tag, Answer
from django.db.models import Count
from templates.components.forms import LoginForm, RegisterForm, AskQuestion, EditForm

QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 7

SORT_BY = {'index': 'new', 'hot': 'hot', 'tag': 'tag'}


def pages_range(page, pages_count):
    if pages_count == 1:
        return []
    if pages_count < 5:
        return [i for i in range(1, pages_count + 1)]
    if 4 < page < pages_count - 3:
        return [1, '...'] + [i for i in range(page - 2, page + 3)] + ['...', pages_count]
    elif page > 4:
        return [1, '..'] + [i for i in range(page - 2, pages_count + 1)]
    return [i for i in range(1, page + 3)] + ['...', pages_count]


def check_page(request):
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            return -1
    except:
        return -1
    return page


def paginate(request, typeRequest, tag_name='null'):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    if typeRequest == 'index':
        questions = index_questions(page)
    elif typeRequest == 'hot':
        questions = hot_questions(page)
    else:
        questions = tag_questions(page, tag_name)
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (Question.objects.count() + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE),
            'sort_by': SORT_BY[typeRequest], 'isLogIn': False, 'tag_name': tag_name}


def index_questions(page):
    return Question.objects.newer()[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]


def hot_questions(page):
    return Question.objects.hot()[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]


def tag_questions(page, tag_name):
    return Tag.objects.isThisTag(tag_name).questions.all()[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]


def certain_question(request, question_id):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    try:
        question = Question.objects.get(pk=question_id)
    except:
        return {'page': -1}
    tags = question.tags.all()
    answers = question.answer_set.all()[(page - 1) * ANSWERS_PER_PAGE: page * ANSWERS_PER_PAGE]
    if not len(answers):
        return {'page': -1}
    return {'question': question, 'tags': tags, 'answers': answers, 'page': page,
            'pages': pages_range(page, (question.answer_set.count() + ANSWERS_PER_PAGE - 1) // ANSWERS_PER_PAGE),
            'isLogIn': True}


# REWRITE WHAT ABOVE THIS
def login_user(request):
    if request.method == 'POST':
        return LoginForm(request.POST)
    return LoginForm()


def signup(request):
    if request.method == 'POST':
        return RegisterForm(request.POST)
    return RegisterForm()


def ask(request):
    if request.method == 'POST':
        return AskQuestion(request.POST)
    return AskQuestion()


def profile_edit(request):
    return EditForm()
