# Generated by Django 5.0 on 2024-09-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0014_alter_jobprofile_sex"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
