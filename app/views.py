from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from app import settings


# Create your views here.

@login_required(login_url='login', redirect_field_name='continue')
def index(request):
    context = settings.index_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def hot(request):
    context = settings.hot_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('404 Error')
    return render(request, 'index.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def tag(request, tag_name):
    context = settings.tag_questions(request, tag_name)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', context)


@login_required
def query_question(request, query_name):
    context = settings.query_question(request, query_name)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'index.html', context)

@csrf_protect
def log_in(request):
    form = settings.login_user(request)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, **form.cleaned_data)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('continue', '/'))
        form.add_error('password', 'Password is incorrect')
    return render(request, 'login.html', {'form': form})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def question(request, question_id):
    if request.method == 'GET':
        context = settings.certain_question(request, question_id)
        if context['page'] == -1:
            return HttpResponseNotFound('Bad request')
        context['form'] = settings.give_answer(request, question_id)
        return render(request, 'question.html', context)
    [count, answer_id] = settings.give_answer(request, question_id)
    return redirect(reverse('question', kwargs={'question_id': question_id}) +
                    '?page=' + str(count) + '#' + str(answer_id))


@csrf_protect
def signup(request):
    form = settings.signup(request)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(reverse('index'))
    return render(request, 'signup.html', {'form': form})


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
    return render(request, 'ask.html', {'form': form})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def profile(request, profile_id):
    if request.method == 'POST':
        settings.follow(request, profile_id)
        return redirect(request.META.get('HTTP_REFERER'))
    [context, isFollowed] = settings.profile(request, profile_id)
    if context == -1:
        return HttpResponseNotFound('404 Not found')
    return render(request, 'profile.html', {'profile': context, 'isFollowed': isFollowed})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def profile_edit(request):
    if request.method == 'GET':
        context = settings.profile_edit(request)
        return render(request, 'profile_edit.html', {'form': context})
    settings.profile_edit(request)
    return redirect(reverse('profile', kwargs={'profile_id': request.user.profile.id}))


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def follows(request):
    context = settings.follows(request)
    return render(request, 'follows.html', context)


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def my_questions(request):
    context = settings.my_questions(request)
    if context['page'] == -1:
        return HttpResponseNotFound('Bad request')
    return render(request, 'my_questions.html', context)


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def my_answers(request):
    context = settings.my_answers(request)
    return render(request, 'my_answers.html', context)


@csrf_protect
@login_required
def like(request):
    count = settings.like(request)
    return JsonResponse({'count': str(count)})


@csrf_protect
@login_required
def ban_answer(request):
    settings.ban_answer(request)
    return JsonResponse({})


@csrf_protect
@login_required
def delete_something(request, type_query, delete_id):
    settings.delete_something(type_query, delete_id)
    return redirect(request.META.get('HTTP_REFERER'))