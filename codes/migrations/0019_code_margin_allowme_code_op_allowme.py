# Generated by Django 5.0 on 2024-11-06 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codes", "0018_code_offsiteexpense_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="code",
            name="margin_allowme",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="op_allowme",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
