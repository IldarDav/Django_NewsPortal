from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'header', 'post_text']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        send_mail(
            subject=user.username,
            message='Вы успешно зарегистрировались',
            from_email='ildardave@yandex.ru',
            recipient_list=[user.email]
        )
        return user

