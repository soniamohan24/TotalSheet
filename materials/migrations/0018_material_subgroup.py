# Generated by Django 5.0 on 2024-09-20 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0017_remove_total_operational_cost_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="material",
            name="subgroup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subgroup_material",
                to="materials.subgroup",
            ),
        ),
    ]
