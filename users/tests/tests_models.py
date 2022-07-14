from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user_data = {"name": "usertest", "email": "test@mail.com",
                     "password": "1234", "is_teacher": True}

        cls.user = User.objects.create(**cls.user_data)

    def test_name_max_length(self):
        user = User.objects.get(id=1)

        max_length = user._meta.get_field("name").max_length

        self.assertEquals(max_length, 127)

    def test_user_fields(self):

        self.assertEqual(self.user.name,
                         self.user_data["name"])
        self.assertEqual(self.user.email,
                         self.user_data["email"])
        self.assertEqual(self.user.is_teacher,
                         self.user_data["is_teacher"])
        self.assertIsNotNone(self.user.password)
