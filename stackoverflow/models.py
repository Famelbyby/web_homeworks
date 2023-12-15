from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


# Create your models here.

class ProfileQuerySet(models.QuerySet):

    def toggleFollow(self, user_whome, profile_who_id):
        profile_who = self.get(pk=profile_who_id)
        profile = self.get(user=user_whome)
        if profile.follows.filter(user=profile_who.user).count() > 0:
            profile.follows.remove(profile_who)
        else:
            profile.follows.add(profile_who)


class ProfileManager(models.Manager):

    def get_query_set(self):
        return ProfileQuerySet(self.model, using=self._db)

    def toggleFollow(self, user_whome, profile_who_id):
        return self.get_query_set().toggleFollow(user_whome, profile_who_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default='ava.png', blank=True)
    follows = models.ManyToManyField('Profile')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class TagQueryset(models.QuerySet):
    def isThisTag(self, thisTag):
        return self.get(tag_name=thisTag)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQueryset(self.model, using=self._db)

    def isThisTag(self, thisTag):
        return self.get_queryset().isThisTag(thisTag)


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


class QuestionQueryset(models.QuerySet):
    def hot(self):
        return self.order_by('-rating')

    def newer(self):
        return self.order_by('-date')


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQueryset(self.model, using=self._db)

    def hot(self):
        return self.get_queryset().hot()

    def newer(self):
        return self.get_queryset().newer()


class Question(models.Model):
    title = models.TextField(max_length=30)
    description = models.TextField()
    date = models.DateField()
    rating = models.IntegerField(default=0)
    author_id = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    description = models.TextField()
    date = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.description


class QuestionLikesQuerySet(models.QuerySet):

    def toggleLike(self, user_id, question_id):
        try:
            self.get(user_id=user_id, question_id=question_id).delete()
        except:
            self.create(user_id=user_id, question_id=question_id)


class QuestionLikesManager(models.Manager):

    def get_query_set(self):
        return QuestionLikesQuerySet(self.model, using=self._db)

    def toggleLike(self, user_id, question_id):
        self.get_query_set().toggleLike(user_id, question_id=question_id)


class QuestionLikes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = QuestionManager()


class AnswerLikesQuerySet(models.QuerySet):

    def toggleLike(self, user_id, question_id):
        try:
            self.get(user_id=user_id, question_id=question_id).delete()
        except:
            self.create(user_id=user_id, question_id=question_id)


class AnswerLikesManager(models.Manager):

    def get_query_set(self):
        return AnswerLikesQuerySet(self.model, using=self._db)

    def toggleLike(self, user_id, question_id):
        self.get_query_set().toggleLike(user_id, question_id=question_id)


class AnswerLikes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = AnswerLikesManager()
