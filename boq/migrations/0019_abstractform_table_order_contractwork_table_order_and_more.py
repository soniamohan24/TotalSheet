# Generated by Django 5.0 on 2024-10-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boq", "0018_clientinfo_social_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="abstractform",
            name="table_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="contractwork",
            name="table_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="finishing",
            name="table_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="floor",
            name="table_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="wallmasonry",
            name="table_order",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
