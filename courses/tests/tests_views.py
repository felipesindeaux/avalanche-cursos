from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from categories.models import Category
from courses.models import Course

from users.models import User


class TestCreateCourseViewsByTeacher(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
            "categories": [{"name": "Node"}],
        }

        cls.user_teacher = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_teacher = Token.objects.create(user=cls.user_teacher)

    def test_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(
            "/api/courses/", data=self.course_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("title", response.data)
        self.assertIn("description", response.data)
        self.assertIn("price", response.data)
        self.assertIn("total_hours", response.data)
        self.assertIn("categories", response.data)

    def test_create_course_with_invalid_price(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        self.course_data["price"] = 1.222

        response = self.client.post(
            "/api/courses/", data=self.course_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_list_course_created(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        for _ in range(5):
            self.client.post("/api/courses/", data=self.course_data, format="json")

        response = self.client.get("/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, len(response.data))


class TestCourseViewsByTeacher(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
        }

        cls.user_teacher = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.other_teacher = User.objects.create(
            email="teste2@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.token_teacher = Token.objects.create(user=cls.user_teacher)
        cls.token_other_teacher = Token.objects.create(user=cls.other_teacher)

        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()

        cls.course = Course.objects.create(**cls.course_data, owner=cls.user_teacher)
        cls.course.categories.set(cls.category)
        cls.course.save()

        cls.course_deactive = Course.objects.create(
            **cls.course_data, is_active=False, owner=cls.user_teacher
        )
        cls.course_deactive.categories.set(cls.category)
        cls.course_deactive.save()

    def test_buy_course_with_teacher(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_complete_course_with_teacher(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_update_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(
            f"/api/courses/{self.course.id}/", data={"total_hours": 1000}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_hours", response.data)
        self.assertEqual(1000, response.data["total_hours"])
        self.assertNotEqual(
            response.data["date_published"], response.data["updated_at"]
        )

    def test_update_course_not_be_owner(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_other_teacher.key
        )

        response = self.client.patch(
            f"/api/courses/{self.course.id}/", data={"total_hours": 1000}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_delete_course_with_user_no_adm_permission(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.delete(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_activate_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(
            f"/api/courses/activate/{self.course_deactive.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertTrue(response.data["is_active"])

    def test_deactivate_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_teacher.key)

        response = self.client.patch(f"/api/courses/deactivate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_active", response.data)
        self.assertFalse(response.data["is_active"])

    def test_activate_course_not_be_owner(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_other_teacher.key
        )

        response = self.client.patch(f"/api/courses/activate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_deactivate_course_not_be_owner(self):

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_other_teacher.key
        )

        response = self.client.patch(f"/api/courses/deactivate/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)


class TestCourseViewsByStudent(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.course_data = {
            "title": "Titulo",
            "description": "Description",
            "price": 12.22,
            "total_hours": 12,
        }

        cls.user_teacher = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.user_student = User.objects.create(
            email="teste2@mail.com", name="teste", password="123", is_teacher=False
        )

        cls.token_student = Token.objects.create(user=cls.user_student)

        Category.objects.create(name="TEST")
        cls.category = Category.objects.all()

        cls.course = Course.objects.create(**cls.course_data, owner=cls.user_teacher)
        cls.course.categories.set(cls.category)
        cls.course.save()

        cls.course_deactive = Course.objects.create(
            **cls.course_data, is_active=False, owner=cls.user_teacher
        )
        cls.course_deactive.categories.set(cls.category)
        cls.course_deactive.save()

    def test_list_valid_course(self):
        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_course_bought(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.get("/api/courses/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))

    def test_list_course_by_id(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)

    def test_list_course_by_invalid_id(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.get(f"/api/courses/INVALID_ID/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_buy_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("student", response.data)
        self.assertFalse(response.data["is_completed"])

    def test_buy_course_duplicated(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.post(f"/api/courses/buy/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)

    def test_complete_course(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)
        self.client.post(f"/api/courses/buy/{self.course.id}/")

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_completed", response.data)
        self.assertTrue(response.data["is_completed"])

    def test_complete_course_not_buy(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_student.key)

        response = self.client.patch(f"/api/courses/complete/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
