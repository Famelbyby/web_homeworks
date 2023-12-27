import random

from django.test import TestCase
import requests

from stackoverflow.models import Question

# Create your tests here.
params = {'csrftoken': '8MF6hDLNiMZOzf86bHj9pKCcTNMTVoEP',
          'sessionid': 'pmc7hbjmle2x2zefcdemtpbhjeaqji1k'}


class ProfilesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_if_exists(self):
        q_id = int(random.random() * 1000000)
        print(q_id)
        resp = requests.get(f'http://127.0.0.1:8000/question/{q_id}', cookies=params)
        self.assertEqual(resp.status_code == 200, Question.objects.filter(pk=q_id).count() > 0,
                         'There is no selected profile!')


p = ProfilesTest()
p.test_if_exists()
