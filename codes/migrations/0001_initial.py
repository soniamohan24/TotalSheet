# Generated by Django 5.0 on 2024-07-12 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="code_Execution",
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
                    "execution_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("code", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("need", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "basic_value",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_value", models.CharField(blank=True, max_length=100, null=True)),
                ("sub_total", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_execution_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="code_Material",
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
                    "material_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("code", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("Required", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "basic_value",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_value", models.CharField(blank=True, max_length=100, null=True)),
                ("sub_total", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_material_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="codematerial_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="code_OffSiteExpense",
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
                    "offsite_expense_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "on_value",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("i_need", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "basic_value",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_value", models.CharField(blank=True, max_length=100, null=True)),
                ("sub_total", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_offsite_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_offsite_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="code_OnSiteExpense",
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
                    "onsite_expense_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "on_value",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("allow_me", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "basic_value",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_value", models.CharField(blank=True, max_length=100, null=True)),
                ("sub_total", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "gst",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_onsite_gst",
                        to="materials.gst",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_onsite_unit",
                        to="materials.unit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Code",
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
                ("industries", models.CharField(blank=True, max_length=100, null=True)),
                ("group_name", models.CharField(blank=True, max_length=100, null=True)),
                ("created_by", models.CharField(blank=True, max_length=100, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                (
                    "code_preview",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("design_for", models.CharField(blank=True, max_length=100, null=True)),
                ("unit", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "basic_value",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("gst_value", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "grand_total",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=100, null=True),
                ),
                ("note", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "code_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("default_code", "default_code"),
                            ("draft_code", "draft_code"),
                            ("used_boq_code", "used_boq_code"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "code_execution",
                    models.ManyToManyField(
                        blank=True,
                        related_name="execution_codes",
                        to="codes.code_execution",
                    ),
                ),
                (
                    "code_material",
                    models.ManyToManyField(
                        blank=True,
                        related_name="material_codes",
                        to="codes.code_material",
                    ),
                ),
                (
                    "offsite_expense",
                    models.ManyToManyField(
                        blank=True,
                        related_name="offsite_codes",
                        to="codes.code_offsiteexpense",
                    ),
                ),
                (
                    "onsite_expense",
                    models.ManyToManyField(
                        blank=True,
                        related_name="onsite_codes",
                        to="codes.code_onsiteexpense",
                    ),
                ),
            ],
        ),
    ]
