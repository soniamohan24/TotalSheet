# Generated by Django 5.0 on 2024-07-12 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PhysicalFitness",
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
                ("description", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Profession",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Vision",
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
                ("description", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="WorkChallenge",
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
                ("description", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="WorkPlace",
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
                ("place", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="BusinessProfile",
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
                ("industries", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "company_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "company_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("cin_no", models.CharField(blank=True, max_length=21, null=True)),
                ("gst_no", models.CharField(blank=True, max_length=15, null=True)),
                ("location_link", models.URLField(blank=True, null=True)),
                (
                    "whatsapp_mobile_no",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("email_verified", models.BooleanField(default=False)),
                ("whatsapp_verified", models.BooleanField(default=False)),
                ("social_link_additional", models.URLField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("work_history", models.TextField(blank=True, null=True)),
                ("photo_showcase", models.URLField(blank=True, null=True)),
                ("video_showcase", models.URLField(blank=True, null=True)),
                (
                    "project_brochures",
                    models.FileField(
                        blank=True, null=True, upload_to="project_brochures/"
                    ),
                ),
                ("advertisement", models.TextField(blank=True, null=True)),
                (
                    "approved_association_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_business_associations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_company_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_business_companies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_friends_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_business_friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_influencer_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_business_influencers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JOBProfile",
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
                    "passport_type_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="passport_photos/"
                    ),
                ),
                (
                    "qualification",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "sex",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("current_resident_address", models.TextField(blank=True, null=True)),
                ("adhar_no", models.CharField(blank=True, max_length=12, null=True)),
                ("adhar_verified", models.BooleanField(default=False)),
                ("pan_no", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "marital_status",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Married"), ("S", "Single")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("anniversary_date", models.DateField(blank=True, null=True)),
                (
                    "spouse_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("children_count", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "experience_months",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "experience_years",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "last_work_place",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "reference_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "reference_contact_no",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "work_duration",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "work_choice",
                    models.CharField(
                        blank=True,
                        choices=[("H", "Hourly"), ("D", "Daily"), ("M", "Monthly")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "expected_salary_hourly",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "expected_salary_daily",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "expected_salary_monthly",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("work_history", models.TextField(blank=True, null=True)),
                ("photo_showcase_description", models.TextField(blank=True, null=True)),
                ("video_showcase_description", models.TextField(blank=True, null=True)),
                (
                    "emergency_contact_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "emergency_contact_phone_no",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "emergency_contact_place",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "emergency_contact_relationship",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("looking_for_international", models.BooleanField(default=False)),
                ("passport_no", models.CharField(blank=True, max_length=9, null=True)),
                (
                    "medical_report",
                    models.FileField(
                        blank=True, null=True, upload_to="medical_reports/"
                    ),
                ),
                (
                    "insurance_policy_no",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("insurance_verified", models.BooleanField(default=False)),
                ("accident_policy_valid_upto", models.DateField(blank=True, null=True)),
                ("if_not_buy_policy", models.BooleanField(default=False)),
                ("get_membership", models.BooleanField(default=False)),
                ("vehicle_owned", models.BooleanField(default=False)),
                (
                    "vehicle_type",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "vehicle_model",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "vehicle_usage",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("vehicle_year", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "vehicle_registration_no",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "vehicle_insurance_policy_no",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("vehicle_insurance_verified", models.BooleanField(default=False)),
                (
                    "vehicle_accident_policy_valid_upto",
                    models.DateField(blank=True, null=True),
                ),
                ("vehicle_if_not_buy_policy", models.BooleanField(default=False)),
                ("vehicle_get_membership", models.BooleanField(default=False)),
                (
                    "approved_company_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_companies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_friends_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_influencer_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="approved_influencers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "physical_fitness",
                    models.ManyToManyField(blank=True, to="profile.physicalfitness"),
                ),
                ("skills", models.ManyToManyField(blank=True, to="profile.skill")),
                ("vision", models.ManyToManyField(blank=True, to="profile.vision")),
                (
                    "work_challenges",
                    models.ManyToManyField(blank=True, to="profile.workchallenge"),
                ),
                (
                    "choice_of_work_place",
                    models.ManyToManyField(blank=True, to="profile.workplace"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("mid_name", models.CharField(blank=True, max_length=30, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("pan_no", models.CharField(blank=True, max_length=10, null=True)),
                ("facebook_link", models.URLField(blank=True, null=True)),
                ("linkedin_link", models.URLField(blank=True, null=True)),
                ("other_social_link", models.URLField(blank=True, null=True)),
                ("social_link_additional", models.URLField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("work_history", models.TextField(blank=True, null=True)),
                ("photo_showcase", models.URLField(blank=True, null=True)),
                ("video_showcase", models.URLField(blank=True, null=True)),
                (
                    "project_brochures",
                    models.FileField(
                        blank=True, null=True, upload_to="project_brochures/"
                    ),
                ),
                ("advertisement", models.TextField(blank=True, null=True)),
                (
                    "approved_association_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="business_associations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_company_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="business_companies",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_friends_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="business_friends",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approved_influencer_connections",
                    models.ManyToManyField(
                        blank=True,
                        related_name="business_influencers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "business_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profile.businessprofile",
                    ),
                ),
                (
                    "job_profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profile.jobprofile",
                    ),
                ),
                (
                    "profession",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="profile.profession",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
