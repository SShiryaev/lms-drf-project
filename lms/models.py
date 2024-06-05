from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """Модель курса lms. Связанна с моделью Lesson отношением One to many"""

    name = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to='lms/course/', **NULLABLE, verbose_name='превью')
    description = models.TextField(max_length=500, **NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'Курс: {self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Модель урока lms. Имеет внешний ключ на модель Course"""

    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(max_length=500, **NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='lms/lesson/', **NULLABLE, verbose_name='превью')
    link_to_video = models.CharField(max_length=200, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')

    def __str__(self):
        return f'Урок: {self.name} курса: {self.course}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
