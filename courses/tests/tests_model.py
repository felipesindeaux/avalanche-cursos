from datetime import datetime as dt

from categories.models import Category
from courses.models import Course
from django.test import TestCase
from users.models import User


class CourseTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user_data = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )
        Category.objects.create(name="TEST")

        cls.user = User.objects.get(pk=cls.user_data.id)
        cls.category = Category.objects.all()

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 1.555,
            "total_hours": 12,
        }

    def test_owner_of_course(self):
        course = Course.objects.create(**self.course_data, owner=self.user)
        course.categories.set(self.category)

        course.save()

        self.assertIn("owner_id", course.__dict__)
        self.assertEqual(self.user.id, course.owner_id)

    def test_is_active_default_of_course(self):
        course = Course.objects.create(**self.course_data, owner=self.user)
        course.categories.set(self.category)

        course.save()

        self.assertIn("is_active", course.__dict__)
        self.assertTrue(course.is_active)

    def test_price_of_course(self):
        course = Course.objects.create(**self.course_data, owner=self.user)
        course.categories.set(self.category)

        course.save()

        date_now = dt.strftime(dt.now(), "%D")
        date_model = dt.strftime(course.date_published, "%D")

        self.assertEqual(date_now, date_model)
