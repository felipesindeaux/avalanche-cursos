from categories.models import Category
from courses.models import Course
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User

LESSON_DATA = {
    "title": "Lesson One",
    "description": "Introduction of the Course",
}

READ_ONLY_LESSON_DATA = {
    "id": 999,
    "course_id": 999,
    "is_active": False,
    "created_at": "2022-07-14T16:36:44.002553Z",
    "updated_at": "2022-07-14T16:36:44.002577Z",
}

COURSE_DATA = {
    "title": "Titulo",
    "description": "Description",
    "price": 12.22,
    "total_hours": 12,
}

CATEGORY_DATA = {"name": "teste"}

ADMIN_DATA = {"name": "super", "email": "super2@mail.com", "password": "1234"}

TEACHER_DATA_1 = {
    "name": "prof1",
    "email": "prof1@mail.com",
    "password": "1234",
    "is_teacher": True,
}

TEACHER_DATA_2 = {
    "name": "prof2",
    "email": "prof2@mail.com",
    "password": "1234",
    "is_teacher": True,
}

STUDENT_DATA = {
    "name": "stud",
    "email": "stud@mail.com",
    "password": "1234",
    "is_teacher": False,
}


class TestCreateLesson(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.admin_token = Token.objects.create(user=admin)
        cls.teacher_token = Token.objects.create(user=teacher)
        cls.student_token = Token.objects.create(user=student)

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course.categories.set(cls.categories)
        cls.course.save()

    def test_create_lesson_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_create_lesson_as_admin_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_create_lesson_as_student_fail(self):
        ...

    def test_create_lesson_without_token_fail(self):
        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_create_lesson_with_additional_data_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/",
            data={**LESSON_DATA, **READ_ONLY_LESSON_DATA},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key, value in READ_ONLY_LESSON_DATA.items():
            self.assertNotEqual(response.data[key], value)

    def test_create_lesson_with_missing_data_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/",
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("required", response.data["title"][0].code)
        self.assertEqual("required", response.data["description"][0].code)

