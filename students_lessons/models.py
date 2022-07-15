from django.db import models


class StudentLessons(models.Model):

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
