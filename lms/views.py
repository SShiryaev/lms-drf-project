from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lms.models import Course, Lesson
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.models import Subscription
from users.permissions import IsModerator, IsOwner
from users.tasks import send_email_of_updates


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator)
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, ~IsModerator,)
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def patch(self, request, *args, **kwargs):
        # Получаем текущее время
        now = timezone.now()
        # Получаем пользователя
        user = self.request.user
        # Получаем id урока
        lesson_id = kwargs.get('pk')

        # Получаем объект урока из базы данных
        lesson_item = generics.get_object_or_404(Lesson, pk=lesson_id)

        # Получаем объект курса в составе которого находится урок у текущего пользователя
        course_item = Course.objects.filter(owner=user, lesson=lesson_id).first()

        # Получаем объект подписки по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Уведомление отправляется только в том случае, если курс не обновлялся более четырех часов
        if subs_item.exists():
            if now - course_item.update.hours >= 4:
                send_email_of_updates.delay(user.email, lesson_item.pk, 'Lesson')
                message = f'Урок "{lesson_item.name}" обновлен'
            else:
                message = f'Курс с уроком "{lesson_item.name}" обновлялся менее четырех часов назад'
        else:
            message = 'Урок обновлен без подписки'

        # Возвращаем ответ в API
        return Response({"message": message})


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner,)
    queryset = Lesson.objects.all()
