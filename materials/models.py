from django.db import models
from projects.models import Project
from django.apps import apps
from django.db import models
from django.db.models import Sum
from django.db.models import FloatField, Sum
from django.db.models.functions import Cast
from ckeditor.fields import RichTextField

class SubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed SubGroup"


class BusinessSubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed SubGroup"
    
class CodesgroupSubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed SubGroup"    

class MaterialGroup(models.Model):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank
    logo = models.ImageField(upload_to="material_logos/", blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    sub_groups = models.ManyToManyField(SubGroup, related_name="materials", blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed MaterialGroup"

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return (
            self.material_group.exists()
            or self.materials_product_group.exists()
            or self.material_code_group.exists()
        )


class WorkGroup(models.Model):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank
    logo = models.ImageField(upload_to="workgroup_logos/", blank=True, null=True)
    description = RichTextField(blank=True, null=True)  # Allow null and blank
    codesgroup_sub_groups = models.ManyToManyField(
        CodesgroupSubGroup, related_name="codesgroup_sub_group", blank=True
    )
    

    def __str__(self):
        return self.name if self.name else "Unnamed WorkGroup"

    @property
    def code_count(self):
        """Count of Code instances related to this WorkGroup."""
        Code = apps.get_model("codes", "Code")
        return Code.objects.filter(group_name=self.name).count()

    def is_referenced(self):
        Code = apps.get_model("codes", "Code")
        return Code.objects.filter(group_name=self.name).exists()


class BusinessType(models.Model):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank
    business_sub_groups = models.ManyToManyField(
        BusinessSubGroup, related_name="business_sub_group", blank=True
    )

    def __str__(self):
        return self.name if self.name else "Unnamed BusinessType "

    def is_referenced(self):
        Code = apps.get_model("codes", "Code")
        return Code.objects.filter(group_name=self.name).exists()


class GST(models.Model):
    rate = models.FloatField(null=True, blank=True)


    def __str__(self):
        return str(self.rate) if self.rate not in [None, 0.0] else "0.00"

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return (
            self.code_material_gst.exists()
            or self.code_execution_gst.exists()
            or self.code_onsite_gst.exists()
            or self.code_offsite_gst.exists()
            or self.material_gst.exists()
            or self.product_gst.exists()
            or self.Contract_Margins_gst.exists()
            or self.Operational_Costs_gst.exists()
            or self.Operational_Costs_product_gst.exists()
            or self.Contract_Margins_product_gst.exists()
            or self.execution_gst.exists()
            or self.ex_gst.exists()
        )


class Brand(models.Model):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank
    logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)

    def is_referenced(self):
        return self.product_brand.exists() or self.material_brand.exists()

    def __str__(self):
        return self.name if self.name else "Unnamed Brand"

    def material_count(self):
        # Count how many times this brand is used in the Material model
        return Material.objects.filter(brand=self).count()

    def total_count(self):
        # Count how many times this brand is used in the Material model
        return Material.objects.all().count()


class Formula(models.Model):
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank

    def __str__(self):
        return self.name if self.name else "Unnamed Unit"

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return (
            self.contract_formula.exists()
            or self.operational_formula.exists()
            or self.contract_product_formula.exists()
            or self.total_operationcost_formula.exists()
        )


class Unit(models.Model):  # Assuming you have a Unit model
    name = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # Allow null and blank
    unit_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allow null and blank
    engineer_field = models.BooleanField(default=False)
    description = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Unit"

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return (
            self.code_material_unit.exists()
            or self.code_execution_unit.exists()
            or self.code_onsite_unit.exists()
            or self.code_offsite_unit.exists()
            or self.material_unit.exists()
            or self.product_unit.exists()
            or self.Contract_Margins_unit.exists()
            or self.Operational_Costs_unit.exists()
            or self.Operational_Costs_product_unit.exists()
            or self.Contract_Margins_product_unit.exists()
            or self.execution_unit.exists()
            or self.ex_unit.exists()
        )


class Material(models.Model):
    name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allow null and blank
    group = models.ForeignKey(
        MaterialGroup,
        on_delete=models.CASCADE,
        related_name="material_group",
        null=True,
        blank=True,
    )  # Allow null and blank
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="material_gst",
        null=True,
        blank=True,
    )
    subgroup = models.ForeignKey(
        SubGroup,
        on_delete=models.CASCADE,
        related_name="subgroup_material",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="material_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="material_brand",
        null=True,
        blank=True,
    )  # Allow null and blank
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
        return self.materials_name.exists() or self.code_materials_name.exists()

    def __str__(self):
        return self.name if self.name else "Unnamed Material"


class Material_Product(models.Model):
    name = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="materials_name",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        MaterialGroup,
        on_delete=models.CASCADE,
        related_name="materials_product_group",
        null=True,
        blank=True,
    )  # Allow null and blank
    gst = models.ForeignKey(
        GST, on_delete=models.CASCADE, related_name="product_gst", null=True, blank=True
    )
    gst_value = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="product_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="product_brand",
        null=True,
        blank=True,
    )  # Allow null and blank
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Allow null and blank
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="materials",
        null=True,
        blank=True,
    )

    # def __str__(self):U
    #     return self.name.name if self.name.name else "Unnamed Material"


class Contract_Margins(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="Contract_Margins_gst",
        null=True,
        blank=True,
    )
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="Contract_Margins_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="contract_formula",
        null=True,
        blank=True,
    )  # Allow null and blank

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return self.Contract_Margins.exists()

    def __str__(self):
        return self.name if self.name else "Unnamed Material"

    @classmethod
    def total_allow_me(cls):
        """Calculate the total of allow_me values, casting them to float."""
        total = cls.objects.aggregate(
            total=Sum(Cast("allow_me", FloatField()))  # Cast allow_me to float
        )
        return total["total"] if total["total"] is not None else 0.0


class Operational_Costs(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="Operational_Costs_gst",
        null=True,
        blank=True,
    )
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="Operational_Costs_unit",
        null=True,
        blank=True,
    )
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="operational_formula",
        null=True,
        blank=True,
    )  # Allow null and blank

    def __str__(self):
        return self.name if self.name else "Unnamed Material"

    def is_referenced(self):
        # Check if the GST instance is referenced in any of the related models
        return self.operational_costs.exists()

    @classmethod
    def total_allow_me(cls):
        """Calculate the total of allow_me values, casting them to float."""
        total = cls.objects.aggregate(
            total=Sum(Cast("allow_me", FloatField()))  # Cast allow_me to float
        )
        return total["total"] if total["total"] is not None else 0.0


class Contract_Margin_product(models.Model):
    name = models.ForeignKey(
        Contract_Margins,
        on_delete=models.CASCADE,
        related_name="Contract_Margins",
        null=True,
        blank=True,
    )
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="Contract_Margins_product_gst",
        null=True,
        blank=True,
    )
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="Contract_Margins_product_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    description = models.TextField()
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="contract_product_formula",
        null=True,
        blank=True,
    )  # Allow null and blank
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="projects_Contract_Margin",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name.name if self.name.name else "Unnamed Margin"


class Total_Operational_cost(models.Model):
    expense_name = models.CharField(max_length=255, default="ON & OFF-SITE EXPENSE")
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="total_operationcost_gst",
        null=True,
        blank=True,
    )
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="total_operationcost_unit",
        null=True,
        blank=True,
    )  # Allow null and blank
    description = models.TextField()
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="total_operationcost_formula",
        null=True,
        blank=True,
    )  # Allow null and blank
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="total_operationcost_Margin",
        null=True,
        blank=True,
    )
    # def __str__(self):
    #     return self.name.name if self.name.name else "Unnamed Margin"


class Operational_Cost_product(models.Model):
    name = models.ForeignKey(
        Operational_Costs,
        on_delete=models.CASCADE,
        related_name="operational_costs",
        null=True,
        blank=True,
    )
    gst = models.ForeignKey(
        GST,
        on_delete=models.CASCADE,
        related_name="Operational_Costs_product_gst",
        null=True,
        blank=True,
    )
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="Operational_Costs_product_unit",
        null=True,
        blank=True,
    )
    description = models.TextField()

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="projects_operational_cost",
        null=True,
        blank=True,
    )
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="operational_product_formula",
        null=True,
        blank=True,
    )  # Allow null and blank

    def __str__(self):
        return self.name.name if self.name.name else "Unnamed Material"
