from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Модель пользователя с наследованием от AbstractUser, исключением поля username
    и переопределением USERNAME_FIELD на поле email.
    Связанна с моделями Payments, Course, Lesson, Subscription отношением One to many.
    """

    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=30, **NULLABLE, verbose_name='телефон')
    town = models.CharField(max_length=50, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'Пользователь ({self.email})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    """Модель платежа. Имеет внешний ключ на модели User, Course, Lesson."""

    # Сопоставление или итерация для использования в качестве вариантов для поля method.
    METHOD_CHOICES = {
        'TRANSFER': 'Перевод на счет',
        'CASH': 'Наличные',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.SET_NULL, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, **NULLABLE, on_delete=models.SET_NULL, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="сумма оплаты")
    method = models.CharField(max_length=15, choices=METHOD_CHOICES, default='TRANSFER', verbose_name="Способ оплаты")

    def __str__(self):
        return (f'{self.user} оплатил {self.course if self.course else self.lesson}, датой {self.date},'
                f'на сумму {self.amount}, методом {self.method}.')

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-date',]


class Subscription(models.Model):
    """Модель подписки на обновления курса. Имеет внешний ключ на модели User, Course."""

    is_subscribed = models.BooleanField(default=True, verbose_name='подписан')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
