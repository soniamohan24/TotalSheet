# Generated by Django 5.0 on 2024-08-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codes", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="code_execution",
            name="code",
        ),
        migrations.RemoveField(
            model_name="code_material",
            name="code",
        ),
        migrations.AddField(
            model_name="code",
            name="execution_code",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="execution_subtotal",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="execution_total_basicvalue",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="execution_total_gstvalue",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="execution_total_rate",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="margin_subtotal",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="margin_total_basicvalue",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="margin_totalrate",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="material_code",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="material_subtotal",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="material_total_basicvalue",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="material_total_gstvalue",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="code",
            name="material_total_rate",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
