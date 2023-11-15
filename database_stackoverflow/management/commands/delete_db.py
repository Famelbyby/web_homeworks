from django.core.management.base import BaseCommand
from database_stackoverflow.models import Profile, Question, Answer, Tag
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Enter ratio'

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
