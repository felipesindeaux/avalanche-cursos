from django.db import models
from datetime import datetime as dt
class Course(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField()
    total_hours = models.IntegerField()
    date_published = models.DateTimeField(default=dt.now())
    updated_at = models.DateTimeField(default=dt.now())
    is_active = models.BooleanField(default=True)

    owner_id = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")