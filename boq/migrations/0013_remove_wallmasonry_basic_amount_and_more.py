# Generated by Django 5.0 on 2024-09-10 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("boq", "0012_alter_finishing_code"),
        ("codes", "0005_code_execution_total_gst_code_material_total_gst"),
        ("materials", "0016_total_operational_cost_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wallmasonry",
            name="basic_amount",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="code",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="full_amount",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="gst_amount",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="gst_applied",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="rate_per_unit",
        ),
        migrations.RemoveField(
            model_name="wallmasonry",
            name="unit",
        ),
        migrations.CreateModel(
            name="AbstractForm",
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
                ("form_name", models.CharField(blank=True, max_length=50, null=True)),
                ("table_name", models.CharField(blank=True, max_length=100, null=True)),
                ("work_detail", models.TextField(blank=True, null=True)),
                (
                    "value_excluding_gst",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("ratio", models.CharField(blank=True, max_length=100, null=True)),
                ("full_amount", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "basic_amount",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "gst_applied",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("gst_amount", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "boq",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="abs_form",
                        to="boq.boq",
                    ),
                ),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="abs_gst",
                        to="materials.gst",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Total",
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
                ("table_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "full_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "basic_amount",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "gst_applied",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_amount", models.CharField(blank=True, max_length=100, null=True)),
                ("quantity", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "rate_per_unit",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("ratio", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "boq",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="boq.boq",
                    ),
                ),
                (
                    "code",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="walltable_code",
                        to="codes.code",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materials.unit",
                    ),
                ),
            ],
            options={
                "unique_together": {("boq", "table_name")},
            },
        ),
        migrations.DeleteModel(
            name="BasicForm",
        ),
    ]
