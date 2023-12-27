import random

from django.contrib.postgres.search import SearchVector
from django.contrib.auth import authenticate, login
from django.forms import model_to_dict
from django.core.cache import cache
from stackoverflow.models import Profile, Question, Tag, Answer, AnswerLikes, QuestionLikes
from django.db.models import Count
from templates.components.forms import LoginForm, RegisterForm, AskQuestion, EditForm, GiveAnswer

QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 7
PROFILE_PER_PAGE = 15
POPULAR_TAGS_COUNT = 20
POPULAR_PROFILES_COUNT = 10


def all_popular():
    cache_key_tags = 'popular_tags'
    tags = cache.get(cache_key_tags)
    cache_key_profiles = 'popular_profiles'
    profiles = cache.get(cache_key_profiles)
    return {'popular_tags': tags,
            'popular_profiles': profiles}


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


def index_questions(request):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    all_ques = Question.objects.newer()
    count_all_ques = all_ques.count()
    questions = all_ques[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (count_all_ques + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE),
            'type_sort': 'New questions'}


def hot_questions(request):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    all_ques = Question.objects.hot()
    count_all_ques = all_ques.count()
    questions = all_ques[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (count_all_ques + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE),
            'type_sort': 'Hot questions'}


def tag_questions(request, tag_name):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    all_ques = Tag.objects.isThisTag(tag_name).questions.all()
    count_all_ques = all_ques.count()
    questions = all_ques[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (count_all_ques + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE),
            'type_sort': f'Tag: {tag_name}'}


def query_question(request, query_name):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    all_ques = Question.objects.annotate(search=SearchVector('title') +
                            SearchVector('description')).filter(search=query_name)
    count_ques = all_ques.count()
    questions = all_ques[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (count_ques + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE),
            'type_sort': f'Query: {query_name}', 'query_question': query_name}


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
    can_banned = [request.user.profile == question.author_id and request.user.profile != a.author and
                  AnswerLikes.objects.filter(user_id=request.user, answer_id=a).count() == 0 for a in answers]
    return {'question': question, 'tags': tags, 'answers': answers, 'page': page,
            'pages': pages_range(page, (question.answer_set.count() + ANSWERS_PER_PAGE - 1) // ANSWERS_PER_PAGE),
            'can_banned': can_banned}


def give_answer(request, question_id):
    if request.method == 'POST':
        form = GiveAnswer(request.POST)
        if form.is_valid():
            answer = form.save()
            answer.author = request.user.profile
            question = Question.objects.get(pk=question_id)
            answer.question = question
            answer.save()
            return answer
    return GiveAnswer()


def login_user(request):
    if request.method == 'POST':
        return LoginForm(request.POST)
    return LoginForm()


def signup(request):
    if request.method == 'POST':
        return RegisterForm(request.POST, request.FILES)
    return RegisterForm()


def ask(request):
    if request.method == 'POST':
        return AskQuestion(request.POST)
    return AskQuestion()


def profile(request, profile_id):
    page = check_page(request)
    if page == -1:
        return [-1, -1]
    try:
        profile = Profile.objects.get(pk=profile_id)
    except:
        return [-1, -1]
    return [profile, request.user.profile.follows.filter(pk=profile_id).count() > 0]


def profile_edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    return EditForm(initial=model_to_dict(request.user))


def follow(request, profile_id):
    Profile.objects.toggleFollow(request.user, profile_id)


def follows(request):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    all_follows = Profile.objects.get(user=request.user).follows.all()
    count_follows = all_follows.count()
    my_follows = all_follows[(page - 1) * PROFILE_PER_PAGE: page * PROFILE_PER_PAGE]
    return {'follows': my_follows, 'page': page,
            'pages': pages_range(page, (count_follows + PROFILE_PER_PAGE - 1) // PROFILE_PER_PAGE)}


def my_questions(request):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    my_ques = Question.objects.filter(author_id=request.user.profile)
    count_my_ques = my_ques.count()
    questions = my_ques[(page - 1) * QUESTIONS_PER_PAGE: page * QUESTIONS_PER_PAGE]
    tags = [list(q.tags.all()) for q in questions]
    answers = list(q.answer_set.count() for q in questions)
    return {'answers': answers, 'tags': tags, 'questions': questions, 'page': page,
            'pages': pages_range(page, (count_my_ques + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE)}


def my_answers(request):
    page = check_page(request)
    if page == -1:
        return {'page': -1}
    my_ans = Answer.objects.filter(author=request.user.profile)
    count_ans = my_ans.count()
    answers = my_ans[(page - 1) * ANSWERS_PER_PAGE: page * ANSWERS_PER_PAGE]
    return {'answers': answers, 'page': page,
            'pages': pages_range(page, (count_ans + ANSWERS_PER_PAGE - 1) // ANSWERS_PER_PAGE)}


def like(request):
    type_req = request.POST.get('type_req')
    if type_req == 'answer':
        answer_id = request.POST.get('answer_id')
        answer = Answer.objects.get(pk=answer_id)
        AnswerLikes.objects.toggleLike(request.user, answer)
        answer.rating = AnswerLikes.objects.filter(answer_id=answer).count()
        answer.save()
        return answer.rating
    else:
        question_id = request.POST.get('question_id')
        question = Question.objects.get(pk=question_id)
        QuestionLikes.objects.toggleLike(request.user, question)
        question.rating = QuestionLikes.objects.filter(question_id=question).count()
        question.save()
        return question.rating


def ban_answer(request):
    if request.POST.get('type_req', '') == 'yes':
        answer = Answer.objects.get(pk=request.POST.get('answer_id'))
        AnswerLikes.objects.toggleLike(request.user, answer)
        answer.rating = AnswerLikes.objects.filter(answer_id=answer).count()
        answer.save()
    if request.POST.get('type_req', '') == 'no':
        Answer.objects.get(pk=request.POST.get('answer_id')).delete()
    return


def delete_something(request):
    delete_id = request.POST.get('delete_id')
    if request.POST.get('type_query', '') == 'answer':
        Answer.objects.get(pk=delete_id).delete()
    if request.POST.get('type_query', '') == 'question':
        Question.objects.get(pk=delete_id).delete()
