from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""

    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        model = Lesson
        fields = '__all__'
