# Generated by Django 5.0 on 2024-08-23 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0015_total_contract_margin_product"),
        ("projects", "0004_alter_project_client"),
    ]

    operations = [
        migrations.CreateModel(
            name="Total_Operational_cost",
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
                ("allow_me", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField()),
                (
                    "formula",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_operationcost_formula",
                        to="materials.formula",
                    ),
                ),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_operationcost_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_operationcost",
                        to="materials.contract_margins",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_operationcost_Margin",
                        to="projects.project",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="total_operationcost_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Total_Contract_Margin_product",
        ),
    ]
