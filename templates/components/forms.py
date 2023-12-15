from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from database_stackoverflow.models import Profile, Question, Tag, Answer


class LoginForm(forms.ModelForm):
    password = forms.CharField(min_length=4)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        try:
            username = self.clean_password.get('username')
            user = User.objects.get(username=username)
            return user
        except:
            raise ValidationError('There is no selected user')

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.get(username=username)
        if user.password != password:
            raise ValidationError('Password is incorrect')
        return password


class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=5)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=4)
    repeat_password = forms.CharField(min_length=4)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise ValidationError('This email already exists')
        return email

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password')
        password = self.cleaned_data.get('password')
        if password != repeat_password:
            raise ValidationError('Password must be similar')
        return repeat_password

    def save(self, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        avatar = self.cleaned_data.get('avatar')
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('This user already exists')
        user = User.objects.create(username=username, first_name=first_name,
                                   last_name=last_name, email=email, password=password)
        Profile.objects.create(user=user, avatar=avatar)
        return user


class EditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AskQuestion(forms.ModelForm):
    title = forms.CharField(min_length=3, max_length=30)
    tags = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def save(self, **kwargs):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        tags = self.cleaned_data.get('tags').split(' ')
        date = timezone.now()
        question = Question.objects.create(title=title, description=description, date=date)
        for t in tags:
            question.tags.add(t)
        return question


class GiveAnswer(forms.ModelForm):
    description = forms.CharField(required=True)

    class Meta:
        model = Answer
        fields = ['description']

    def save(self, **kwargs):
        description = self.cleaned_data.get('description')
        answer = Answer.objects.create(description=description)
        return answer
