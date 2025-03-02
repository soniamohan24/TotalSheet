# Generated by Django 5.0 on 2024-08-22 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0012_formula"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract_margins",
            name="formula",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contract_formula",
                to="materials.formula",
            ),
        ),
        migrations.AddField(
            model_name="operational_costs",
            name="formula",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="operational_formula",
                to="materials.formula",
            ),
        ),
    ]
