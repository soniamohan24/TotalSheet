from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=255, null=True, blank=True
    )  # Allow null and blank
    description = models.TextField(blank=True, null=True)  # Allow null and blank
    project_type = models.CharField(max_length=255, null=True, blank=True)
    interior_project_photo = models.ImageField(
        upload_to="photos/", null=True, blank=True
    )
    exterior_project_photo = models.ImageField(
        upload_to="photos", null=True, blank=True
    )
    # project_photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    project_brocher = models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    place = models.CharField(max_length=255, null=True, blank=True)
    webside = models.CharField(max_length=255, null=True, blank=True)
    location_link = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(
        "boq.ClientInfo",
        on_delete=models.CASCADE,
        related_name="client_user",
        null=True,
        blank=True,
    )

    construction_area = models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    building_license_no = models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    Building_rera_license = models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    drawings = models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    documents= models.FileField(
        upload_to="construction_files/", null=True, blank=True
    )
    social_link = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Add updated_at field
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        "boq.CustomUser", on_delete=models.CASCADE
    )  # Add user field

    def __str__(self):
        return self.name if self.name else "Unnamed Project"
