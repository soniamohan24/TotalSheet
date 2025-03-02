from django.db import models
from boq.models import CustomUser
from django.utils.crypto import get_random_string
from .utils_models import Socials, Website
import os


def get_profile_photo_path(instance, filename):
    return os.path.join(
        str(instance.user.pk), "profile_photos", filename.replace("_", " ")
    )


def get_passport_photo_path(instance, filename):
    return os.path.join(
        str(instance.user.pk), "passport_photos", filename.replace("_", " ")
    )


def get_medical_report_path(instance, filename):
    return os.path.join(
        str(instance.pk), "medical_report", filename.replace("_", " ")
    )


def get_project_brochure_path(instance, filename):
    return os.path.join(
        str(instance.pk), "project_brochures", filename.replace("_", " ")
    )


PROFILE_TYPE_CHOICES = [
    ("jobseeker", "Job Seeker"),
    ("business", "Business"),
    ("client", "Client"),
]


# Create your models here.
class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    role_description = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class BusinessProfile(models.Model):
    industries = models.CharField(
        max_length=255, blank=True, null=True
    )  # Allow null and blank
    company_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Allow null and blank
    company_type = models.CharField(
        max_length=255, blank=True, null=True
    )  # Allow null and blank
    scale = models.CharField(max_length=255, blank=True, null=True)  #
    company_size = models.CharField(max_length=255, blank=True, null=True)  #
    cin_no = models.CharField(
        max_length=21, blank=True, null=True
    )  # Allow null and blank
    gst_no = models.CharField(
        max_length=15, blank=True, null=True
    )  # Allow null and blank
    whatsapp_mobile_no = models.CharField(
        max_length=15, blank=True, null=True
    )  # Allow null and blank
    business_type = models.CharField(max_length=255, blank=True, null=True)
    location_link = models.URLField(blank=True, null=True)  # Allow null and blank
    address = models.CharField(blank=True, null=True)  # Allow null and blank
    google_plus_code = models.CharField(blank=True, null=True)  # Allow null and blank
    email_verified = models.BooleanField(default=False)
    whatsapp_verified = models.BooleanField(default=False)
    social_link = models.ManyToManyField(
        Socials, related_name="business_social_link", blank=True
    )
    website = models.ManyToManyField(
        Website, related_name="business_websites", blank=True
    )
    work_history = models.TextField(blank=True, null=True)  # Allow null and blank
    photo_showcase = models.URLField(blank=True, null=True)  # Allow null and blank
    video_showcase = models.URLField(blank=True, null=True)  # Allow null and blank
    project_brochures = models.FileField(
        upload_to=get_project_brochure_path, blank=True, null=True
    )  # Allow null and blank
    approved_friends_connections = models.ManyToManyField(
        CustomUser, related_name="approved_business_friends", blank=True
    )
    approved_influencer_connections = models.ManyToManyField(
        CustomUser, related_name="approved_business_influencers", blank=True
    )
    approved_company_connections = models.ManyToManyField(
        CustomUser, related_name="approved_business_companies", blank=True
    )
    approved_association_connections = models.ManyToManyField(
        CustomUser, related_name="approved_business_associations", blank=True
    )
    advertisement = models.TextField(blank=True, null=True)  # Allow null and blank


class JOBProfile(models.Model):
    passport_type_photo = models.ImageField(
        upload_to=get_passport_photo_path, blank=True, null=True
    )
    qualification = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    SEX_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    current_resident_address = models.TextField(blank=True, null=True)
    adhar_no = models.CharField(max_length=14, blank=True, null=True)
    adhar_verified = models.BooleanField(default=False)
    pan_no = models.CharField(max_length=10, blank=True, null=True)
    MARITAL_STATUS_CHOICES = (
        ("S", "Single"),
        ("M", "Married"),
        ("P", "Partnered"),
        ("W", "Widowed"),
    )
    marital_status = models.CharField(
        max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True, null=True
    )
    experience = models.ManyToManyField(
        Experience, related_name="experience", blank=True
    )
    anniversary_date = models.DateField(blank=True, null=True)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    children_count = models.PositiveIntegerField(blank=True, null=True)
    skills = models.ManyToManyField("Skill", blank=True)
    experience_months = models.PositiveIntegerField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    last_work_place = models.CharField(max_length=255, blank=True, null=True)
    reference_name = models.CharField(max_length=255, blank=True, null=True)
    reference_contact_no = models.CharField(max_length=15, blank=True, null=True)
    work_duration = models.CharField(max_length=255, blank=True, null=True)
    physical_fitness = models.ManyToManyField("PhysicalFitness", blank=True)
    work_challenges = models.ManyToManyField("WorkChallenge", blank=True)
    vision = models.ManyToManyField("Vision", blank=True)
    WORK_CHOICE_CHOICES = (("H", "Hourly"), ("D", "Daily"), ("M", "Monthly"))
    work_choice = models.CharField(
        max_length=1, choices=WORK_CHOICE_CHOICES, blank=True, null=True
    )
    expected_salary_hourly = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    expected_salary_daily = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    expected_salary_monthly = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    short_work_history = models.CharField(blank=True, null=True)
    work_history = models.TextField(blank=True, null=True)
    photo_showcase_description = models.TextField(blank=True, null=True)
    video_showcase_description = models.TextField(blank=True, null=True)
    approved_friends_connections = models.ManyToManyField(
        CustomUser, related_name="approved_friends", blank=True
    )
    approved_influencer_connections = models.ManyToManyField(
        CustomUser, related_name="approved_influencers", blank=True
    )
    approved_company_connections = models.ManyToManyField(
        CustomUser, related_name="approved_companies", blank=True
    )
    business_type = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone_no = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_place = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_relationship = models.CharField(
        max_length=255, blank=True, null=True
    )
    choice_of_work_place = models.ManyToManyField("WorkPlace", blank=True)
    looking_for_international = models.CharField(max_length=20, blank=True, null=True)
    passport_no = models.CharField(max_length=9, blank=True, null=True)
    medical_report = models.FileField(
        upload_to=get_medical_report_path, blank=True, null=True
    )
    insurance_policy_no = models.CharField(max_length=255, blank=True, null=True)
    insurance_company = models.CharField(max_length=255, blank=True, null=True)
    insurance_verified = models.BooleanField(default=False)
    insurance_policy_valid_upto = models.DateField(blank=True, null=True)
    if_not_buy_policy = models.BooleanField(default=False)
    get_membership = models.BooleanField(default=False)
    vehicle_owned = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    vehicle_usage = models.CharField(max_length=255, blank=True, null=True)
    vehicle_year = models.PositiveIntegerField(blank=True, null=True)
    vehicle_registration_no = models.CharField(max_length=255, blank=True, null=True)
    vehicle_insurance_policy_no = models.CharField(
        max_length=255, blank=True, null=True
    )
    vehicle_insurance_company = models.CharField(max_length=255, blank=True, null=True)
    vehicle_insurance_verified = models.BooleanField(default=False)
    vehicle_accident_policy_valid_upto = models.DateField(blank=True, null=True)
    vehicle_if_not_buy_policy = models.BooleanField(default=False)
    vehicle_get_membership = models.BooleanField(default=False)


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PhysicalFitness(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class WorkChallenge(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Vision(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class WorkPlace(models.Model):
    place = models.CharField(max_length=255)

    def __str__(self):
        return self.place


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo = models.ImageField(
        upload_to=get_profile_photo_path, blank=True, null=True
    )
    first_name = models.CharField(
        max_length=100, blank=True, null=True
    )  # Allow null and blank
    last_name = models.CharField(
        max_length=100, blank=True, null=True
    )  # Allow null and blank
    mid_name = models.CharField(
        max_length=30, blank=True, null=True
    )  # Allow null and blank
    address = models.TextField(blank=True, null=True)  # Allow null and blank
    pan_no = models.CharField(
        max_length=10, blank=True, null=True
    )  # Allow null and blank
    email = models.CharField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)  # Allow null and blank
    linkedin_link = models.URLField(blank=True, null=True)  # Allow null and blank
    other_social_link = models.URLField(blank=True, null=True)  # Allow null and blank
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL, null=True, blank=True
    )
    business_profile = models.ForeignKey(
        BusinessProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    job_profile = models.ForeignKey(
        JOBProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    social_link = models.ManyToManyField(
        Socials, related_name="profile_social_link", blank=True
    )
    website = models.ManyToManyField(
        Website, related_name="profile_websites", blank=True
    )
    work_history = models.TextField(blank=True, null=True)  # Allow null and blank
    photo_showcase = models.URLField(blank=True, null=True)  # Allow null and blank
    video_showcase = models.URLField(blank=True, null=True)  # Allow null and blank
    project_brochures = models.FileField(
        upload_to=get_project_brochure_path, blank=True, null=True
    )  # Allow null and blank
    approved_friends_connections = models.ManyToManyField(
        CustomUser, related_name="business_friends", blank=True
    )
    approved_influencer_connections = models.ManyToManyField(
        CustomUser, related_name="business_influencers", blank=True
    )
    approved_company_connections = models.ManyToManyField(
        CustomUser, related_name="business_companies", blank=True
    )
    approved_association_connections = models.ManyToManyField(
        CustomUser, related_name="business_associations", blank=True
    )
    advertisement = models.TextField(blank=True, null=True)  # Allow null and blank
    profile_type = models.CharField(
        max_length=20,
        choices=PROFILE_TYPE_CHOICES,
        default="jobseeker",
        blank=True,
        null=True,
    )
    unique_id = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def generate_unique_id(self):
        unique_id = get_random_string(length=8)
        self.unique_id = unique_id
        # self.save()

    def save(self, *args, **kwargs):
        # Generate short link if it doesn't exist
        if not self.unique_id:
            self.generate_unique_id()
        super().save(*args, **kwargs)

    def is_complete(self):
        """Check if essential fields are filled (first_name, last_name, mid_name)."""
        return all(
            [
                self.first_name,
                self.last_name,
                self.mid_name,
                self.address,
                self.phone,
                self.email,
            ]
        )

    def incomplete_fields(self):
        """Return a list of fields that are not completed."""
        fields = []
        if not self.first_name:
            fields.append("first name")
        if not self.last_name:
            fields.append("last name")

        return fields
