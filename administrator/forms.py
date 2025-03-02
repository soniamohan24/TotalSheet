# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from materials.models import *
from execution.models import *
from administrator.models import *


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username..."}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "*******"}
        )
    )


class MaterialGroupForm(forms.ModelForm):
    class Meta:
        model = MaterialGroup
        fields = ["name", "logo", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if MaterialGroup.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError(
                    "A material group with this name already exists."
                )
        else:
            # If creating a new instance, check for any existing brand with the same name
            if MaterialGroup.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "A material group with this name already exists."
                )

        return name


class ExecutionGroupForm(forms.ModelForm):
    class Meta:
        model = ExecutionGroup
        fields = ["name", "logo", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if (
                ExecutionGroup.objects.filter(name=name)
                .exclude(pk=instance.pk)
                .exists()
            ):
                raise forms.ValidationError(
                    "A execution group with this name already exists."
                )
        else:
            # If creating a new instance, check for any existing brand with the same name
            if ExecutionGroup.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "A execution group with this name already exists."
                )

        return name


class FormulaForm(forms.ModelForm):
    class Meta:
        model = Formula
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if Formula.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A formula with this name already exists.")
        else:
            # If creating a new instance, check for any existing brand with the same name
            if Formula.objects.filter(name=name).exists():
                raise forms.ValidationError("A formula with this name already exists.")

        return name


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "logo", "website_url"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if Brand.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A brand with this name already exists.")
        else:
            # If creating a new instance, check for any existing brand with the same name
            if Brand.objects.filter(name=name).exists():
                raise forms.ValidationError("A brand with this name already exists.")

        return name


class GstForm(forms.ModelForm):
    class Meta:
        model = GST
        fields = ["rate"]

    def clean_rate(self):
        rate = self.cleaned_data.get("rate")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if GST.objects.filter(rate=rate).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A GST with this rate already exists.")
        else:
            # If creating a new instance, check for any existing GST with the same rate
            if GST.objects.filter(rate=rate).exists():
                raise forms.ValidationError("A GST with this rate already exists.")

        return rate


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "unit_name", "engineer_field", "description"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if Unit.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A unit with this name already exists.")
        else:
            # If creating a new instance, check for any existing unit with the same name
            if Unit.objects.filter(name=name).exists():
                raise forms.ValidationError("A unit with this name already exists.")

        return name


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if Industry.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A industry with this name already exists.")
        else:
            # If creating a new instance, check for any existing unit with the same name
            if Industry.objects.filter(name=name).exists():
                raise forms.ValidationError("A industry with this name already exists.")

        return name


class GroupForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        # If updating an existing instance, exclude it from the duplicate check
        if instance and instance.pk:
            if Industry.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A industry with this name already exists.")
        else:
            # If creating a new instance, check for any existing unit with the same name
            if Industry.objects.filter(name=name).exists():
                raise forms.ValidationError("A industry with this name already exists.")

        return name


class WorkGroupForm(forms.ModelForm):
    class Meta:
        model = WorkGroup
        fields = ["name", "logo", "description"]    

    def clean_rate(self):
        rate = self.cleaned_data.get("rate")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate rates, excluding the current instance
            if GST.objects.filter(rate=rate).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A GST with this rate already exists.")
        else:
            # Check for duplicate rates when creating a new instance
            if GST.objects.filter(rate=rate).exists():
                raise forms.ValidationError("A GST with this rate already exists.")

        return rate


class BusinessTypeForm(forms.ModelForm):
    class Meta:
        model = BusinessType
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate names, excluding the current instance
            if BusinessType.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError(
                    "A BusinessType with this name already exists."
                )
        else:
            # Check for duplicate names when creating a new instance
            if BusinessType.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "A BusinessType with this name already exists."
                )

        return name


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "name",
            "group",
            "gst",
            "unit",
            "brand",
            "price",
            "gst_value",
            "sale_price",
            "subgroup",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate names, excluding the current instance
            if Material.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError("A Material with this name already exists.")
        else:
            # Check for duplicate names when creating a new instance
            if Material.objects.filter(name=name).exists():
                raise forms.ValidationError("A Material with this name already exists.")

        return name


class ExecutionForm(forms.ModelForm):
    class Meta:
        model = Execution
        fields = ["name", "group", "gst", "unit", "price", "gst_value", "sale_price", "subgroup",]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate names, excluding the current instance
            if Execution.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise forms.ValidationError(
                    "An Execution with this name already exists."
                )
        else:
            # Check for duplicate names when creating a new instance
            if Execution.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "An Execution with this name already exists."
                )

        return name


class OperationalCost(forms.ModelForm):
    class Meta:
        model = Operational_Costs
        fields = ["name", "allow_me", "gst", "unit", "formula"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate names, excluding the current instance
            if (
                Operational_Costs.objects.filter(name=name)
                .exclude(pk=instance.pk)
                .exists()
            ):
                raise forms.ValidationError(
                    "An Operational Cost with this name already exists."
                )
        else:
            # Check for duplicate names when creating a new instance
            if Operational_Costs.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "An Operational Cost with this name already exists."
                )

        return name


class ContractMargin(forms.ModelForm):
    class Meta:
        model = Contract_Margins
        fields = ["name", "allow_me", "gst", "unit", "formula"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        # Get the current instance
        instance = getattr(self, "instance", None)

        if instance and instance.pk:
            # Check for duplicate names, excluding the current instance
            if (
                Contract_Margins.objects.filter(name=name)
                .exclude(pk=instance.pk)
                .exists()
            ):
                raise forms.ValidationError(
                    "A Contract Margin with this name already exists."
                )
        else:
            # Check for duplicate names when creating a new instance
            if Contract_Margins.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    "A Contract Margin with this name already exists."
                )

        return name
