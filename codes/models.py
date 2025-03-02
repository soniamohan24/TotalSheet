from django.db import models
from materials.models import Unit,Material_Product,GST, MaterialGroup,Material,Formula
from execution.models import Execution_Product,ExecutionGroup,Execution


CODE_TYPE_CHOICES = (
    ('default_code', 'default_code'),
    ('draft_code', 'draft_code'),
    ('used_boq_code', 'used_boq_code'),

)

class code_Material(models.Model):
    group = models.ForeignKey(
        MaterialGroup,
        on_delete=models.CASCADE,
        related_name="material_code_group",
        null=True,
        blank=True,
    )  # Allow null and blank

    material_name = models.CharField(max_length=100, null=True, blank=True) # will remove once change in system this to mat_name
    mat_name = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="code_materials_name",
        null=True,
        blank=True,
    )
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, related_name='code_material_gst', null=True,blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='code_material_unit', null=True,blank=True)
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Required=models.CharField(max_length=100, null=True, blank=True)
    basic_value=models.CharField(max_length=100, null=True, blank=True)
    gst_value=models.CharField(max_length=100, null=True, blank=True)
    sub_total=models.CharField(max_length=100, null=True, blank=True)
    is_used=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group} - {self.material_name}" if self.material_name else f"{self.group} - {self.mat_name}"
class code_Execution(models.Model):
    group = models.ForeignKey(
        ExecutionGroup,
        on_delete=models.CASCADE,
        related_name="execution_code_group",
        null=True,
        blank=True,
    )
    execution_name = models.CharField(max_length=100, null=True, blank=True)# will remove once change in system this to ex_name
    ex_name = models.ForeignKey(
        Execution,
        on_delete=models.CASCADE,
        related_name="code_execution_name",
        null=True,
        blank=True,
    )
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, related_name='code_execution_gst', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='code_execution_unit', null=True, blank=True)
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    need = models.CharField(max_length=100, null=True, blank=True)
    basic_value = models.CharField(max_length=100, null=True, blank=True)
    gst_value = models.CharField(max_length=100, null=True, blank=True)
    sub_total = models.CharField(max_length=100, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.execution_name) if self.execution_name else "Unnamed Execution"

class code_OnSiteExpense(models.Model):
    onsite_expense_name = models.CharField(max_length=100, null=True, blank=True)
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, related_name='code_onsite_gst', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='code_onsite_unit', null=True, blank=True)
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="onsideexpense_formula",
        null=True,
        blank=True,
    )  # Allow null and blank
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', null=True,blank=True)
    on_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    allow_me = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    basic_value = models.CharField(max_length=100, null=True, blank=True)
    gst_value = models.CharField(max_length=100, null=True, blank=True)
    sub_total = models.CharField(max_length=100, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.onsite_expense_name) if self.onsite_expense_name else "Unnamed Onsite Exepense"
    
class code_OffSiteExpense(models.Model):
    offsite_expense_name = models.CharField(max_length=100, null=True, blank=True)
    gst = models.ForeignKey(GST, on_delete=models.CASCADE, related_name='code_offsite_gst', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='code_offsite_unit', null=True, blank=True)
    formula = models.ForeignKey(
        Formula,
        on_delete=models.CASCADE,
        related_name="offsideexpense_formula",
        null=True,
        blank=True,
    )  # Allow null and blank
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand', null=True,blank=True)
    on_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    i_need = models.CharField(max_length=100, null=True, blank=True)
    basic_value = models.CharField(max_length=100, null=True, blank=True)
    gst_value = models.CharField(max_length=100, null=True, blank=True)
    sub_total = models.CharField(max_length=100, null=True, blank=True)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return str(self.offsite_expense_name) if self.offsite_expense_name else "Unnamed Onsite Expense"
    
class Code(models.Model):
    industries = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    group_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    subgroup_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    material_code = models.CharField(max_length=100, null=True, blank=True)
    execution_code= models.CharField(max_length=100, null=True, blank=True)
    creator_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    created_by=models.ForeignKey('boq.CustomUser', on_delete=models.CASCADE, related_name='code_created_by',null=True, blank=True)
    date = models.DateField(null=True, blank=True)  # Allow null and blank
    code_preview = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    design_for = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    unit = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    basic_value = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    gst_value = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    gst_per = models.CharField(max_length=100, null=True, blank=True)
    grand_total = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank
    description = models.TextField(max_length=100, null=True, blank=True)  # Allow null and blank
    note = models.TextField(blank=True, null=True)  # Allow null and blank
    code_material = models.ManyToManyField(code_Material, related_name='material_codes', blank=True)  # Allow blank
    code_execution = models.ManyToManyField(code_Execution, related_name='execution_codes', blank=True)  # Allow blank
    onsite_expense = models.ManyToManyField(code_OnSiteExpense, related_name='onsite_codes', blank=True)  # Allow blank
    offsite_expense = models.ManyToManyField(code_OffSiteExpense, related_name='offsite_codes', blank=True)  # Allow blank
    code_type = models.CharField(max_length=100, choices=CODE_TYPE_CHOICES, blank=True, null=True)
    material_total_rate= models.CharField(max_length=100, null=True, blank=True)
    material_total_basicvalue = models.CharField(max_length=100, null=True, blank=True)
    material_total_gstvalue = models.CharField(max_length=100, null=True, blank=True)
    material_total_gst = models.CharField(max_length=100, null=True, blank=True)
    material_subtotal = models.CharField(max_length=100, null=True, blank=True)
    execution_total_rate = models.CharField(max_length=100, null=True, blank=True)
    execution_total_basicvalue = models.CharField(max_length=100, null=True, blank=True)
    execution_total_gstvalue = models.CharField(max_length=100, null=True, blank=True)
    execution_total_gst = models.CharField(max_length=100, null=True, blank=True)
    execution_subtotal = models.CharField(max_length=100, null=True, blank=True)
    margin_totalrate=models.CharField(max_length=100, null=True, blank=True)
    margin_total_basicvalue=models.CharField(max_length=100, null=True, blank=True)
    margin_total_gst = models.CharField(max_length=100, null=True, blank=True)
    margin_total_gst_value = models.CharField(max_length=100, null=True, blank=True)
    margin_subtotal=models.CharField(max_length=100, null=True, blank=True)
    operational_cost_totalrate = models.CharField(max_length=100, null=True, blank=True)
    operational_cost_basicvalue = models.CharField(max_length=100, null=True, blank=True)
    operational_cost_subtotal = models.CharField(max_length=100, null=True, blank=True)
    operational_cost_gst = models.CharField(max_length=100, null=True, blank=True)
    operational_cost_gst_value = models.CharField(max_length=100, null=True, blank=True)
    op_allowme= models.CharField(max_length=100, null=True, blank=True)
    margin_allowme = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.code_preview) if self.code_preview else "Unnamed Code"

    def duplicate(self):
        # Create a duplicate of the current instance, excluding Many-to-Many relationships
        new_code = Code.objects.create(
            industries=self.industries,
            group_name=self.group_name,
            subgroup_name=self.subgroup_name,
            material_code=self.material_code,
            execution_code=self.execution_code,
            creator_name=self.creator_name,
            created_by=self.created_by,
            date=timezone.now(),  # Set to current date or copy from the original
            code_preview=self.code_preview,
            design_for=self.design_for,
            unit=self.unit,
            basic_value=self.basic_value,
            gst_value=self.gst_value,
            gst_per=self.gst_per,
            grand_total=self.grand_total,
            description=self.description,
            note=self.note,
            code_type=self.code_type,
            material_total_rate=self.material_total_rate,
            material_total_basicvalue=self.material_total_basicvalue,
            material_total_gstvalue=self.material_total_gstvalue,
            material_total_gst=self.material_total_gst,
            material_subtotal=self.material_subtotal,
            execution_total_rate=self.execution_total_rate,
            execution_total_basicvalue=self.execution_total_basicvalue,
            execution_total_gstvalue=self.execution_total_gstvalue,
            execution_total_gst=self.execution_total_gst,
            execution_subtotal=self.execution_subtotal,
            margin_totalrate=self.margin_totalrate,
            margin_total_basicvalue=self.margin_total_basicvalue,
            margin_total_gst=self.margin_total_gst,
            margin_total_gst_value=self.margin_total_gst_value,
            margin_subtotal=self.margin_subtotal,
            operational_cost_totalrate=self.operational_cost_totalrate,
            operational_cost_basicvalue=self.operational_cost_basicvalue,
            operational_cost_subtotal=self.operational_cost_subtotal,
            operational_cost_gst=self.operational_cost_gst,
            operational_cost_gst_value=self.operational_cost_gst_value
        )

        # Duplicate Many-to-Many relationships without creating new records
        new_code.code_material.set(self.code_material.all())
        new_code.code_execution.set(self.code_execution.all())
        new_code.onsite_expense.set(self.onsite_expense.all())
        new_code.offsite_expense.set(self.offsite_expense.all())

        return new_code