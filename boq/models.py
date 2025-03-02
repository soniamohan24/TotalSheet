from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from materials.models import GST, Unit
from codes.models import Code
from projects.models import Project


class CustomUser(AbstractUser):
    # Your custom fields
    USER_TYPE_CHOICES = [
        ("admin", "Admin"),
        ("client", "Client"),
        ("projectuser", "ProjectUser"),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="projectuser",
        blank=True,
        null=True,
    )
    # Custom related names for groups and permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        related_name="custom_user_groups",  # Custom related name for groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        related_name="custom_user_permissions",  # Custom related name for user permissions
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Other required fields if any

    def __str__(self):
        return f"{self.username} "


class ClientInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_clients",
    )
    address = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    pan_no = models.CharField(max_length=10, blank=True, null=True)
    cin_no = models.CharField(
        max_length=21, blank=True, null=True
    )  # CIN number is usually 21 characters
    phone_no = models.CharField(
        max_length=15, blank=True, null=True
    )  # Adjust length as needed
    company_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    social_link = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["created_by", "user"],
                name="unique_client_per_creator"
            )
        ]

    def __str__(self):
        return f"{self.user}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or "No Name"

    def can_delete(self):
        """
        Check if the client can be deleted.
        The client cannot be deleted if they are associated with any active project.
        """
        # Check if the client is associated with any active project
        return not Project.objects.filter(client=self).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"





class OTP(models.Model):
    email = models.EmailField()
    otp_value = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(minutes=30)
        return self.created_at < expiration_time


class Floor(models.Model):
    boq = models.ForeignKey("BOQ", on_delete=models.CASCADE, related_name="floors")
    description = models.TextField(null=True, blank=True)
    table_name = models.CharField(max_length=100, null=True, blank=True)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.ForeignKey(
        Code, on_delete=models.CASCADE, null=True, blank=True, related_name="floor_code"
    )
    table_order = models.PositiveIntegerField(default=0)
    work_detail = models.CharField(max_length=255, null=True, blank=True)
    N = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    L = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    W = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    H = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    rate_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    full_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    basic_amount = models.CharField(max_length=255, null=True, blank=True)
    gst_applied = models.CharField(max_length=255, null=True, blank=True)
    gst_amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def select_unit(self):
    #     hasN = float(self.N if self.N else 0) > 0
    #     hasL = float(self.L if self.L else 0) > 0
    #     hasW = float(self.W if self.W else 0) > 0
    #     hasH = float(self.H if self.H else 0) > 0
    #
    #     count = 0
    #     if hasL:
    #         count += 1
    #     if hasN:
    #         count += 1
    #     if hasW:
    #         count += 1
    #     if hasH:
    #         count += 1
    #
    #     if count == 1:
    #         logicalUnit = "N"
    #     elif count == 2:
    #         logicalUnit = "M"
    #     elif count == 3:
    #         logicalUnit = "M2"
    #     elif count == 4:
    #         logicalUnit = "M3"
    #     else:
    #         logicalUnit = None
    #
    #     return Unit.objects.get(unit_name=logicalUnit) if logicalUnit else None

    def calculate_quantity(self):
        if self.N != 0 and self.L != 0 and self.W != 0 and self.H != 0:
            self.quantity = (
                float(self.N or 1)
                * float(self.L or 1)
                * float(self.W or 1)
                * float(self.H or 1)
            )
        else:
            self.quantity = 0
        return self.quantity

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        # self.unit = self.select_unit()

        if self.rate_per_unit and self.quantity:
            self.full_amount = float(self.rate_per_unit) * float(self.quantity)
        super().save(*args, **kwargs)


class WallMasonry(models.Model):
    boq = models.ForeignKey(
        "BOQ", on_delete=models.CASCADE, related_name="wall_masonries"
    )
    table_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    work_detail = models.CharField(max_length=255, null=True, blank=True)
    table_order = models.PositiveIntegerField(default=0)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    N = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    L = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    W = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    H = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def select_unit(self):
        hasN = float(self.N if self.N else 0) > 0
        hasL = float(self.L if self.L else 0) > 0
        hasW = float(self.W if self.W else 0) > 0
        hasH = float(self.H if self.H else 0) > 0

        count = 0
        if hasL:
            count += 1
        if hasN:
            count += 1
        if hasW:
            count += 1
        if hasH:
            count += 1

        if count == 1:
            logicalUnit = "N"
        elif count == 2:
            logicalUnit = "M"
        elif count == 3:
            logicalUnit = "M2"
        elif count == 4:
            logicalUnit = "M3"
        else:
            logicalUnit = None

        return Unit.objects.get(unit_name=logicalUnit) if logicalUnit else None

    def calculate_quantity(self):
        if self.N != 0 and self.L != 0 and self.W != 0 and self.H != 0:
            self.quantity = (
                float(self.N or 1)
                * float(self.L or 1)
                * float(self.W or 1)
                * float(self.H or 1)
            )
        else:
            self.quantity = 0
        return self.quantity

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        super().save(*args, **kwargs)


class Finishing(models.Model):
    boq = models.ForeignKey("BOQ", on_delete=models.CASCADE, related_name="finishings")
    description = models.TextField(null=True, blank=True)
    table_name = models.CharField(max_length=100, null=True, blank=True)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    free_code = models.CharField(max_length=255, null=True, blank=True)
    work_detail = models.CharField(max_length=255, null=True, blank=True)
    table_order = models.PositiveIntegerField(default=0)
    basic_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    full_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    full_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    basic_amount = models.CharField(max_length=255, null=True, blank=True)
    gst_applied = models.CharField(max_length=255, null=True, blank=True)
    gst_amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.pk)


class ContractWork(models.Model):
    boq = models.ForeignKey(
        "BOQ", on_delete=models.CASCADE, related_name="contract_works"
    )
    table_name = models.CharField(max_length=100, null=True, blank=True)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    external_work = models.CharField(max_length=255, null=True, blank=True)
    work_detail = models.CharField(max_length=255, null=True, blank=True)
    table_order = models.PositiveIntegerField(default=0)
    work_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    ratio_owv = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, null=True, blank=True)
    full_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    basic_amount = models.CharField(max_length=255, null=True, blank=True)
    gst_applied = models.CharField(max_length=255, null=True, blank=True)
    gst_amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AbstractForm(models.Model):
    boq = models.ForeignKey("BOQ", on_delete=models.CASCADE, related_name="abs_form")
    form_name = models.CharField(max_length=50, null=True, blank=True)
    table_name = models.CharField(max_length=100, null=True, blank=True)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    table_order = models.PositiveIntegerField(default=0)
    work_detail = models.TextField(null=True, blank=True)
    value_excluding_gst = models.CharField(max_length=20, null=True, blank=True)
    gst = models.ForeignKey(
        GST, on_delete=models.CASCADE, related_name="abs_gst", null=True, blank=True
    )
    ratio = models.CharField(max_length=100, null=True, blank=True)
    full_amount = models.CharField(max_length=50, null=True, blank=True)
    basic_amount = models.CharField(max_length=255, null=True, blank=True)
    gst_applied = models.CharField(max_length=255, null=True, blank=True)
    gst_amount = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReportForm(models.Model):
    boq = models.ForeignKey("BOQ", on_delete=models.CASCADE, related_name="report_form")
    form_name = models.CharField(max_length=50, null=True, blank=True)
    table_name = models.CharField(max_length=100, null=True, blank=True)
    table_heading_name = models.CharField(max_length=100, null=True, blank=True)
    table_order = models.PositiveIntegerField(default=0)
    gst_to_be_paid = models.CharField(max_length=50, null=True, blank=True)
    gst_refund = models.CharField(max_length=255, null=True, blank=True)
    gst_to_be_collected = models.CharField(max_length=255, null=True, blank=True)
    gst_to_be_paid_per = models.CharField(max_length=50, null=True, blank=True)
    gst_refund_per = models.CharField(max_length=255, null=True, blank=True)
    total_amount=models.CharField(max_length=255, null=True, blank=True)
    gst_to_be_collected_per = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BOQ(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="boq_project",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    boq_name = models.CharField(null=True, blank=True)
    basic_amount = models.CharField(max_length=255, null=True, blank=True)
    gst_applied = models.CharField(max_length=255, null=True, blank=True)
    gst_amount = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.project.name) if self.project else "N/A"


class Total(models.Model):
    boq = models.ForeignKey(
        "BOQ", on_delete=models.CASCADE, null=True, blank=True
    )  # Link to BOQ
    table_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Table name (e.g., Floor, Wall)
    full_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )  # Full total amount
    basic_amount = models.CharField(
        max_length=100, null=True, blank=True
    )  # Basic amount
    gst_applied = models.CharField(max_length=100, null=True, blank=True)  # GST applied
    gst_amount = models.CharField(max_length=100, null=True, blank=True)  # GST amount
    code = models.ForeignKey(
        "codes.Code",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="walltable_code",
    )  # Code reference
    quantity = models.CharField(
        max_length=100, null=True, blank=True
    )  # Quantity of materials/work
    unit = models.ForeignKey(
        "materials.Unit", on_delete=models.CASCADE, null=True, blank=True
    )  # Unit reference
    rate_per_unit = models.CharField(
        max_length=100, null=True, blank=True
    )  # Rate per unit
    ratio = models.CharField(max_length=100, null=True, blank=True)  # Ratio

    class Meta:
        unique_together = [
            "boq",
            "table_name",
        ]  # Ensure a unique total per BOQ and table

    def __str__(self):
        return f"Total for BOQ {self.boq.id} - {self.table_name}: {self.full_amount}"
