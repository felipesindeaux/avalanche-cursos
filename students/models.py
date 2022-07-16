from django.db import models
import uuid


class Student(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_completed = models.BooleanField(default=False)
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="students"
    )
    student = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="students"
    )
