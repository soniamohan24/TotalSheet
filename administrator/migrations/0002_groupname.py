# Generated by Django 5.0 on 2024-09-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
