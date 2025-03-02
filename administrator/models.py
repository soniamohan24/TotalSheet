from django.db import models
from django.apps import apps
from ckeditor.fields import RichTextField


# Create your models here.

class WorkGroupSubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed SubGroup"
    
class Industry(models.Model):
    name = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )  # Allow null and blank
    description = RichTextField(blank=True, null=True)  # Allow null and blank
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the field to now when the object is created
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically set the field to now every time the object is saved
    workgroup_sub_groups = models.ManyToManyField(
        WorkGroupSubGroup, related_name="workgroup_sub_group", blank=True
    )

    def __str__(self):
        return self.name if self.name else "Unnamed Industry"

    def is_referenced(self):
        Code = apps.get_model("codes", "Code")
        return Code.objects.filter(industries=self.name).exists()
