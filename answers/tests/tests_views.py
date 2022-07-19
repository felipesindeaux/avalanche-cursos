from categories.models import Category
from questions.models import Question
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class AnswerTestView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.question_data = {
            "title": "Titulo",
            "description": "Description",
        }

        cls.question = Question.objects.create(
            **cls.question_data, user=cls.user)

        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()
        cls.question.categories.set(cls.category)
        cls.question.save()

        cls.answer_data = {"content": "Resposta Teste"}

        cls.token_data = Token.objects.create(user=cls.user)

        cls.user_wrong = User.objects.create(
            email="teste.teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_data_wrong = Token.objects.create(user=cls.user_wrong)

    def test_create_answer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        response = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("content", response.data)
        self.assertIn("date_published", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("question_id", response.data)
        self.assertIn("user_id", response.data)

    def test_create_question_with_invalid_value(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        self.answer_data["content"] = ""

        response = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)

    def test_list_answer_created(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        response = self.client.get(
            f"/api/questions/{self.question.id}/answers/")

        # está retornando um warning, não achei nada que eu possa resolver isto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_answer_created_with_wrong_question_uuid(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        ID = "55aa248a-ad0b-4558-a3b2-c4b62ce08b97"

        self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        response = self.client.get(f"/api/questions/{ID}/answers/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_answer_question_created(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        answer = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        response = self.client.get(
            f"/api/questions/answers/{answer.data['id']}/")
        # está retornando um warning, não achei nada que eu possa resolver isto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], answer.data['id'])

    def test_list_answer_question_created_with_wrong_uuid(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        ID = "55aa248a-ad0b-4558-a3b2-c4b62ce08b97"

        response = self.client.get(f"/api/questions/answers/{ID}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_update_answer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        answer = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        response = self.client.patch(
            f"/api/questions/answers/{answer.data['id']}/",
            data={"content": "mundando resposta"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("content", response.data)
        self.assertEqual("mundando resposta", response.data["content"])
        self.assertNotEqual(
            response.data["date_published"], response.data["updated_at"]
        )

    def test_update_answer_not_be_owner(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        answer = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data_wrong.key)

        response = self.client.patch(
            f"/api/questions/answers/{answer.data['id']}/",
            data={"content": "mundando resposta"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_answer_be_onwer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        answer = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        response = self.client.delete(
            f"/api/questions/answers/{answer.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_delete_answer_not_be_onwer(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data.key)

        answer = self.client.post(
            f"/api/questions/{self.question.id}/answers/",
            data=self.answer_data,
            format="json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_data_wrong.key)

        response = self.client.delete(
            f"/api/questions/answers/{answer.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
