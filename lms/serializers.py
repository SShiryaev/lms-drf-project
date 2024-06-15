from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import LinkToVideoValidator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkToVideoValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True)
    subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    def get_subscription(self, instance):
        return Subscription.objects.filter(course=instance).exists()

    class Meta:
        model = Course
        fields = '__all__'
