# Generated by Django 5.0 on 2024-09-03 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0013_alter_profile_profile_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobprofile",
            name="sex",
            field=models.CharField(
                blank=True,
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                max_length=1,
                null=True,
            ),
        ),
    ]
