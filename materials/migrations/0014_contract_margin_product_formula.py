# Generated by Django 5.0 on 2024-08-23 06:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0013_contract_margins_formula_operational_costs_formula"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract_margin_product",
            name="formula",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contract_product_formula",
                to="materials.formula",
            ),
        ),
    ]
