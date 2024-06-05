from django.urls import path
from rest_framework.routers import DefaultRouter

from lms import views
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'lms', views.CourseViewSet, basename='lms')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson-delete'),
] + router.urls
