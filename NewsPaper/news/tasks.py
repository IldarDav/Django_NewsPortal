import datetime

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from NewsPaper.settings import DEFAULT_FROM_EMAIL
from .models import Post, Category


@shared_task
def weekly_sending():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(data__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        "weekly_post.html",
        {
            'link': settings.SITE_URL,
            'posts': posts
        }

    )

    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.header
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'new_post_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
