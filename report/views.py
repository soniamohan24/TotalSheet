from django.shortcuts import render
from django.shortcuts import render, redirect
from projects.models import Project
from codes.models import *
from boq.models import *
from materials.models import *
from django.db.models.functions import Replace, Lower
from django.db.models import Value
from django.views.generic import UpdateView, TemplateView, View, DeleteView, CreateView


# Create your views here.
class ReportView(TemplateView):
    template_name = "dashboards/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("pk")

        if not project_id:
            return context
        # Fetch Floor and Total querysets and exclude null codes
        floors = Floor.objects.filter(boq__project=project_id).exclude(
            code__isnull=True
        )
        totals = Total.objects.filter(boq__project=project_id).exclude(
            code__isnull=True
        )
        # Extract code IDs from the querysets
        floor_code_ids = floors.values_list("code_id", flat=True)
        total_code_ids = totals.values_list("code_id", flat=True)
        # Merge code IDs and remove duplicates
        merged_code_ids = set(floor_code_ids) | set(total_code_ids)
        # Fetch Code instances using the merged code IDs
        codes = Code.objects.filter(id__in=merged_code_ids)

        # Get the related code_material instances
        code_materials = code_Material.objects.filter(
            id__in=codes.values_list("code_material", flat=True).distinct()
        )

        # Create a dictionary to aggregate material_name and ratio values
        material_aggregation = {}

        for cm in code_materials:
            if cm.mat_name:
                material_name = cm.mat_name.name
                if material_name not in material_aggregation:
                    # Fetch Material_Product details
                    material_product = Material_Product.objects.filter(
                        name=cm.mat_name, project=project_id
                    ).first()
                    # Initialize dictionary entry
                    material_aggregation[material_name] = {
                        "quantity": 0,
                        "rate": (
                            float(material_product.price) if material_product else 0
                        ),
                        "gst": (
                            float(material_product.gst_value)
                            if material_product
                            and material_product.gst_value is not None
                            else 0
                        ),
                        "unit": (
                            material_product.unit.name
                            if material_product
                            and material_product.unit
                            and material_product.unit.name
                            else "N/A"
                        ),
                    }
                # Update the quantity
                material_aggregation[material_name]["quantity"] += float(
                    cm.Required or 0
                )
        print(material_aggregation)
        code_materials = code_Material.objects.filter(
            id__in=codes.values_list("code_material", flat=True).distinct()
        )

        # Create a dictionary to aggregate material_name and ratio values
        material_aggregation = {}

        for cm in code_materials:
            if cm.mat_name:
                material_name = cm.mat_name.name
                if material_name not in material_aggregation:
                    # Fetch Material_Product details
                    material_product = Material_Product.objects.filter(
                        name=cm.mat_name, project=project_id
                    ).first()
                    # Initialize dictionary entry
                    material_aggregation[material_name] = {
                        "quantity": 0,
                        "rate": (
                            float(material_product.price) if material_product else 0
                        ),
                        "gst": (
                            float(material_product.gst.rate)
                            if material_product
                            and material_product.gst.rate is not None
                            else 0
                        ),
                        "unit": (
                            material_product.unit.name
                            if material_product
                            and material_product.unit
                            and material_product.unit.name
                            else "N/A"
                        ),
                    }
                # Update the quantity
                material_aggregation[material_name]["quantity"] += float(
                    cm.Required or 0
                )
        print(material_aggregation)
        code_executions = code_Execution.objects.filter(
            id__in=codes.values_list("code_execution", flat=True).distinct()
        )
        execution_aggregation = {}
        for cm in code_executions:
            if cm.ex_name:
                execution_name = cm.ex_name.name
                if execution_name not in execution_aggregation:
                    execution_product = Execution_Product.objects.filter(
                        name=cm.ex_name, project=project_id
                    ).first()
                    execution_aggregation[execution_name] = {
                        "quantity": 0,
                        "rate": (
                            float(execution_product.price) if execution_product else 0
                        ),
                        "gst": (
                            float(execution_product.gst.rate)
                            if execution_product
                            and execution_product.gst
                            and execution_product.gst.rate is not None
                            else 0
                        ),
                        "unit": (
                            execution_product.unit.name
                            if execution_product
                            and execution_product.unit
                            and execution_product.unit.name
                            else "N/A"
                        ),
                    }
                # Update the quantity
                execution_aggregation[execution_name]["quantity"] += float(cm.need or 0)
        # Add project and aggregated data to context
        project_obj = Project.objects.get(pk=project_id)
        operational_cost = Total_Operational_cost.objects.filter(project=project_id)
        management_margin = code_OffSiteExpense.objects.filter(
            id__in=codes.values_list("offsite_expense", flat=True).distinct()
        )
        print(management_margin)
        management_aggregation = {}
        for cm in management_margin:
            if cm.offsite_expense_name:
                onmargin_name = cm.offsite_expense_name
                print(onmargin_name, "ftg")
                # Contract_Margins.objects.filter(name=onmargin_name)
                if onmargin_name not in management_aggregation:
                    normalized_name = onmargin_name.replace("-", "").lower()
                    matching_margin = (
                        Contract_Margins.objects.annotate(
                            normalized_name=Lower(
                                Replace("name", Value("-"), Value(""))
                            )
                        )
                        .filter(normalized_name=normalized_name)
                        .first()
                    )
                    print(matching_margin.pk)
                    management_product = Contract_Margin_product.objects.filter(
                        name=matching_margin.pk,  # Use the primary key of the matching object
                        project=project_id,
                    ).first()
                    print(management_product, "product")
                    management_aggregation[onmargin_name] = {
                        "allow_me": (
                            management_product.allow_me if management_product else 0
                        ),
                        "gst": (
                            float(management_product.gst.rate)
                            if management_product.gst
                            and management_product.gst is not None
                            else 0
                        ),
                        "unit": (
                            management_product.unit.name
                            if onmargin_name
                            and management_product.unit
                            and management_product.unit.name
                            else "N/A"
                        ),
                        "formula": (
                            management_product.formula.name
                            if management_product
                            and management_product.formula
                            and management_product.formula.name
                            else "N/A"
                        ),
                    }
        print(management_aggregation)
        context["project"] = project_obj
        context["pk"] = project_id
        context["boq"] = list(floors) + list(totals)  # Merge lists after processing
        context["material_aggregation"] = (
            material_aggregation  # Add aggregated data to context
        )
        context["execution_aggregation"] = execution_aggregation
        context["operational_cost"] = operational_cost
        context["management_aggregation"] = management_aggregation

        return context
