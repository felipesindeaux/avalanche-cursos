from django.test import TestCase

# from users.models import User
# from questions.models import Question
# from answers.models import Answer


# from rest_framework.views import status


class AnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        print("executando o teste")
    #     cls.user_data = {
    #         "name": "usertest",
    #         "email": "test@mail.com",
    #         "password": "1234",
    #         "is_teacher": True,
    #     }

    #     cls.user = User.objects.create(**cls.user_data)

    #     cls.question_data = {"title": "bom dia", "description": "bom dia familia"}

    #     cls.user = Question.objects.create(**cls.question_data)

    #     cls.content = "respondendo sua pergunta"

    #     cls.answer = Answer.objects.create(content=cls.content)

    def test_user_fields(self):
        print("executando o teste")