# Generated by Django 5.0 on 2024-09-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boq", "0010_alter_finishing_code_alter_floor_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientinfo",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clientinfo",
            name="cin_no",
            field=models.CharField(blank=True, max_length=21, null=True),
        ),
        migrations.AddField(
            model_name="clientinfo",
            name="company_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="clientinfo",
            name="pan_no",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="clientinfo",
            name="phone_no",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="clientinfo",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
    ]
