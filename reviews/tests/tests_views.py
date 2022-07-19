from courses.models import Course
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from reviews.models import Review
from users.models import User

REVIEW_DATA = {"score": 5, "comment": "muito boin"}

UPDATE_REVIEW_DATA = {"comment": "atualizado"}

COURSE_DATA = {
    "title": "Titulo",
    "description": "Description",
    "price": 12.22,
    "total_hours": 12,
}

USER_OWNER_COURSE_DATA = {
    "name": "teach",
    "email": "teach@mail.com",
    "password": "1234",
    "is_teacher": True,
}

USER_REVEIWER_DATA = {
    "name": "user",
    "email": "user@mail.com",
    "password": "1234",
    "is_teacher": False,
}


class ReviewViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        teacher = User.objects.create_user(**USER_OWNER_COURSE_DATA)
        student = User.objects.create_user(**USER_REVEIWER_DATA)

        cls.teacher_token = Token.objects.create(user=teacher)
        cls.student_token = Token.objects.create(user=student)

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)

        cls.course.save()

        cls.review = Review.objects.create(
            **REVIEW_DATA, user=student, course=cls.course
        )

        cls.review.save()

    def create_review_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        response = self.client.post(
            f"/api/review/course/{self.course.id}/", data=REVIEW_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_without_token_fail(self):
        response = self.client.post(
            f"/api/review/course/{self.course.id}/", data=REVIEW_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_get_reviews_by_course(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.get(f"/api/review/course/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.get(f"/api/review/{self.review.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        response = self.client.patch(
            f"/api/review/{self.review.id}/", UPDATE_REVIEW_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        response = self.client.delete(f"/api/review/{self.review.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
