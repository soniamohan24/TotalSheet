# utils.py
from django.apps import apps
from django.urls import reverse
from .forms import *  # Import your forms here

# Define the mappings for models, forms, and templates
MODEL_CONFIGS = {
    "material_group": {
        "model": "materials.MaterialGroup",
        "form": MaterialGroupForm,
        "templates": {
            "create": "administrator/material_group.html",
            "update": "administrator/material_group.html",
            "delete": "administrator/material_group.html",
            "detail": "administrator/material_group.html",
            "list": "administrator/material_group.html",
        },
    },
    "execution_group": {
        "model": "execution.ExecutionGroup",
        "form": ExecutionGroupForm,
        "templates": {
            "create": "administrator/execution_group.html",
            "update": "administrator/execution_group.html",
            "delete": "administrator/execution_group.html",
            "detail": "administrator/execution_group.html",
            "list": "administrator/execution_group.html",
        },
    },
    "brand": {
        "model": "materials.Brand",
        "form": BrandForm,
        "templates": {
            "create": "administrator/brands.html",
            "update": "administrator/brands.html",
            "delete": "administrator/brands.html",
            "detail": "administrator/brands.html",
            "list": "administrator/brands.html",
        },
    },
    "gst": {
        "model": "materials.GST",
        "form": GstForm,
        "templates": {
            "create": "administrator/gst.html",
            "update": "administrator/gst.html",
            "delete": "administrator/gst.html",
            "detail": "administrator/gst.html",
            "list": "administrator/gst.html",
        },
    },
    "unit": {
        "model": "materials.Unit",
        "form": UnitForm,
        "templates": {
            "create": "administrator/unit.html",
            "update": "administrator/unit.html",
            "delete": "administrator/unit.html",
            "detail": "administrator/unit.html",
            "list": "administrator/unit.html",
        },
    },
    "workgroup": {
        "model": "materials.WorkGroup",
        "form": WorkGroupForm,
        "templates": {
            "create": "administrator/workgroup.html",
            "update": "administrator/workgroup.html",
            "delete": "administrator/workgroup.html",
            "detail": "administrator/workgroup.html",
            "list": "administrator/workgroup.html",
        },
    },
    "businesstype": {
        "model": "materials.BusinessType",
        "form": BusinessTypeForm,
        "templates": {
            "create": "administrator/business_type.html",
            "update": "administrator/business_type.html",
            "delete": "administrator/business_type.html",
            "detail": "administrator/business_type.html",
            "list": "administrator/business_type.html",
        },
    },
    "material": {
        "model": "materials.Material",
        "form": MaterialForm,
        "templates": {
            "create": "administrator/material.html",
            "update": "administrator/material.html",
            "delete": "administrator/material.html",
            "detail": "administrator/material.html",
            "list": "administrator/material.html",
        },
    },
    "execution": {
        "model": "execution.Execution",
        "form": ExecutionForm,
        "templates": {
            "create": "administrator/execution.html",
            "update": "administrator/execution.html",
            "delete": "administrator/execution.html",
            "detail": "administrator/execution.html",
            "list": "administrator/execution.html",
        },
    },
    "operationalcost": {
        "model": "materials.Operational_Costs",
        "form": OperationalCost,
        "templates": {
            "create": "administrator/operation_cost.html",
            "update": "administrator/operation_cost.html",
            "delete": "administrator/operation_cost.html",
            "detail": "administrator/operation_cost.html",
            "list": "administrator/operation_cost.html",
        },
    },
    "formula": {
        "model": "materials.Formula",
        "form": FormulaForm,
        "templates": {
            "create": "administrator/formula.html",
            "update": "administrator/formula.html",
            "delete": "administrator/formula.html",
            "detail": "administrator/formula.html",
            "list": "administrator/formula.html",
        },
    },
    "contractmargin": {
        "model": "materials.Contract_Margins",
        "form": ContractMargin,
        "templates": {
            "create": "administrator/contract_margin.html",
            "update": "administrator/contract_margin.html",
            "delete": "administrator/contract_margin.html",
            "detail": "administrator/contract_margin.html",
            "list": "administrator/contract_margin.html",
        },
    },
    "industry": {
        "model": "administrator.Industry",
        "form": IndustryForm,
        "templates": {
            "create": "administrator/industries.html",
            "update": "administrator/industries.html",
            "delete": "administrator/industries.html",
            "detail": "administrator/industries.html",
            "list": "administrator/industries.html",
        },
    },
    # Add more model configurations here
}


def get_model_class(model_name):
    """Return the model class based on the model name."""
    model_path = MODEL_CONFIGS[model_name]["model"]

    return apps.get_model(model_path)


def get_form_class(model_name):
    """Return the form class based on the model name."""
    return MODEL_CONFIGS[model_name]["form"]


def get_template_name(action, model_name):
    """Return the template name based on the action and model name."""
    return MODEL_CONFIGS[model_name]["templates"][action]


def get_model_fields(model_name):
    """Return model fields based on the model name."""
    model_class = get_model_class(model_name)
    return {field.name: field.verbose_name for field in model_class._meta.fields}
