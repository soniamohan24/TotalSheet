# Generated by Django 5.0 on 2024-08-28 07:18

import django.db.models.deletion
import profile.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0011_delete_profile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                (
                    "profile_photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=profile.models.get_profile_photo_path,
                    ),
                ),
                ("mid_name", models.CharField(blank=True, max_length=30, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("pan_no", models.CharField(blank=True, max_length=10, null=True)),
                ("facebook_link", models.URLField(blank=True, null=True)),
                ("linkedin_link", models.URLField(blank=True, null=True)),
                ("other_social_link", models.URLField(blank=True, null=True)),
                ("work_history", models.TextField(blank=True, null=True)),
                ("photo_showcase", models.URLField(blank=True, null=True)),
                ("video_showcase", models.URLField(blank=True, null=True)),
                (
                    "project_brochures",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=profile.models.get_project_brochure_path,
                    ),
                ),
                ("advertisement", models.TextField(blank=True, null=True)),
                (
                    "profile_type",
                    models.CharField(
                        choices=[
                            ("jobseeker", "Job Seeker"),
                            ("business", "Business"),
                            ("client", "Client"),
                        ],
                        default="jobseeker",
                        max_length=20,
                    ),
                ),
                ("unique_id", models.CharField(blank=True, max_length=8, null=True)),
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
                    "social_link",
                    models.ManyToManyField(
                        blank=True,
                        related_name="profile_social_link",
                        to="profile.socials",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "website",
                    models.ManyToManyField(
                        blank=True,
                        related_name="profile_websites",
                        to="profile.website",
                    ),
                ),
            ],
        ),
    ]
