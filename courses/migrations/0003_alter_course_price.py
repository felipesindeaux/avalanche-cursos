# Generated by Django 4.0.6 on 2022-07-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
