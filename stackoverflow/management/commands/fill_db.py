from django.core.management.base import BaseCommand
from stackoverflow.models import Profile, Question, Answer, Tag, AnswerLikes, QuestionLikes
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone


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
        for q in Question.objects.all():
            if q.tags.count() == 0:
                q.delete()
        return
        print('Generate users?')
        if input() == 'yes':
            for i in range(9957, ratio + 1):
                u = User.objects.create_user(username=get_rand_str(5, 9),
                                             password=get_rand_str(5, 7),
                                             email=get_rand_str(3, 4) + '@gmail.com',
                                             first_name=get_rand_str(2, 4, False),
                                             last_name=get_rand_str(2, 4, False),
                                             date_joined=timezone.now())
                Profile.objects.create(user=u, avatar='acc.png')
            print('Created profiles')
        print('Generate tags?')
        if input() == 'yes':
            for i in range(1, ratio + 1):
                Tag.objects.create(tag_name=get_rand_str(1, 4, False))
            print('Created tags')
        print('Generate questions?')
        if input() == 'yes':
            profiles = Profile.objects.all()
            tags = Tag.objects.all()
            for i in range(1, ratio * 10 + 1):
                if i % 10000 == 0:
                    print(i)
                q = Question.objects.create(
                             title=get_rand_str(3, 8, False, True),
                             description=get_rand_str(5, 10, True, True),
                             date=timezone.now(),
                             rating=0,
                             author_id=profiles[i % ratio]
                             )
                for j in range(1, 3):
                    q.tags.add(tags[(i + j) % ratio])
            print('Created questions')
        print('Generate answers?')
        if input() == 'yes':
            questions = Question.objects.all()
            profiles = Profile.objects.all()
            for i in range(164949, ratio * 100 + 1):
                if i % 10000 == 0:
                    print(i)
                Answer.objects.create(description=get_rand_str(2, 6, True, True),
                                      date=timezone.now(),
                                      question=questions[i % ratio],
                                      author=profiles[i % ratio],
                                      rating=0
                                      )
            print('Created answers')
        print('Generate answerlikes?')
        if input() == 'yes':
            answers = Answer.objects.all()
            profiles = User.objects.all()
            for i in range(1, ratio * 150 + 1):
                if i % 10000 == 0:
                    print(i)
                AnswerLikes.objects.toggleLike(user_id=profiles[i % ratio], answer_id=answers[i % ratio])
            print('Created answerlikes')
        print('Generate questionlikes?')
        if input() == 'yes':
            questions = Question.objects.all()
            profiles = User.objects.all()
            for i in range(1, ratio * 150 + 1):
                if i % 10000 == 0:
                    print(i)
                QuestionLikes.objects.toggleLike(user_id=profiles[i % ratio], question_id=questions[i % ratio])
            print('Created questionlikes')