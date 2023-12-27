from django.core.management.base import BaseCommand
from django.db.models import Count
from stackoverflow.models import Profile, Question, Answer, Tag, AnswerLikes, QuestionLikes
from django.contrib.auth.models import User
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Enter ratio'

    def handle(self, *args, **options):
        cache_key_profiles = 'popular_profiles'
        users = sorted([[QuestionLikes.objects.filter(user_id=i).count() +
                         AnswerLikes.objects.filter(user_id=i).count(), i.id] for i in User.objects.all()],
                       reverse=True)[:10]
        profiles = [Profile.objects.get(user_id=i[1]) for i in users]
        cache.set(cache_key_profiles, profiles, 60 * 60 * 24 * 7)
