from datetime import datetime
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from .models import PostCategory
from .tasks import subsribed_mail_send_task

# короче надо со временем связывать, иначе никак
@receiver(m2m_changed, sender=PostCategory)
def subsribed_mail_send_signal(instance, **kwargs):
    if kwargs.get('action') != 'post_add':
        return
    subsribed_mail_send_task.delay(instance.pk)