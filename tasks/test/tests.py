from categories.models import Category
from courses.models import Course
from lessons.models import Lesson
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from tasks.models import Task
from users.models import User

COURSE_DATA = {
    "title": "title",
    "description": "Description",
    "price": 12.22,
    "total_hours": 12,
}

CATEGORY_DATA = {"name": "teste"}

ADMIN_DATA = {"name": "super", "email": "super@mail.com", "password": "1234"}

TEACHER_DATA_1 = {
    "name": "teacher",
    "email": "teacher@mail.com",
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
    "name": "student",
    "email": "student@mail.com",
    "password": "1234",
    "is_teacher": False,
}

LESSON_DATA = {
    "title": "Lesson One",
    "description": "Introduction of the Course",
}

TASK_DATA = {
    "title": "Task One",
    "description": "Introduction of the lesson",
    "resolution": "Task resolution",
}


class TestCreateTasksViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        teacher_2 = User.objects.create_user(**TEACHER_DATA_2)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_teacher_2 = Token.objects.create(user=teacher_2)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.lesson_1 = Lesson.objects.create(**LESSON_DATA, course=cls.course)
        cls.lesson_2 = Lesson.objects.create(**LESSON_DATA, course=cls.course)

    def test_create_task_with_teacher(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            f"/api/lessons/{self.lesson_1.id}/tasks/", data=TASK_DATA, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("lesson_id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("resolution", response.data)
        self.assertTrue("resolution")

    def test_create_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.post(
            f"/api/lessons/{self.lesson_1.id}/tasks/", data=TASK_DATA, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_create_task_with_student(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.post(
            f"/api/lessons/{self.lesson_1.id}/tasks/", data=TASK_DATA, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_create_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.post(
            f"/api/lessons/{self.lesson_1.id}/tasks/", data=TASK_DATA, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_create_task_to_not_exists_lesson(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            f"/api/lessons/Invalid_ID_Lesson/tasks/", data=TASK_DATA, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_with_invalid_request(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            f"/api/lessons/{self.lesson_1.id}/tasks/",
            data={
                "title": "Task One",
                "description": "Introduction of the lesson",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("resolution", response.data)


class TestListTasksViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        teacher_2 = User.objects.create_user(**TEACHER_DATA_2)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_teacher_2 = Token.objects.create(user=teacher_2)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(categories)
        cls.course.save()

        cls.lesson_1 = Lesson.objects.create(**LESSON_DATA, course=cls.course)
        cls.lesson_2 = Lesson.objects.create(**LESSON_DATA, course=cls.course)

        cls.tasks = [
            Task.objects.create(**TASK_DATA, lesson=cls.lesson_1) for i in range(5)
        ]

        cls.tasks_2 = [
            Task.objects.create(**TASK_DATA, lesson=cls.lesson_2) for i in range(5)
        ]

    def test_list_tasks_with_student_not_buy_the_course(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/lessons/{self.lesson_1.id}/tasks/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_list_tasks_with_student_of_bought_the_course(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get(f"/api/lessons/{self.lesson_1.id}/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(5, response.data["count"])

    def test_list_tasks_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get(f"/api/lessons/{self.lesson_1.id}/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(5, response.data["count"])

    def test_list_tasks_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.get(f"/api/lessons/{self.lesson_1.id}/tasks/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_list_tasks_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(f"/api/lessons/{self.lesson_1.id}/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertEqual(5, response.data["count"])

    def test_retrieve_task_with_student_not_buy_the_course(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/tasks/{self.tasks[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_retrieve_task_with_student_of_bought_the_course(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get(f"/api/tasks/{self.tasks[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("lesson_id", response.data)
        self.assertEqual(str(self.lesson_1.id), response.data["lesson_id"])

    def test_retrieve_task_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/tasks/{self.tasks[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("lesson_id", response.data)
        self.assertEqual(str(self.lesson_1.id), response.data["lesson_id"])

    def test_retrieve_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.get(f"/api/tasks/{self.tasks[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_retrieve_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.get(f"/api/tasks/{self.tasks[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("lesson_id", response.data)
        self.assertEqual(str(self.lesson_1.id), response.data["lesson_id"])


class TestUpdateTasksViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        teacher_2 = User.objects.create_user(**TEACHER_DATA_2)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_teacher_2 = Token.objects.create(user=teacher_2)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        categories = Category.objects.all()

        course = Course.objects.create(owner=teacher, **COURSE_DATA)
        course.categories.set(categories)
        course.save()

        cls.lesson_1 = Lesson.objects.create(**LESSON_DATA, course=course)
        cls.lesson_2 = Lesson.objects.create(**LESSON_DATA, course=course)

        cls.tasks = Task.objects.create(**TASK_DATA, lesson=cls.lesson_1)
        cls.tasks_2 = Task.objects.create(
            **TASK_DATA, lesson=cls.lesson_2, is_active=False
        )

    def test_update_task_with_student(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(
            f"/api/tasks/{self.tasks.id}/",
            data={"title": "Update Teste"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_update_task_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(
            f"/api/tasks/{self.tasks.id}/",
            data={"title": "Update Teste"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertEqual("Update Teste", response.data["title"])

    def test_update_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.patch(
            f"/api/tasks/{self.tasks.id}/",
            data={"title": "Update Teste"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_update_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(
            f"/api/tasks/{self.tasks.id}/",
            data={"title": "Update Teste"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_task_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertTrue(response.data["is_active"])

    def test_activate_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_task_with_student(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_task_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/deactivate/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertFalse(response.data["is_active"])

    def test_deactivate_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_task_with_student(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(f"/api/tasks/{self.tasks.id}/activate/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)


class TestDeleteTasksViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        teacher_2 = User.objects.create_user(**TEACHER_DATA_2)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_teacher_2 = Token.objects.create(user=teacher_2)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        categories = Category.objects.all()

        course = Course.objects.create(owner=teacher, **COURSE_DATA)
        course.categories.set(categories)
        course.save()

        cls.lesson_1 = Lesson.objects.create(**LESSON_DATA, course=course)
        cls.lesson_2 = Lesson.objects.create(**LESSON_DATA, course=course)

        cls.tasks = Task.objects.create(**TASK_DATA, lesson=cls.lesson_1)

    def test_delete_task_with_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(f"/api/tasks/{self.tasks.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_with_teacher_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.delete(f"/api/tasks/{self.tasks.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_task_with_teacher_not_owner(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_teacher_2.key)

        response = self.client.delete(f"/api/tasks/{self.tasks.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_task_with_student(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.delete(f"/api/tasks/{self.tasks.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
