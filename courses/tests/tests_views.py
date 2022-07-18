import copy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from categories.models import Category
from courses.models import Course

from users.models import User

COURSE_DATA = {
    "title": "title",
    "description": "Description",
    "price": 12.22,
    "total_hours": 12,
}

CATEGORY_DATA = {"name": "teste"}

COURSE_DATA_REQUEST = {
    "title": "title",
    "description": "Description",
    "price": 12.22,
    "total_hours": 12,
    "categories": [CATEGORY_DATA],
}

ADMIN_DATA = {"name": "super", "email": "super@mail.com", "password": "1234"}

TEACHER_DATA_1 = {
    "name": "teacher",
    "email": "teacher@mail.com",
    "password": "1234",
    "is_teacher": True,
}

TEACHER_DATA_2 = {
    "name": "teacher2",
    "email": "teacher2@mail.com",
    "password": "1234",
    "is_teacher": True,
}

STUDENT_DATA = {
    "name": "student",
    "email": "student@mail.com",
    "password": "1234",
    "is_teacher": False,
}


class TestCreateCourseViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

    def test_create_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            "/api/courses/", data=COURSE_DATA_REQUEST, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("categories", response.data)

    def test_create_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.post(
            "/api/courses/", data=COURSE_DATA_REQUEST, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("categories", response.data)

    def test_create_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.post(
            "/api/courses/", data=COURSE_DATA_REQUEST, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_create_course_with_invalid_price(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        course_data = copy.deepcopy(COURSE_DATA_REQUEST)
        course_data["price"] = 1.222

        response = self.client.post("/api/courses/", data=course_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_create_course_without_categories(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post("/api/courses/", data=COURSE_DATA, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("categories", response.data)

    def test_list_course_created(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        for _ in range(5):
            self.client.post("/api/courses/", data=COURSE_DATA_REQUEST, format="json")

        response = self.client.get("/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, len(response.data))


class TestListCoursesTeacherViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.course_deactive = Course.objects.create(
            **COURSE_DATA, is_active=False, owner=teacher
        )
        cls.course_deactive.categories.set(cls.categories)
        cls.course_deactive.save()

    def test_list_all_course_activate(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_one_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(str(self.course.id), response.data["id"])

    def test_list_all_course_created_by_the_teacher(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_list_all_course_created_by_the_teacher_active(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/courses/me/?active=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_all_course_created_by_the_teacher_deactive(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.get(f"/api/courses/me/?active=false")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))


class TestListCoursesStudentViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.course_two = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course_two.categories.set(cls.categories)
        cls.course_two.save()

        cls.course_deactive = Course.objects.create(
            **COURSE_DATA, is_active=False, owner=teacher
        )
        cls.course_deactive.categories.set(cls.categories)
        cls.course_deactive.save()

    def test_list_all_course_activate(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_list_one_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(str(self.course.id), response.data["id"])

    def test_list_all_course_bought_by_the_student(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get(f"/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_all_course_completed_by_the_student(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")
        self.client.patch(f"/api/courses/complete/{self.course.id}/")

        response = self.client.get(f"/api/courses/me/?completed=completed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_all_course_uncompleted_by_the_student(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get(f"/api/courses/me/?completed=uncompleted")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))


class TestBuyCoursesViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.course_two = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course_two.categories.set(cls.categories)
        cls.course_two.save()

        cls.course_deactive = Course.objects.create(
            **COURSE_DATA, is_active=False, owner=teacher
        )
        cls.course_deactive.categories.set(cls.categories)
        cls.course_deactive.save()

    def test_buy_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(str(self.course.id), response.data["course"]["id"])

    def test_buy_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_buy_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(str(self.course.id), response.data["course"]["id"])

    def test_buy_course_duplicated_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn("detail", response.data)

    def test_buy_course_duplicated_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn("detail", response.data)


class TestUpdatedCoursesViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.course_two = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course_two.categories.set(cls.categories)
        cls.course_two.save()

        cls.course_deactive = Course.objects.create(
            **COURSE_DATA, is_active=False, owner=teacher
        )
        cls.course_deactive.categories.set(cls.categories)
        cls.course_deactive.save()

    def test_update_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            data={"title": "Title_Test"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertEqual("Title_Test", response.data["title"])

    def test_update_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            data={"title": "Title_Test"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_update_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            data={"title": "Title_Test"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(
            f"/api/courses/activate/{self.course_deactive.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertTrue(response.data["is_active"])

    def test_activate_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/courses/activate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(f"/api/courses/activate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(f"/api/courses/deactivate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertFalse(response.data["is_active"])

    def test_deactivate_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/courses/deactivate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(f"/api/courses/deactivate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_complete_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_completed", response.data)
        self.assertTrue(response.data["is_completed"])

    def test_complete_course_not_bought_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_complete_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_completed", response.data)
        self.assertTrue(response.data["is_completed"])

    def test_complete_course_not_bought_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)


class TestDeleteCoursesViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        admin = User.objects.create_superuser(**ADMIN_DATA)
        teacher = User.objects.create_user(**TEACHER_DATA_1)
        student = User.objects.create_user(**STUDENT_DATA)

        cls.token_admin = Token.objects.create(user=admin)
        cls.token_teacher = Token.objects.create(user=teacher)
        cls.token_student = Token.objects.create(user=student)

        Category.objects.create(**CATEGORY_DATA)
        cls.categories = Category.objects.all()

        cls.course = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course.categories.set(cls.categories)
        cls.course.save()

        cls.course_two = Course.objects.create(owner=teacher, **COURSE_DATA)
        cls.course_two.categories.set(cls.categories)
        cls.course_two.save()

        cls.course_deactive = Course.objects.create(
            **COURSE_DATA, is_active=False, owner=teacher
        )
        cls.course_deactive.categories.set(cls.categories)
        cls.course_deactive.save()

    def test_delete_course_with_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_with_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.delete(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_course_with_student(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.delete(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
