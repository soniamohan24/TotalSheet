# Generated by Django 5.0 on 2024-08-22 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0011_alter_contract_margin_product_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Formula",
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
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
            ],
        ),
    ]
