from django.test import TestCase
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
        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()

        cls.question_data = {
            "title": "Titulo",
            "description": "Description",
        }

        cls.title = "Titulo"
        cls.description = "Description"

    def test_onwer_of_question(self):
        question = Question.objects.create(**self.question_data, user=self.user)
        question.categories.set(self.category)
        question.save()
        self.assertIn("user_id", question.__dict__)
        self.assertEqual(self.user.id, question.user_id)

    def test_question_has_information_fields(self):
        question = Question.objects.create(**self.question_data, user=self.user)
        question.categories.set(self.category)
        question.save()

        date_now = dt.strftime(dt.now(), "%D")
        date_model = dt.strftime(question.date_published, "%D")

        self.assertEqual(question.description, self.description)
        self.assertEqual(question.title, self.title)
        self.assertEqual(date_now, date_model)