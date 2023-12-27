from django.core.management.base import BaseCommand
from django.db.models import Count
from stackoverflow.models import Profile, Question, Answer, Tag, AnswerLikes, QuestionLikes
from django.contrib.auth.models import User
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Enter ratio'

    def handle(self, *args, **options):
        cache_key_tags = 'popular_tags'
        tags = Tag.objects.all().annotate(Count('questions')).order_by('-questions__count')[:10]
        cache.set(cache_key_tags, tags, 60 * 60 * 24 * 90)
