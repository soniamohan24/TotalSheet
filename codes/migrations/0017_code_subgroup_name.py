# Generated by Django 5.1.2 on 2024-10-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0016_alter_code_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='subgroup_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
