from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Course, Lesson
from users.models import User


@shared_task
def send_email_of_updates(email, pk, model):
    """Отправляет письмо об обновлении курса/урока"""

    now = timezone.now()

    if model == 'Lesson':
        material = Lesson.objects.filter(pk=pk).first()
        material_name = 'урок'
    else:
        material = Course.objects.filter(pk=pk).first()
        material_name = 'курс'

    send_mail(
        subject=f'Обновление {material_name}а',
        message=f'Обновились материалы {material_name}а: "{material.name}"',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    material.update = now
    material.save()


@shared_task
def user_deactivation_by_time():
    """Деактивация пользователя, если он не входил более 30 дней"""

    now = timezone.now()
    users = User.objects.all()

    for user in users:
        if user.is_active and now - user.last_login.days > 30:
            user.is_active = False
            user.save()
