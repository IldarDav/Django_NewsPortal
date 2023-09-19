from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import PostCategory, Post


def send_notifications(preview, pk, header, subscribers):
    html_content = render_to_string(
        'new_post_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email='ildardave@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.header, subscribers)


def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать на новостной портал!'
        message = f"Добро пожаловать, {instance.username}!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])


@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(sender, instance, created, **kwargs)


@receiver(m2m_changed, sender=PostCategory)
def weekly_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.category.all()
        subscribers_emails: list[str] = []
        for category in categories:
            subscribers_emails += category.subscribers.all()

            subscribers_emails = [s.email for s in subscribers_emails]

        send_notifications(instance.preview(), instance.pk, instance.headline, subscribers_emails)
