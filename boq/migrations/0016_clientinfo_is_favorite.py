# Generated by Django 5.0 on 2024-09-18 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boq", "0015_rename_code_finishing_free_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientinfo",
            name="is_favorite",
            field=models.BooleanField(default=False),
        ),
    ]
