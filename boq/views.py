from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from materials.models import *
from execution.models import *
from projects.models import Project
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from administrator.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from materials.models import Material, MaterialGroup, Unit, GST
from codes.models import *
from django.http import JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
from .models import (
    BOQ,
    Floor,
    WallMasonry,
    Finishing,
    ContractWork,
    AbstractForm,
    Total,
)
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json, time
from collections import defaultdict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.apps import apps
from icecream import ic
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

MODELS_CLASSES = {
    "Floor": Floor,
    "WallMasonry": WallMasonry,
    "Finishing": Finishing,
    "ContractWork": ContractWork,
    "AbstractForm": AbstractForm,
}

def calculate_margin_based_on_formula(formula, material_baseprice, execution_baseprice, operational_cost_base):
    # Clean the formula to only allow 'a', 'b', 'c', '+', '-'
    clean_formula = re.sub(r'[^aAbBcC+\-]', '', formula)  # Allow a, b, c, +, -

    # Initialize calculated_value to zero
    calculated_value = 0

    # Define sums for a, b, and c
    material_baseprice_sum = sum(material_baseprice) if material_baseprice else 0  # For 'a'
    execution_baseprice_sum = sum(execution_baseprice) if execution_baseprice else 0  # For 'b'
    operational_cost_base_sum = sum(operational_cost_base) if operational_cost_base else 0  # For 'c'

    # Replace a, b, c in the formula with their respective sums
    clean_formula = clean_formula.lower()  # Convert formula to lowercase
    formula_with_values = clean_formula.replace('a', str(material_baseprice_sum)) \
                                       .replace('b', str(execution_baseprice_sum)) \
                                       .replace('c', str(operational_cost_base_sum))

    # Print the modified formula for debugging
    print(f"Formula with values: {formula_with_values}")

    try:
        # Safely evaluate the formula (only + and - are allowed)
        calculated_value = eval(formula_with_values)
    except Exception as e:
        print(f"Error evaluating formula: {e}")
        return None

    print(f"Final calculated value: {calculated_value}")
    return calculated_value
@csrf_exempt
def boq_calculation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_value = data.get("selected_value")
            model_name = data.get("model")
            field_name = data.get("field")
            pk = data.get("pk")

            if not all([selected_value, model_name, field_name, pk]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            model = apps.get_model("codes", "Code")
            obj = get_object_or_404(model, pk=selected_value)

            materials_total = []
            material_baseprice = []
            executions_total = []
            execution_baseprice = []
            operational_cost_total = []
            operational_cost_base = []
            contractmargin_total = []
            contractmargin_baseprice = []
            total_gst = []
            total_value = []

            project = Project.objects.get(pk=pk)

            # Process materials
            for material in obj.code_material.all():
                material_products = Material_Product.objects.filter(
                    name=material.mat_name, project=project
                )
                ic(material_products)
                if material_products.exists():
                    for product in material_products:
                        # matching_materials.append(product.sale_price)
                        total_gst.append(product.gst.rate)
                        get_gst=product.gst_value
                        print(get_gst,'gst')
                        price = product.price or 0  # Set to 0 if price is None
                        required = material.Required or 0  # Set to 0 if Required is None
                        materials_total.append(float(get_gst )* float(required) + float(price) *float( required))
                        print(materials_total.append)
                        material_baseprice.append(float(price) * float(required))
                else:
                    try:
                        material_obj = Material.objects.get(name=material.material_name)
                    except:
                        material_obj = Material.objects.get(name=material.mat_name)
                    material_prod = Material_Product.objects.create(
                        name=material_obj, price=material_obj.price, gst_value= material_obj.gst_value, sale_price=material_obj.sale_price )
                    # matching_materials.append(material_prod.sale_price)
                    total_gst.append(material_prod.gst.rate if material_prod.gst else 0)
                    get_gst = material_prod.gst_value
                    price = material_prod.price or 0  # Set to 0 if price is None
                    required =  material.Required or 0  # Set to 0 if Required is None
                    base_price = float(price) * float(required)
                    print(base_price)
                    total_g = float(get_gst) * float( required)
                    print(get_gst,'get_gst')
                    print(required,'qty')
                    print(total_g,'finalgst')
                    materials_total.append((float(get_gst) * float(required)) +  base_price)

                    material_baseprice.append(base_price)

            print(materials_total,'materialtotal')
            # Process executions
            for execution in obj.code_execution.all():
                execution_products = Execution_Product.objects.filter(
                    name__name=execution.ex_name, project=project
                )
                if execution_products.exists():
                    for product in execution_products:
                        price = product.price or 0  # Set to 0 if price is None
                        required = execution.need or 0  # Set to 0 if Required is None
                        execution_baseprice.append(float(price) * float(required))
                        total_gst.append(product.gst.rate)
                        get_gst = product.gst_value
                        print(get_gst,'exgstggggggggggggggg')
                        print()
                        base_price = float(price) * float(required)
                        executions_total.append((float(get_gst) * float(required)) +  base_price)

                else:
                    try:
                        # First, try to get Execution by name
                        ex = Execution.objects.get(name=execution.ex_name)
                    except:
                        ex = Execution.objects.get(pk=execution.id)
                        # If not found by name, try to get by primary key

                    ex_prod=Execution_Product.objects.create(
                        name=ex, price=execution.price, gst_value=ex.gst_value, sale_price=ex.sale_price
                    )
                    price = ex_prod.price or 0  # Set to 0 if price is None
                    required = execution.need or 0  # Set to 0 if Required is None
                    base_price = float(price) * float(required)
                    execution_baseprice.append(base_price)
                    get_gst = ex_prod.gst_value
                    executions_total.append((float(get_gst) * float(required)) + (float(price) * float(required)))


            print(executions_total, 'executiontotal')
            # Calculate costs
            operational_costs = Operational_Cost_product.objects.filter(project=project)

            for cost in operational_costs:
                if cost.formula:  # Assuming 'name' contains the formula
                    formula = cost.formula.name.lower()
                    # Initialize sum variable for this iteration
                    calculated_value = 0
                    calculated_value = calculate_based_on_formula(formula, material_baseprice, execution_baseprice)
                    # Now apply cost.allow_me if present
                    if cost.allow_me:
                        allow_me_value = float(cost.allow_me)  # Convert allow_me to float
                        with_allow_me =float((float( calculated_value) * allow_me_value) /100 )# Formula for allow_me
                    else:
                        allow_me_value = float(cost.allow_me)  # Convert allow_me to float
                        with_allow_me = float((float(calculated_value) * allow_me_value) / 100)
                    operational_cost_base.append(with_allow_me)

                    # Apply GST if present
                    if cost.gst:
                        gst_value = float(cost.gst.rate)  # Assuming gst.rate is the percentage value
                        gst_value_of_cost = (with_allow_me * gst_value) /100  # Calculate basic_value with GST
                        operational_cost_total.append(with_allow_me + gst_value_of_cost)
                    else:
                        gst_value_of_cost = with_allow_me  # If no GST, keep the same value
                        operational_cost_total.append(with_allow_me + gst_value_of_cost)
                        total_gst_cost = (
                        sum(float(i.gst.rate) for i in operational_costs if i.gst is not None)
                        / len(operational_costs)
                        if operational_costs
                        else 0
                        )
                        total_gst.append(total_gst_cost)
                        # total_value.append(gst_value_of_cost)
            print(operational_cost_total,'operationalcost total')
            # Calculate margin
            contract_margins = Contract_Margin_product.objects.filter(project=project)
            for margin in contract_margins:
                if margin.formula:  # Assuming 'name' contains the formula
                    formula = margin.formula.name.lower()
                    # Initialize sum variable for this iteration
                    margin_calculated_value = 0
                    margin_calculated_value = calculate_margin_based_on_formula(formula, material_baseprice, execution_baseprice,operational_cost_base)
                    # Now apply cost.allow_me if present
                    if margin.allow_me:
                        margin_allow_me_value = float(margin.allow_me)  # Convert allow_me to float
                        margin_with_allow_me = float((float(margin_calculated_value) * margin_allow_me_value) / 100)  # Formula for allow_me
                    else:
                        margin_allow_me_value = float(margin.allow_me)  # Convert allow_me to float
                        margin_with_allow_me = float((float(margin_calculated_value) * allow_me_value) / 100)
                    contractmargin_baseprice.append(margin_with_allow_me)


                    # Apply GST if present
                    if margin.gst:
                        gst_value = float(margin.gst.rate)  # Assuming gst.rate is the percentage value
                        gst_value_of_margin = (margin_with_allow_me * gst_value) /100   # Calculate basic_value with GST
                        contractmargin_total.append(margin_with_allow_me + gst_value_of_margin)
                    else:
                        gst_value_of_margin = margin_with_allow_me  # If no GST, keep the same value
                        contractmargin_total.append(margin_with_allow_me + gst_value_of_margin)
                        total_gst_margin = (
                            sum(float(i.gst.rate) for i in contract_margins  if i.gst is not None)
                            / len(contract_margins )
                            if contract_margins
                            else 0
                        )
                        total_gst.append(total_gst_margin)
                        # total_value.append(gst_value_of_margin)
            print(contractmargin_total,'contractmargintotl')
            total_material_baseprice = sum(material_baseprice)
            total_execution_baseprice = sum(execution_baseprice)
            total_operational_cost_total = sum(operational_cost_total)
            total_operational_cost_baseprice = sum(operational_cost_base)
            total_contractmargin_baseprice = sum(contractmargin_baseprice)

            total_sum = (
                    sum(float(val) for val in materials_total)
                    + sum(float(val) for val in executions_total)
                    + sum(float(val) for val in operational_cost_total)
                    + sum(float(val) for val in contractmargin_total)
            )

            total_gst_price = sum(Decimal(value) for value in total_value)
            total_basic_value = (
                Decimal(total_material_baseprice)
                +  Decimal(total_execution_baseprice)
                +  Decimal(total_operational_cost_baseprice)
                + Decimal(total_contractmargin_baseprice)
            )
            print( total_basic_value)
            total_gst = sum(Decimal(value) for value in total_gst)
            try:
                get_unit = Unit.objects.get(name=obj.unit)
                unit= get_unit.pk

            except ObjectDoesNotExist:
                unit = 1
            response_data = {
                "message": f"Successfully fetched data for {obj}",
                "totalprice": total_sum,
                "totalgstprice": total_gst_price,
                "total_basic_value": total_basic_value,
                "total_gst": total_gst,
                "unit": unit,
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            ic(e.__traceback__.tb_lineno)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def calculate_based_on_formula(formula, material_baseprice, execution_baseprice):
    # Clean the formula to remove irrelevant characters
    clean_formula = re.sub(r'[^aAbB+-]', '', formula)  # Keeping only relevant parts like 'a', 'b', '+', and '-'

    # Initialize calculated_value to zero
    calculated_value = 0

    # Step 1: Handle individual 'a' and 'b' if they exist
    if 'a' in clean_formula.lower():
        material_baseprice_sum = sum(material_baseprice)
        print(f"'a' found: material_baseprice_sum = {material_baseprice_sum}")
        calculated_value += material_baseprice_sum

    if 'b' in clean_formula.lower():
        execution_baseprice_sum = sum(execution_baseprice)
        print(f"'b' found: execution_baseprice_sum = {execution_baseprice_sum}")
        calculated_value += execution_baseprice_sum

    # Step 2: Handle combined formulas like 'a+b', 'a-b', 'b-a'
    if 'a+b' in clean_formula.lower():
        calculated_value = sum(material_baseprice) + sum(execution_baseprice)
        print(f"'a+b' found: calculated_value = {calculated_value}")

    elif 'a-b' in clean_formula.lower():
        calculated_value = sum(material_baseprice) - sum(execution_baseprice)
        print(f"'a-b' found: calculated_value = {calculated_value}")

    elif 'b-a' in clean_formula.lower():
        calculated_value = sum(execution_baseprice) - sum(material_baseprice)
        print(f"'b-a' found: calculated_value = {calculated_value}")

    # Step 3: Final output
    print(f'Final calculated value: {calculated_value}')
    return calculated_value
def load_materials(request):
    group = request.GET.get("group")
    if group.isdigit():  # Check if the group is a numeric value (pk)
        materials = Material.objects.filter(group__pk=group).values(
            "name", "price", "unit__name", "gst__rate"
        )
    else:  # Otherwise, filter by group name
        materials = Material.objects.filter(group__name=group).values(
            "name", "price", "unit__name", "gst__rate"
        )
    # materials = Material.objects.filter(group__pk=group).values('name','price','unit__name','gst__rate')
    return JsonResponse({"materials": list(materials)})


# Create your views here.
class BOQVIEW(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/boq.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_project(pk)
        boq = self.get_or_create_boq(project)
        current_time = int(time.time())
        context.update(self.get_model_data(boq, current_time))
        ic(context)
        context.update(self.get_additional_data(pk))
        print(pk)
        try:
            project = self.get_project(pk)
            boq = self.get_or_create_boq(project)
            current_time = int(time.time())
            context.update(self.get_model_data(boq, current_time)) 
            ic(context)
            context.update(self.get_additional_data(pk))
            print(pk)

        except ObjectDoesNotExist as e:
            context["error"] = f"Project with pk {pk} does not exist."
        except Exception as e:
            ic(e)
            context["error"] = "An unexpected error occurred."

        return context

    def get_project(self, pk):
        return Project.objects.get(pk=pk)

    def get_or_create_boq(self, project):
        boq, _ = BOQ.objects.get_or_create(project=project)
        return boq

    def get_model_data(self, boq, current_time):
        model_data = {"tables": []}
        order_no = 1
        for key, model in MODELS_CLASSES.items():
            if key == "AbstractForm":
                model_data["tables"].append(
                    self.process_abstract_form(model, boq, current_time, order_no)
                )
            else:
                model_data["tables"].extend(
                    self.process_model(model, boq, key, current_time, order_no)
                )
            order_no += 1
        return model_data

    def process_model(self, model, boq, key, current_time, order_no):
        query_set = model.objects.filter(boq=boq).order_by("table_order")
        if not query_set.exists():
            self.create_initial_object(model, boq, key, current_time, order_no)
            query_set = model.objects.filter(boq=boq).order_by("table_order")
        return self.group_data(query_set, boq, key.lower())

    def create_initial_object(self, model, boq, key, current_time, order_no):
        return model.objects.create(
            boq=boq,
            table_name=self.generate_table_name(key, boq, current_time),
            table_heading_name=f"{key}-1",
            table_order=order_no,
        )

    def generate_table_name(self, key, boq, current_time):
        return f"{key}_{boq.pk}_{current_time}"

    def process_abstract_form(self, model, boq, current_time, order_no):
        abstract_form_data = {}
        existing_abstract_form = model.objects.filter(boq=boq).order_by("table_order")
        abstract_form_data.update({"type": "abstractform"})
        if existing_abstract_form:
            abstract_form_data["rows"] = existing_abstract_form
            total_obj, _ = Total.objects.get_or_create(
                boq=boq,
                table_name="abstract_form_total",

                defaults={"full_amount": 0},
            )
            abstract_form_data["total"] = [total_obj]
            abstract_form_data["key"] = existing_abstract_form[0].table_name
            print(existing_abstract_form)
        else:
            for key, model_class in MODELS_CLASSES.items():
                if key != "AbstractForm":
                    table_name = f"{key}-1"
                    get_table= model_class.objects.get(boq=boq)
                    print( get_table,'table')
                    uniq_table=get_table.table_name
                    abstract_form_obj, created = model.objects.get_or_create(
                        boq=boq,
                        form_name=table_name,
                        table_name=uniq_table,
                        table_heading_name=table_name,
                        table_order=order_no,
                        defaults={"table_heading_name": f"{key}"},
                    )
                    abstract_form_data[key] = abstract_form_obj

            abstract_form_data["total"] = self.get_or_create_total(boq, table_name)
            abstract_form_data["key"] = abstract_form_obj.table_name
        return {"order": float("inf"), "table": abstract_form_data}

    def group_data(self, query_set, boq, table_type):
        table_dict = {}
        for obj in query_set:
            table_name = obj.table_name
            if table_name not in table_dict:
                table_dict[table_name] = {
                    "order": obj.table_order,
                    "table": {
                        "key": table_name,
                        "total": self.get_or_create_total(boq, table_name),
                        "type": table_type,
                        "rows": [],
                    },
                }
            table_dict[table_name]["table"]["rows"].append(obj)

        table_list = [value for value in table_dict.values()]
        return table_list

    def get_or_create_total(self, boq, table_name):
        total_obj, _ = Total.objects.get_or_create(
            boq=boq,
            table_name=table_name,
            defaults={"full_amount": 0},
        )
        return [total_obj]

    def get_additional_data(self, pk):
        return {
            "units": Unit.objects.all(),
            "gsts": GST.objects.all(),
            "code": Code.objects.filter(created_by=self.request.user),
            "pk": pk,
        }

    @csrf_exempt
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        model_name = data.get("model")
        table_name = data.get("table_name")
        field = data.get("field")
        value = data.get("value")
        row_pk = data.get("pk")
        field_values = data.get("fieldValues")
        project_pk = pk

        model_class = MODELS_CLASSES.get(model_name)
        if not model_class:
            return JsonResponse({"error": "Invalid model"}, status=400)

        # try:
        if row_pk != "new":
            instance = model_class.objects.get(pk=row_pk)
        elif row_pk == "new":
            project = Project.objects.get(pk=project_pk)
            boq, created = BOQ.objects.get_or_create(project=project)
            instance = model_class(boq_id=boq.pk, table_name=table_name)
            instance.save()

        if field_values:
            for key, value in field_values.items():
                if key in ["code", "gst", "unit"] and value is not None:
                    model = {
                        "code": Code.objects.filter(pk=int(value)).first(),
                        "gst": GST.objects.filter(pk=int(value)).first(),
                        "unit": Unit.objects.filter(pk=int(value)).first(),
                    }
                    ic(model)
                    setattr(instance, key, model[key])
                else:
                    setattr(instance, key, value)
        else:
            if field == "code":
                instance.code = Code.objects.filter(pk=value).first()
            else:
                setattr(instance, field, value)
        instance.save()

        return JsonResponse({"pk": instance.pk})
        # except Exception as e:
        #     return JsonResponse({'error': str(e), 'error_line_no': e.__traceback__.tb_lineno})


@csrf_exempt
def save_total(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        boq = BOQ.objects.get(project=project)

        data = json.loads(request.body)
        obj_pk = data.get("obj_pk")
        field_values = data.get("fieldValues")

        obj = Total.objects.get(boq=boq, pk=int(obj_pk))
        for key, value in field_values.items():
            if key == "code" and value is not None:
                ic(key, value)
                obj.code = Code.objects.get(pk=value)
                ic(obj.code)
                obj.unit = (
                    Unit.objects.get(name=obj.code.unit) if obj.code.unit else None
                )
            else:
                setattr(obj, key, Decimal(value) if value else None)
        obj.save()
        print(obj.table_name,'totallnnhnhhhhhhhhhhhhhhhh')
        # get_table =AbstractForm.objects.get(table_name=obj.form_name)

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse(
            {"status": "failed", "line_number": e.__traceback__.tb_lineno, "error": e}
        )


@csrf_exempt
def save_table_name(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        boq = BOQ.objects.get(project=project)

        data = json.loads(request.body)
        table_id = data.get("table_id")
        new_name = data.get("new_name")
        model = data.get("model")
        model = MODELS_CLASSES.get(model)
        model.objects.filter(table_name=table_id).update(table_heading_name=new_name)

        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse(
            {"status": "failed", "line_number": e.__traceback__.tb_lineno, "error": e}
        )


def reorder_boq_tables(boq, table_order, pk, current_model):
    model_list = [Floor, WallMasonry, Finishing]
    for model in model_list:
        if model == current_model:
            query_set = (
                model.objects.filter(boq=boq, table_order__gte=table_order)
                .exclude(pk=pk)
                .update(table_order=F("table_order") + 1)
            )
        else:
            query_set = model.objects.filter(
                boq=boq, table_order__gte=table_order
            ).update(table_order=F("table_order") + 1)

# for when click add table and select form that time use this create _table
@csrf_exempt
def create_table(request, pk):
    data = json.loads(request.body)
    table_type = data.get("type")
    table_order = int(data.get("order"))
    project = Project.objects.get(pk=pk)
    boq = BOQ.objects.get(project=project)
    print(boq)
    table_name = f"{table_type}_{boq.pk}_{int(time.time())}"
    print(table_name)
    if  table_type == 'Floor':
        heading_name='Multiline Form'
    elif table_type == 'WallMasonry':
        heading_name ='Bottomline Form'
    elif table_type == 'Finishing':
        heading_name ='Basic Form'

    model = MODELS_CLASSES.get(table_type)
    obj = model.objects.create(
        boq=boq,
        table_name=table_name,
        table_heading_name=heading_name,
        table_order=table_order + 1,
    )
    print(obj)
    reorder_boq_tables(boq, table_order, obj.pk, model)
    AbstractForm.objects.create(boq=boq, form_name=obj.table_heading_name,table_name=table_name,table_heading_name= obj.table_heading_name)
    total_obj = Total.objects.create(
        boq=boq,
        table_name=table_name,
    )

    return JsonResponse({"key": obj.table_name, "total_pk": total_obj.pk})



@csrf_exempt
def delete_row(request):
    if request.method == 'POST':
        print('hello')
        data = json.loads(request.body)
        pk = data.get('pk')
        table_type = data.get('table_type')
        print( table_type)
        print(pk)

        if table_type == "floor":
            try:
                # Assuming Floor is the model, filter and delete the object
                floor = Floor.objects.get(pk=pk)
                floor.delete()
                return JsonResponse({'success': True})
            except Floor.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Floor not found'})

        elif table_type == "finishing":
            finishing = Finishing.objects.get(pk=pk)
            finishing.delete()
            try:
                finishing = Finishing.objects.get(pk=pk)
                finishing.delete()
                return JsonResponse({'success': True})
            except Finishing.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Wall not found'})
        elif table_type == "wall":
            try:
                wall =  WallMasonry.objects.get(pk=pk)
                wall.delete()
                return JsonResponse({'success': True})
            except  WallMasonry.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Wall not found'})
        elif table_type == "other":
            try:
                other = ContractWork.objects.get(pk=pk)
                other.delete()
                return JsonResponse({'success': True})
            except ContractWork.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Wall not found'})

        # Add more cases for other table types if needed

    return JsonResponse({'success': False, 'error': 'Invalid request'})

class ContactList(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/contact_list.html"


class ContactForm(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/contact_form.html"
