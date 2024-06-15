from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='ТестКурс', owner=self.user)
        self.lesson = Lesson.objects.create(name='ТестУрок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('lms:lesson-create')
        data = {
            'name': 'ТестУрок2',
            'course': self.course.id,
            'owner': self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:lesson-update', args=(self.lesson.pk,))
        data = {
            'name': 'ТестУрок2 + редактирование',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'ТестУрок2 + редактирование')

    def test_lesson_destroy(self):
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('lms:lesson-list')
        response = self.client.get(url)
        data = response.json()
        sample = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "link_to_video": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, sample)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='ТестКурс', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("users:subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": 'подписка добавлена'})

    def test_unsubscribe(self):
        url = reverse("users:subscription")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'подписка удалена'})


# class CourseTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(email='test@test.ru')
#         self.course = Course.objects.create(name='ТестКурс', owner=self.user)
#         self.lesson = Lesson.objects.create(name='ТестУрок', course=self.course, owner=self.user)
#         self.client.force_authenticate(user=self.user)
#
#     def test_course_retrieve(self):
#         url = reverse('lms:course-detail', args=(self.course.pk,))
#         response = self.client.get(url)
#         data = response.json()
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get('name'), self.course.name)
#
#     def test_course_create(self):
#         url = reverse('lms:course-list')
#         data = {
#             'name': 'ТестКурс2',
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Course.objects.all().count(), 2)
