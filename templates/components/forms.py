from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from stackoverflow.models import Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_username(self):
        try:
            username = self.cleaned_data.get('username')
            user = User.objects.get(username=username)
            return user
        except:
            raise ValidationError('There is no selected user')

    def save(self, **kwargs):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=5)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeat_password', 'first_name', 'last_name']

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
        self.cleaned_data.pop('repeat_password')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        avatar = self.cleaned_data.get('avatar')
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('This user already exists')
        user = User.objects.create_user(username=username, first_name=first_name,
                                        last_name=last_name, email=email, password=password)
        Profile.objects.create(user=user, avatar=avatar)
        return user


class EditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def save(self, **kwargs):
        user = super().save(**kwargs)
        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')
        if received_avatar:
            profile.avatar = received_avatar
            profile.save()
        return user


class AskQuestion(forms.ModelForm):
    title = forms.CharField(min_length=3, max_length=30)
    description = forms.CharField(widget=forms.Textarea)
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
            try:
                question.tags.add(Tag.objects.get(tag_name=t))
            except:
                question.tags.add(Tag.objects.create(tag_name=t))
        return question


class GiveAnswer(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ['description']

    def save(self, **kwargs):
        description = self.cleaned_data.get('description')
        answer = Answer.objects.create(description=description, date=timezone.now())
        return answer
