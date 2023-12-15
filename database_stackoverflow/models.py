from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, QuerySet


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default='ava.png', blank=True)
    follows = models.ManyToManyField('Profile')

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
    question_id = models.IntegerField(primary_key=True)
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
    answer_id = models.IntegerField(primary_key=True)
    description = models.TextField()
    date = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.description


class QuestionLikes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerLikes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_id = models.ForeignKey(Answer, on_delete=models.CASCADE)
