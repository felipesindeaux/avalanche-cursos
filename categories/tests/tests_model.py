from categories.models import Category
from django.db import IntegrityError
from django.test import TestCase


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_create = Category.objects.create(
            name="test_category",
        )

    def test_first_name_max_length(self):
        category = Category.objects.get(id=self.category_create.id)

        max_length = category._meta.get_field("name").max_length

        self.assertEquals(max_length, 127)
