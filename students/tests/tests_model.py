from courses.models import Course
from django.test import TestCase
from students.models import Student
from users.models import User


class StudentTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            email="teste@mail.com", name="teste", password="123", is_teacher=True
        )

        cls.course = Course.objects.create(
            title="curso",
            description="curso descricao",
            price=1.99,
            total_hours=24,
            owner=cls.user,
        )

    def test_student_creation(self):
        student = Student.objects.create(student=self.user, course=self.course)

        student.save()

        self.assertIn("course_id", student.__dict__)
        self.assertIn("student_id", student.__dict__)
        self.assertEqual(self.user.id, student.student_id)
        self.assertEqual(self.course.id, student.course_id)

    def test_is_completed_default_of_student(self):
        student = Student.objects.create(student=self.user, course=self.course)

        student.save()

        self.assertFalse(student.is_completed)
