import uuid

from django.db import models


class StudentLessons(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_completed = models.BooleanField(default=False)

    student = models.ForeignKey(
        "students.Student", on_delete=models.CASCADE, related_name="lessons"
    )
    lesson = models.ForeignKey(
        "lessons.Lesson", on_delete=models.CASCADE, related_name="students_lessons"
    )
