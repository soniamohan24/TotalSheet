# Generated by Django 5.0 on 2024-10-18 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0032_operational_cost_product_formula"),
    ]

    operations = [
        migrations.AddField(
            model_name="workgroup",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="workgroup_logos/"
            ),
        ),
    ]
