from django.test import TestCase
from answers.models import Answer
from categories.models import Category
from users.models import User
from questions.models import Question
from datetime import datetime as dt


class AnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.question_data = {
            "title": "Titulo",
            "description": "Description",
        }
        
        cls.question = Question.objects.create(**cls.question_data, user=cls.user)

        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()
        cls.question.categories.set(cls.category)
        cls.question.save()
        

        cls.answer_data = {
            "content": "Resposta Teste"
        }

        cls.content="Resposta Teste"
        
        

    def test_onwer_of_answer(self):
        answer = Answer.objects.create(**self.answer_data, user=self.user, question=self.question)
        answer.save()
        self.assertIn("user_id", answer.__dict__)
        self.assertEqual(self.user.id, answer.user_id)

    def test_answer_has_information_fields(self):
        answer = Answer.objects.create(**self.answer_data, user=self.user, question=self.question)
        answer.save()
        date_now = dt.strftime(dt.now(), "%D")
        date_model = dt.strftime(answer.date_published, "%D")

        self.assertEqual(answer.content, self.content)
        self.assertEqual(date_now, date_model)
