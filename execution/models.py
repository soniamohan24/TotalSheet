from django.db import models
from materials.models import *
from ckeditor.fields import RichTextField

class ExecutionSubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed SubGroup"


class ExecutionGroup(models.Model):
    name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allow null and blank
    logo = models.ImageField(upload_to="execution_logos/", blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    sub_groups = models.ManyToManyField(
        ExecutionSubGroup, related_name="execution_subgroup", blank=True
    )

    def is_referenced(self):
        return (
            self.execution_group.exists()
            or self.execution_product_group.exists()
            or self.execution_code_group.exists()
        )

    def __str__(self):
        return self.name if self.name else "Unnamed ExecutionGroup"


class Execution(models.Model):
    name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allow null and blank
    group = models.ForeignKey(
        ExecutionGroup,
        on_delete=models.CASCADE,
        related_name="execution_group",
        null=True,
        blank=True,
    )  # Allow null and blank
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="execution_gst",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="execution_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    subgroup = models.ForeignKey(
        ExecutionSubGroup,
        on_delete=models.CASCADE,
        related_name="subgroup_execution",
        null=True,
        blank=True,
    )
    description = RichTextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Allow null and blank
    gst_value = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Allow null and blank
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Allow null and blank

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return self.execution_product_name.exists() or self.code_execution_name.exists()

    def __str__(self):
        return self.name if self.name else "Unnamed Material"


class Execution_Product(models.Model):
    name = models.ForeignKey(
        Execution,
        on_delete=models.CASCADE,
        related_name="execution_product_name",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        ExecutionGroup,
        on_delete=models.CASCADE,
        related_name="execution_product_group",
        null=True,
        blank=True,
    )
    gst = models.ForeignKey(
        "materials.GST",
        on_delete=models.CASCADE,
        related_name="ex_gst",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        "materials.Unit",
        on_delete=models.CASCADE,
        related_name="ex_unit",
        null=True,
        blank=True,
    )
    gst_value = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="execution_project",
        null=True,
        blank=True,
    )

    # def __str__(self):
    #     return self.name.name if self.name.name else "Unnamed Product"
