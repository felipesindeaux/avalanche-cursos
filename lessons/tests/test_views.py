from categories.models import Category
from courses.models import Course
from lessons.models import Lesson
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from students_lessons.models import StudentLessons
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
        cls.student = User.objects.create_user(**STUDENT_DATA)

        cls.admin_token = Token.objects.create(user=admin)
        cls.teacher_token = Token.objects.create(user=teacher)
        cls.student_token = Token.objects.create(user=cls.student)

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

    def test_create_lesson_with_invalid_course_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/1322asdasd13213/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_lesson_with_unexistent_course_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/b024b8d9-39ae-4159-bac4-62c6fad05b91/lessons/",
            data=LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual("not_found", response.data["detail"].code)

    def test_create_lesson_as_admin_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_create_lesson_as_student_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/", data=LESSON_DATA
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

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

    def test_create_lesson_affect_student_lessons_table(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)

        response = self.client.post(
            f"/api/courses/{self.course.id}/lessons/",
            data=LESSON_DATA,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        student_lessons = StudentLessons.objects.all()
        self.assertEqual(len(student_lessons), 1)


class TestListLesson(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher_1 = User.objects.create_user(**TEACHER_DATA_1)
        teacher_2 = User.objects.create_user(**TEACHER_DATA_2)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.admin_token = Token.objects.create(user=admin)
        cls.teacher_token_1 = Token.objects.create(user=teacher_1)
        cls.teacher_token_2 = Token.objects.create(user=teacher_2)
        cls.student_token = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course_1 = Course.objects.create(owner=teacher_1, **COURSE_DATA)
        cls.course_1.categories.set(cls.categories)
        cls.course_1.save()

        cls.course_2 = Course.objects.create(owner=teacher_2, **COURSE_DATA)
        cls.course_2.categories.set(cls.categories)
        cls.course_2.save()

        cls.lessons_1 = [
            Lesson.objects.create(**LESSON_DATA, course=cls.course_1) for i in range(5)
        ]
        cls.lessons_2 = [
            Lesson.objects.create(**LESSON_DATA, course=cls.course_2) for i in range(5)
        ]

    def test_get_lessons_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.get(f"/api/courses/{self.course_1.id}/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, len(response.data["results"]))

    def test_get_lessons_as_admin_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/api/courses/{self.course_1.id}/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, len(response.data["results"]))

    def test_get_lessons_as_student_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.get(f"/api/courses/{self.course_1.id}/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, len(response.data["results"]))

    def test_get_lessons_without_token_fail(self):
        response = self.client.get(f"/api/courses/{self.course_1.id}/lessons/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_retrieve_lesson_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.get(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_retrieve_lesson_as_admin_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.get(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_retrieve_lesson_as_student_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.get(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_retrieve_lesson_without_token_fail(self):
        response = self.client.get(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_retrieve_lesson_as_teacher_from_other_course_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_2.key)

        response = self.client.get(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission_denied", response.data["detail"].code)

    def test_retrieve_lesson_as_student_from_other_course_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.get(f"/api/lessons/{self.lessons_2[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission_denied", response.data["detail"].code)

    def test_update_lesson_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_update_lesson_as_student_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission_denied", response.data["detail"].code)

    def test_update_lesson_as_admin_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission_denied", response.data["detail"].code)

    def test_update_lesson_without_token_fail(self):
        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("not_authenticated", response.data["detail"].code)

    def test_update_lesson_as_teacher_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_2.key)

        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            LESSON_DATA,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission_denied", response.data["detail"].code)

    def test_update_lesson_with_additional_data_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.patch(
            f"/api/lessons/{self.lessons_1[0].id}/",
            data={**LESSON_DATA, **READ_ONLY_LESSON_DATA},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in READ_ONLY_LESSON_DATA.items():
            self.assertNotEqual(response.data[key], value)

    def test_activate_lesson_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"], True)

    def test_deactivate_lesson_as_teacher_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/deactivate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"], False)

    def test_activate_lesson_as_admin_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_deactivate_lesson_as_admin_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/deactivate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_activate_lesson_as_student_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_deactivate_lesson_as_student_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.patch(f"/api/lessons/{self.lessons_1[0].id}/deactivate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_delete_lesson_as_teacher_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token_1.key)

        response = self.client.delete(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_delete_lesson_as_student_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)

        self.client.post(f"/api/courses/buy/{self.course_1.id}/")

        response = self.client.delete(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_delete_lesson_without_token_fail(self):
        response = self.client.delete(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_delete_lesson_as_admin_succcess(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)

        response = self.client.delete(f"/api/lessons/{self.lessons_1[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
