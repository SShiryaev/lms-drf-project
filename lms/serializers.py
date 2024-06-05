from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        model = Lesson
        fields = '__all__'
