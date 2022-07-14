import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status

from users.models import User


class TestCourseViews(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
            "categories": [{"name": "Node"}]
        }

        cls.user = User.objects.create(
            email="teste@mail.com",
            name="teste",
            password="123",
            is_teacher=True
        )
        
        cls.token_client = Token.objects.create(user=cls.user)


    def test_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_client.key)

        response = self.client.post("/api/courses/", data=self.course_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("categories", response.data)

    def test_create_course_with_invalid_price(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_client.key)

        self.course_data["price"] = 1.222

        response = self.client.post("/api/courses/", data=self.course_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)