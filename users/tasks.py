from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Lesson


@shared_task
def send_email_of_updates(email, pk, model):
    """Отправляет письмо об обновлении курса/урока"""

    today = timezone.now()

    if model == 'Lesson':
        instance = Lesson.objects.filter(pk=pk).first()
        instance_name = 'урок'
    elif model == 'Course':
        instance = Course.objects.filter(pk=pk).first()
        instance_name = 'курс'

    send_mail(
        subject=f'Обновление {instance_name}а',
        message=f'Обновились материалы {instance_name}а: "{instance.name}"',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    instance.update = today
    instance.save()
