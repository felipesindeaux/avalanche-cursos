# Generated by Django 4.0.6 on 2022-07-18 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0003_alter_student_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
