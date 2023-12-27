from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.conf import settings as conf_settings
from app import settings
from cent import Client
import jwt
import time

client = Client(conf_settings.CENTRIFUGO_API_URL, api_key=conf_settings.CENTRIFUGO_API_KEY, timeout=1)


# Create your views here.

def get_centrifugo_data(user_id, channel):
    return {
        'centrifugo': {
            'token': jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 10 * 60},
                                conf_settings.CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256"),
            'ws_url': conf_settings.CENTRIFUGO_WS_URL,
            'channel': channel,
        }
    }


def all_popular():
    return settings.all_popular()


@login_required(login_url='login', redirect_field_name='continue')
def index(request):
    query = request.GET.get('query_question', '')
    if query != '':
        return query_question(request, query)
    context = settings.index_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context | all_popular())


@login_required(login_url='login', redirect_field_name='continue')
def hot(request):
    context = settings.hot_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context | all_popular())


@login_required(login_url='login', redirect_field_name='continue')
def tag(request, tag_name):
    context = settings.tag_questions(request, tag_name)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', context | all_popular())


@login_required
def query_question(request, query_name):
    context = settings.query_question(request, query_name)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', context | all_popular())


@csrf_protect
def log_in(request):
    form = settings.login_user(request)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, **form.cleaned_data)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('continue', '/'))
        form.add_error('password', 'Password is incorrect')
    return render(request, 'login.html', {'form': form} | all_popular())


@csrf_protect
@login_required
def give_answer(request):
    question_id = request.POST.get('question_id')
    answer = settings.give_answer(request, question_id)
    client.publish(f'question.{question_id}',
                   {"description": answer.description,
                    "answer_rating": answer.rating,
                    "answer_id": answer.id,
                    "author_id": answer.author.id,
                    "author": answer.author.user.username,
                    })
    return JsonResponse({})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def question(request, question_id):
    if request.method == 'GET':
        context = settings.certain_question(request, question_id)
        if context['page'] == -1:
            return HttpResponseNotFound('Bad request')
        context['form'] = settings.give_answer(request, question_id)
        return render(request, 'question.html',
                      context | all_popular() | get_centrifugo_data(request.user.id, f'question.{question_id}'))
    [count, answer] = settings.give_answer(request, question_id)
    client.publish(f'question.{question_id}', {"value": 'lol'})
    return redirect(reverse('question', kwargs={'question_id': question_id}) +
                    '?page=' + str(count) + '#' + str(answer.id))


@csrf_protect
def signup(request):
    form = settings.signup(request)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(reverse('index'))
    return render(request, 'signup.html', {'form': form} | all_popular())


@csrf_protect
def log_out(request):
    logout(request)
    return redirect(reverse('login'))


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    form = settings.ask(request)
    if request.method == 'POST' and form.is_valid():
        question = form.save()
        question.date = timezone.now()
        question.author_id = request.user.profile
        question.save()
        return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, 'ask.html', {'form': form} | all_popular())


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def profile(request, profile_id):
    if request.method == 'POST':
        settings.follow(request, profile_id)
        return redirect(request.META.get('HTTP_REFERER'))
    [context, isFollowed] = settings.profile(request, profile_id)
    if context == -1:
        return HttpResponseNotFound('404 Not found')
    return render(request, 'profile.html', {'profile': context, 'isFollowed': isFollowed} | all_popular())


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def profile_edit(request):
    if request.method == 'GET':
        context = settings.profile_edit(request)
        return render(request, 'profile_edit.html', {'form': context} | all_popular())
    settings.profile_edit(request)
    return redirect(reverse('profile', kwargs={'profile_id': request.user.profile.id}))


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def follows(request):
    context = settings.follows(request)
    return render(request, 'follows.html', context | all_popular())


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def my_questions(request):
    context = settings.my_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'my_questions.html', context | all_popular())


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def my_answers(request):
    context = settings.my_answers(request)
    return render(request, 'my_answers.html', context | all_popular())


@csrf_protect
@login_required
def like(request):
    count = settings.like(request)
    return JsonResponse({'count': str(count)})


@csrf_protect
@login_required
def ban_answer(request):
    settings.ban_answer(request)
    return JsonResponse({'result': 'success'})


@csrf_protect
@login_required
def delete_something(request):
    settings.delete_something(request)
    return JsonResponse({'result': 'success'})
