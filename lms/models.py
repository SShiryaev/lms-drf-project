from django.db import models
from config.settings import AUTH_USER_MODEL

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """
    Модель курса lms. Связанна с моделями Lesson, Payments, Subscription отношением One to many.
    Имеет внешний ключ на модель User (AUTH_USER_MODEL).
    """

    name = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to='lms/course/', **NULLABLE, verbose_name='превью')
    description = models.TextField(max_length=500, **NULLABLE, verbose_name='описание')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')
    update = models.DateTimeField(**NULLABLE, verbose_name='дата обновления')

    def __str__(self):
        return f'Курс: {self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    Модель урока lms.
    Имеет внешний ключ на модели Course, User.
    Связанна с моделью Payments отношением One to many.
    """

    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(max_length=500, **NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='lms/lesson/', **NULLABLE, verbose_name='превью')
    link_to_video = models.CharField(max_length=200, **NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')
    update = models.DateTimeField(**NULLABLE, verbose_name='дата обновления')

    def __str__(self):
        return f'Урок: {self.name} курса: {self.course}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
