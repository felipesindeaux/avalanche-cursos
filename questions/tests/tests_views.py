from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class AnswerTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.question_data = {
            "title": "Titulo",
            "description": "Description",
            "categories": [{"name": "teste"}],
        }

        cls.user_data = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_data = Token.objects.create(user=cls.user_data)

        cls.user_data_wrong = User.objects.create(
            email="teste2@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_data_wrong = Token.objects.create(user=cls.user_data_wrong)

    def test_create_question(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        response = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("answers_count", response.data)
        self.assertIn("date_published", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("categories", response.data)

    def test_create_question_with_invalid_value(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        self.question_data["categories"] = ""

        response = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categories", response.data)

    def test_list_question_created(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)


        self.client.post("/api/questions/",
                         data=self.question_data, format="json")


        response = self.client.get("/api/questions/?page=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data["results"]))

    def test_list_question_created_by_id(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        question = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data_wrong.key)

        response = self.client.get(f"/api/questions/{question.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], question.data["id"])

    def test_list_question_created_wrong_uuid(self):

        response = self.client.get(f"/api/questions/0/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_question(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        question = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        response = self.client.patch(
            f"/api/questions/{question.data['id']}/", data={"title": "boa tarde"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertEqual("boa tarde", response.data["title"])
        self.assertNotEqual(
            response.data["date_published"], response.data["updated_at"]
        )

    def test_update_question_not_be_owner(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        question = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data_wrong.key)

        response = self.client.patch(
            f"/api/questions/{question.data['id']}/", data={"title": "boa tarde"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_question_be_onwer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        question = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        response = self.client.delete(f"/api/questions/{question.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_delete_question_not_be_onwer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        question = self.client.post(
            "/api/questions/", data=self.question_data, format="json"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data_wrong.key)

        response = self.client.delete(f"/api/questions/{question.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
