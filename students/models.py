from django.db import models


class Student(models.Model):
    is_completed = models.BooleanField(default=False)
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="students"
    )
    student = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="students"
    )
