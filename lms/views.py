from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


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


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner,)
    queryset = Lesson.objects.all()
