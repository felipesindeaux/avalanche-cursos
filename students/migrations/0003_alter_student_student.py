# Generated by Django 4.0.6 on 2022-07-18 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
