import uuid

from django.db import models


class Course(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    total_hours = models.IntegerField()
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="courses"
    )
    categories = models.ManyToManyField("categories.Category", related_name="courses")
