from django.core.management.base import BaseCommand
from stackoverflow.models import Profile, Question, Answer, Tag, AnswerLikes, QuestionLikes
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Enter ratio'

    def handle(self, *args, **options):
        print(f'Tags: {Tag.objects.all().count()}')
        print(f'Answers: {Answer.objects.all().count()}')
        print(f'Questions: {Question.objects.all().count()}')
        print(f'Profiles: {Profile.objects.all().count()}')
        print(f'Likes: {AnswerLikes.objects.all().count() + QuestionLikes.objects.all().count()}')