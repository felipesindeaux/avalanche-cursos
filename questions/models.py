from django.db import models

class Question(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="questions")
