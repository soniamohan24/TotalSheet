# Generated by Django 5.0 on 2024-08-05 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_alter_material_product_brand_and_more"),
        ("projects", "0002_remove_project_is_selected_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract_Margins",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("allow_me", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Contract_Margins_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Contract_Margins_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contract_Margin_product",
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
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Contract_Margins_product_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects_Contract_Margin",
                        to="projects.project",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Contract_Margins_product_unit",
                        to="materials.unit",
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="operational_costs",
                        to="materials.contract_margins",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Operational_Costs",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("allow_me", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Operational_Costs_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Operational_Costs_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Operational_Cost_product",
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
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Operational_Costs_product_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects_operational_cost",
                        to="projects.project",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Operational_Costs_product_unit",
                        to="materials.unit",
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="operational_costs",
                        to="materials.operational_costs",
                    ),
                ),
            ],
        ),
    ]
