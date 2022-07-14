from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    resolution = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    lesson = models.ForeignKey(
        to="lessons.Lesson", related_name="tasks", on_delete=models.CASCADE
    )
