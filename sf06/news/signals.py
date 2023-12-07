from datetime import datetime
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post, Category, PostCategory, Subscription, User

# короче надо со временем связывать, иначе никак
@receiver(m2m_changed, sender=PostCategory)
def subsribed_mail_send(instance, **kwargs):
    if kwargs.get('action')!='post_add':
        return
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






