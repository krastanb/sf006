from celery import shared_task
import time
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Subscription, User, Post
from datetime import datetime, timedelta, timezone
from django.template.loader import render_to_string


@shared_task
def hello():
    for i in range(10):
        time.sleep(1)
        print(i)

@shared_task
def subsribed_mail_send_task(instancepk):
    instance = Post.objects.get(pk=instancepk)
    timecreate = instance.time_create.replace(tzinfo=None)
    if ((datetime.utcnow()-timecreate).total_seconds())<1:
        users_id = Subscription.objects.filter(category__in=instance.category.all()).values_list('user', flat=True)
        users = User.objects.filter(pk__in=users_id)
        for user in users:
            if user.email != '':
                subj = 'Новая новость из Вашего любимого!'
                text = f'{user.username} у Ваших любимых категорий появилась новая новость!'
                html = f'{user.username}, у Ваших любимых категорий появилась новая <a href="{settings.SITE_URL}{instance.get_absolute_url()}">новость</a>!'
                msg = EmailMultiAlternatives(subject=subj, body=text, from_email=settings.EMAIL_HOST_USER,
                                             to=[user.email])
                msg.attach_alternative(html, 'text/html')
                msg.send()

@shared_task
def every_week_mails():
    print('процесс запущен')
    time.sleep(5)
    print('процесс окончен')