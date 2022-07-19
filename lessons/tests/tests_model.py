from courses.models import Course
from django.test import TestCase
from lessons.models import Lesson
from users.models import User


class LessonTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_data = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.user = User.objects.get(pk=cls.user_data.id)

        cls.course_data = {
            "title": "titulo do curso teste",
            "description": "descricao do curso teste kk",
            "price": 1.99,
            "total_hours": 12
        }

        cls.course = Course.objects.create(**cls.course_data, owner=cls.user)

        cls.lesson_data = {
            "title": "lição teste",
            "description": "lição teste descricao"
        }

    def test_creation_of_lesson(self):
        lesson = Lesson.objects.create(**self.lesson_data, course=self.course)

        lesson.save()

        self.assertIn("course_id", lesson.__dict__)
        self.assertEqual(self.course.id, lesson.course_id)

    def test_is_active_by_default(self):
        lesson = Lesson.objects.create(**self.lesson_data, course=self.course)

        lesson.save()

        self.assertIn("is_active", lesson.__dict__)
        self.assertTrue(lesson.is_active)
