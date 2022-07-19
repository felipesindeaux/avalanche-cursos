from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from users.serializers import UserSerializer


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "name": "prof",
            "email": "prof2@mail.com",
            "password": "1234",
            "is_teacher": True,
        }

        cls.user = User.objects.create_user(**cls.user_data)

        cls.token_user = Token.objects.create(user=cls.user)

        cls.user_data_to_create = {
            "name": "newuser",
            "email": "newuser@mail.com",
            "password": "1234",
            "is_teacher": True,
        }

        cls.super_data = {
            "name": "super",
            "email": "super2@mail.com",
            "password": "1234",
        }

        cls.super = User.objects.create_superuser(**cls.super_data)

        cls.token_super = Token.objects.create(user=cls.super)

    def test_register_user_success(self):
        res = self.client.post("/api/register/", data=self.user_data_to_create)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

    def test_register_user_missing_keys(self):
        res = self.client.post("/api/register/", data={})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)
        self.assertIn("name", res.data)
        self.assertIn("email", res.data)

    def test_list_all_users_without_permission(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user.key)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.data,
        )

    def test_list_all_users(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_super.key)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(2, len(response.data))

    def test_retrieve_my_user_without_token(self):

        response = self.client.get(f"/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.data
        )

    def test_retrieve_my_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user.key)
        response = self.client.get(f"/api/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.user.id))

        self.assertEqual(UserSerializer(
            instance=self.user).data, response.data)

    def test_update_my_user_without_token(self):

        newName = {"name": "newname"}
        response = self.client.patch(f"/api/users/me/", data=newName)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.data
        )

    def test_update_my_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_user.key)
        newName = {"name": "newname"}
        response = self.client.patch(f"/api/users/me/", data=newName)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": str(self.user.id),
                "name": newName["name"],
                "email": self.user.email,
                "is_teacher": self.user.is_teacher,
            },
        )
