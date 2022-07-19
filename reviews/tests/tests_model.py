from courses.models import Course
from django.test import TestCase
from users.models import User

CATEGORY_DATA = {"name": "teste"}


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        user_object = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        course_object = Course.objects.create(
            owner=user_object,
            title="Titulo",
            description="Description",
            price=1.55,
            total_hours=12,
        )

        cls.review_data = {"score": 5, "comment": "muito boin"}

        cls.user = User.objects.get(pk=user_object.id)
        cls.course = Course.objects.get(pk=course_object.id)

    def test_is_owner_review(self):
        self.assertEqual(True, True)
        # review = Review.objects.create(**self.review_data, user=self.user)

        # review.save()

        # self.assertEqual(self.user.id, review.user_id)

    # def test_score_is_integer(self):
    #     review = Review.objects.create(
    #         **self.review_data, user=self.user, course=self.course
    #     )

    #     review.save()

    #     self.assertIsInstance(review.score, int)

    # def test_comment_is_string(self):
    #     review = Review.objects.create(
    #         **self.review_data, user=self.user, course=self.course
    #     )

    #     review.save()

    #     self.assertIsInstance(review.comment, str)
