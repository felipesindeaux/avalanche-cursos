from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = {
            "name": "aluno",
            "email": "aluno2@mail.com",
            "password": "123",
            "is_teacher": True
        }

    def test_register_user_success(self):
        res = self.client.post("/api/register/", data=self.user)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

    def test_register_user_missing_keys(self):
        res = self.client.post("/api/register/", data={})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)
        self.assertIn("name", res.data)
        self.assertIn("email", res.data)
