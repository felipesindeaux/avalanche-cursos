from django.db import models
import uuid


class StudentLessons(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_completed = models.BooleanField(default=False)

    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="students_lesson"
    )
    student = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="students_lesson"
    )
    lesson = models.ForeignKey(
        "lessons.Lesson", on_delete=models.CASCADE, related_name="students"
    )
