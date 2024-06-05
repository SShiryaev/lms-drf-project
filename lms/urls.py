from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'lms', CourseViewSet, basename='lms')

urlpatterns = [

] + router.urls
