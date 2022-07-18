import copy

from categories.models import Category
from courses.models import Course
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from lessons.models import Lesson
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

        cls.lessont_1 = Lesson.objects.create(**LESSON_DATA, course=cls.course)
        cls.lessont_2 = Lesson.objects.create(**LESSON_DATA, course=cls.course)

    def test_create_task_with_teacher(self):
        ...

    def test_create_task_with_admin(self):
        ...

    def test_create_task_with_student(self):
        ...

    def test_create_task_with_teacher_not_owner(self):
        ...

    def test_create_task_to_not_exists_lesson(self):
        ...


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

        course = Course.objects.create(owner=teacher, **COURSE_DATA)
        course.categories.set(categories)
        course.save()

        cls.lessont_1 = Lesson.objects.create(**LESSON_DATA, course=course)
        cls.lessont_2 = Lesson.objects.create(**LESSON_DATA, course=course)

        cls.tasks = [
            Task.objects.create(**TASK_DATA, lesson=cls.lessont_1) for i in range(5)
        ]

        cls.tasks_2 = [
            Task.objects.create(**TASK_DATA, lesson=cls.lessont_2) for i in range(5)
        ]

    def test_list_tasks_with_student_not_buy_the_course(self):
        ...

    def test_list_tasks_with_student_of_bought_the_course(self):
        ...

    def test_list_tasks_with_teacher_owner(self):
        ...

    def test_list_tasks_with_teacher_not_owner(self):
        ...

    def test_list_tasks_with_admin(self):
        ...

    def test_retrieve_task_with_student_not_buy_the_course(self):
        ...

    def test_retrieve_task_with_student_of_bought_the_course(self):
        ...

    def test_retrieve_task_with_teacher_owner(self):
        ...

    def test_retrieve_task_with_teacher_not_owner(self):
        ...

    def test_retrieve_task_with_admin(self):
        ...


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

        cls.lessont_1 = Lesson.objects.create(**LESSON_DATA, course=course)
        cls.lessont_2 = Lesson.objects.create(**LESSON_DATA, course=course)

        cls.tasks = Task.objects.create(**TASK_DATA, lesson=cls.lessont_1)
        cls.tasks_2 = Task.objects.create(
            **TASK_DATA, lesson=cls.lessont_2, is_active=False
        )

    def test_update_task_with_student(self):
        ...

    def test_update_task_with_teacher_owner(self):
        ...

    def test_update_task_with_teacher_not_owner(self):
        ...

    def test_update_task_with_admin(self):
        ...

    def test_activate_task_with_teacher_owner(self):
        ...

    def test_activate_task_with_teacher_not_owner(self):
        ...

    def test_activate_task_with_student(self):
        ...

    def test_activate_task_with_admin(self):
        ...

    def test_deactivate_task_with_teacher_owner(self):
        ...

    def test_deactivate_task_with_teacher_not_owner(self):
        ...

    def test_deactivate_task_with_student(self):
        ...

    def test_deactivate_task_with_admin(self):
        ...


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

        cls.lessont_1 = Lesson.objects.create(**LESSON_DATA, course=course)
        cls.lessont_2 = Lesson.objects.create(**LESSON_DATA, course=course)

        cls.tasks = Task.objects.create(**TASK_DATA, lesson=cls.lessont_1)

    def test_deactivate_task_with_admin(self):
        ...

    def test_deactivate_task_with_teacher_owner(self):
        ...

    def test_deactivate_task_with_teacher_not_owner(self):
        ...

    def test_deactivate_task_with_student(self):
        ...
