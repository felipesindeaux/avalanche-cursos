import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from categories.models import Category
from courses.models import Course

from users.models import User


class TestCourseViewsByTeacher(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
            "categories": [{"name": "Node"}],
        }

        cls.user_teacher = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_teacher = Token.objects.create(user=cls.user_teacher)

    def test_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            "/api/courses/", data=self.course_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("categories", response.data)

    def test_create_course_with_invalid_price(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        self.course_data["price"] = 1.222

        response = self.client.post(
            "/api/courses/", data=self.course_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_list_course_created(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)
        self.client.post("/api/courses/", data=self.course_data, format="json")

        response = self.client.get("/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))


class TestCourseViewsByStudent(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
        }

        cls.user_teacher = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.user_student = User.objects.create(
            email="teste2@mail.com", name="teste", password="123", is_teacher=False
        )

        # cls.token_teacher = Token.objects.create(user=cls.user_teacher)
        cls.token_student = Token.objects.create(user=cls.user_student)

        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()

        cls.course = Course.objects.create(**cls.course_data, owner=cls.user_teacher)
        cls.course.categories.set(cls.category)
        cls.course.save()

        cls.course_deactive = Course.objects.create(
            **cls.course_data, is_active=False, owner=cls.user_teacher
        )
        cls.course_deactive.categories.set(cls.category)
        cls.course_deactive.save()

    def test_list_valid_course(self):
        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_course_bought(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get("/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
