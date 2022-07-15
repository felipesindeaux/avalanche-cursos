from django.db import models
from django.utils import timezone
import uuid


class Lesson(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    course = models.ForeignKey(
        to="courses.Course", related_name="lessons", on_delete=models.CASCADE
    )
