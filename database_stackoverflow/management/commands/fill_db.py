from django.core.management.base import BaseCommand
from database_stackoverflow.models import Profile, Question, Answer, Tag
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
from django.db.models import Max


def get_rand_str(my_len_st, my_len_end, withDigits=True, withSpace=False):
    alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    if withDigits:
        alphabet += '1234567890'
    if withSpace:
        alphabet += ' .,!?'
    s = ''
    for i in range(randint(my_len_st, my_len_end)):
        s += alphabet[randint(0, len(alphabet) - 1)]
    return s


class Command(BaseCommand):
    help = 'Enter ratio'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs=1, type=int)

    def handle(self, *args, **options):
        ratio = options['ratio'][0]
        for i in range(1, ratio + 1):
            u = User(id=i,
                     username=get_rand_str(10, 20),
                     password=get_rand_str(5, 15),
                     email=get_rand_str(6, 10) + '@gmail.com',
                     date_joined=timezone.now())
            u.save()
            Profile.objects.create(id=i, user=u, rating=randint(1, 10000), avatar='acc.png')
        print('Created profiles')
        for i in range(1, ratio + 1):
            Tag.objects.create(id=i,
                               tag_name=get_rand_str(2, 12, False))
        print('Created tags')
        for i in range(1, ratio * 10 + 1):
            q = Question(question_id=i,
                         title=get_rand_str(10, 30, False, True),
                         description=get_rand_str(10, 40, True, True),
                         date=timezone.now(),
                         rating=randint(0, 100000),
                         author_id=Profile.objects.all()[randint(0, ratio - 1)]
                         )
            q.save()
            for i in range(randint(1, 3)):
                q.tags.add(Tag.objects.all()[randint(0, ratio - 1)])
        print('Created questions')
        for i in range(1, ratio * 100 + 1):
            if i % 10000 == 0:
                print(i)
            Answer.objects.create(answer_id=i,
                                  description=get_rand_str(1, 50, True, True),
                                  date=timezone.now(),
                                  question_id=Question.objects.all()[randint(0, ratio * 10 - 1)],
                                  author_id=Profile.objects.all()[randint(0, ratio - 1)],
                                  rating=randint(0, ratio - 1)
            )
        print('Created answers')

