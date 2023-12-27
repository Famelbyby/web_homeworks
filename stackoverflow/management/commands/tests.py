import random
from unittest import TestCase

import requests
from django.utils import timezone

from stackoverflow.models import Question

# Create your tests here.
params = {'csrftoken': 'SOWSApJ4L8vuT9os0JjtaQNuJ3HxrZ3S',
          'sessionid': '5m4beck7lz82f4itb9byp8ykirvwvhne'}

from django.core.management.base import BaseCommand
from stackoverflow.models import Profile, Question, Answer, Tag, AnswerLikes, QuestionLikes
from django.contrib.auth.models import User


def get_rand_tag():
    st = 'qwertyuiopasdfghjklzxcvbnm'
    s = ''
    for i in range(5):
        s += random.choice(st)
    return s


class ProfilesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_if_exists_question(self):
        q_id = int(random.random() * 1000000)
        resp = requests.get(f'http://127.0.0.1:8000/question/{q_id}', cookies=params)
        self.assertEqual(resp.status_code == 200, Question.objects.filter(pk=q_id).count() > 0,
                         'There is no selected question!')

    def test_if_exists_tag(self):
        tag_id = get_rand_tag()
        resp = requests.get(f'http://127.0.0.1:8000/tag/{tag_id}', cookies=params)
        self.assertEqual(resp.status_code == 200, Tag.objects.filter(tag_name=tag_id).count() > 0,
                         'There is no selected tag!')

    def test_if_exists_profile(self):
        p_id = int(random.random() * 50000)
        resp = requests.get(f'http://127.0.0.1:8000/profile/{p_id}', cookies=params)
        self.assertEqual(resp.status_code == 200, Profile.objects.filter(pk=p_id).count() > 0,
                         'There is no selected profile!')

    def test_if_no_cookie(self):
        resp = requests.get('http://127.0.0.1:8000/profile/edit')
        self.assertNotEqual(resp.url, 'http://127.0.0.1:8000/profile/edit'
                                      'You can\' edit without cookie!')

    def test_if_asks(self):
        ask_answer = {'id_title': f'Last question{timezone.now()}', 'id_description': 'Something',
                      'id_tags': 'Last YAIP'}
        resp = requests.post('http://127.0.0.1:8000/ask', data=ask_answer, cookies=params)
        self.assertNotEqual(Question.objects.last().title, f'Last question{timezone.now()}',
                            'Wrong title!')

    def test_if_answers(self):
        q_id = 120571
        question = Question.objects.get(pk=q_id)
        give_answer = {'id_description': 'Nothing'}
        resp = requests.post(f'http://127.0.0.1:8000/question/{q_id}', data=give_answer, cookies=params)
        self.assertNotEqual(question.answer_set.all().last().description, 'Nothing',
                            'Wrong description!')


class Command(BaseCommand):
    help = 'Enter ratio'

    def handle(self, *args, **options):
        p = ProfilesTest()
        for i in range(1, 1001):
            p.test_if_exists_question()
            p.test_if_exists_profile()
            p.test_if_exists_tag()
            p.test_if_no_cookie()
            p.test_if_asks()
            p.test_if_answers()
            print(f'Test suite {i}... ok')
