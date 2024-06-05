from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from lms.serializers import CourseSerializer, LessonSerializer
from lms.models import Course, Lesson


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

