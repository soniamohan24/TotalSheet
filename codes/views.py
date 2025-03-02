from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,DeleteView
from execution.models import *
from administrator.models import *
import traceback
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from materials.models import Material, MaterialGroup
from codes.models import *
from profile.mixins import ProfileCompletionMixin
from .forms import CodeDuplicateForm
from django.views.generic.edit import FormView
from django.urls import reverse
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from icecream import ic
# Create your views here.
class CodeView(ProfileCompletionMixin, View):
    template_name = 'dashboards/code.html'

    def get(self, request, *args, **kwargs):
        code_id = kwargs.get('code_id')
        context = {
            'material': Material.objects.all(),
            'execution': Execution.objects.all(),
            'industry': Industry.objects.all(),
            'unit': Unit.objects.filter(engineer_field=True).order_by('name'),
            'worktype': WorkGroup.objects.all(),
            'worktypesubgroup': CodesgroupSubGroup.objects.all(),
            'executiongroup': ExecutionGroup.objects.all(),
            'materialgroup': MaterialGroup.objects.all(),
            'code': None,
            'operational_cost': Operational_Costs.objects.all(),
            'contract_margin': Contract_Margins.objects.all(),
            'today': timezone.now().date()
        }

        if code_id:  # If a code ID is provided, we're editing an existing code
            code = get_object_or_404(Code, id=code_id)
            context['code'] = code
            context['code_material'] = code.code_material.all()
            context['code_execution'] = code.code_execution.all()
            context['onsite_expense'] = code.onsite_expense.all()
            context['offsite_expense'] = code.offsite_expense.all()

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        try:
            # Fetch values from POST request
            pk = request.POST.get('pk', None)
            if not pk:
                pk = None
            industries = request.POST.get('industries', '')
            group_name = request.POST.get('group_name', '')
            subgroup_name = request.POST.get('subgroup_name', '')
            created_by = request.POST.get('created_by', '')
            date_str = request.POST.get('date', None)
            if date_str:
                try:
                    # Convert the date from MM-DD-YYYY to YYYY-MM-DD
                    date_obj = datetime.strptime(date_str, '%m-%d-%Y')
                    date = date_obj.strftime('%Y-%m-%d')
                except ValueError:

                    # Handle invalid date format
                    date = None
            else:
                date = None
            code_preview = request.POST.get('code_preview', '')
            design_for = request.POST.get('design_for', '')
            unit = request.POST.get('unit', '')
            basic_value = request.POST.get('basic_value', '')
            gst_value = request.POST.get('gst_value', '')
            gst = request.POST.get('gst', '')
            grand_total = request.POST.get('grand_total', '')
            description = request.POST.get('description', '')
            note = request.POST.get('note', '')
            material_codes = request.POST.get('materialcode')
            execution_codes = request.POST.get('executioncode')
            material_total_rate = request.POST.get('material_total_rate')
            material_basicvalue = request.POST.get('material_basicvalue')
            material_gstvalue = request.POST.get('material_gstvalue')
            material_total_gst = request.POST.get('material_gstratevalue')
            material_totalvalue = request.POST.get('material_totalvalue')
            execution_total_rate = request.POST.get('execution_total_rate')
            execution_basicvalue = request.POST.get('execution_basicvalue')
            execution_gstvalue = request.POST.get('execution_gstvalue')
            execution_gstrate = request.POST.get('execution_gstrate')
            execution_totalvalue = request.POST.get('execution_total-value')
            margin_totalrate = request.POST.get('margin_rate')
            margin_total_basicvalue = request.POST.get('margin_basicvalue')
            margin_subtotal = request.POST.get('margin_subtotal')
            margin_gst=request.POST.get('margin_gst')
            margin_gst_value=request.POST.get('margin_gstvalue')
            op_basicvalue = request.POST.get('op_basicvalue')
            op_gst = request.POST.get('op_gst')
            op_gstvalue = request.POST.get('op_gstvalue')
            op_total = request.POST.get('op_total')
            op_allowme= request.POST.get('op_allowme')
            margin_allowme =  request.POST.get('margin_required')
            try:
                get_code = Code.objects.get(pk=pk)
            except ObjectDoesNotExist:
                # Check if a code with the specified `code_preview` already exists
                if Code.objects.filter(code_preview=code_preview).exists():
                    messages.error(self.request, "A code with this name already exists.")
                    return redirect(reverse('code:code'))
            code, created = Code.objects.update_or_create(
                pk=pk,  # Assuming this is unique
                defaults={
                    'industries': industries,
                    'group_name': group_name,
                    'subgroup_name':subgroup_name,
                    'creator_name': created_by,
                    'date': date if date else None,
                    'design_for': design_for,
                    'unit': unit,
                    'gst_per':gst,
                    'basic_value': basic_value,
                    'gst_value': gst_value,
                    'grand_total': grand_total,
                    'description': description,
                    'note': note,
                    'code_type': 'draft_code',
                    'material_code' : material_codes,
                    'execution_code' : execution_codes,
                    'code_preview': code_preview,
                    'created_by':self.request.user
                }
            )

            # Handle Materials
            material_pks = request.POST.getlist('material_pk[]')
            materialgroup_selects = request.POST.getlist('material_group[]')
            material_selects = request.POST.getlist('materialselect[]')
            material_rates = request.POST.getlist('rate[]')
            material_units = request.POST.getlist('unit[]')
            material_gst = request.POST.getlist('gst[]')
            material_ratios = request.POST.getlist('ratio[]')
            material_basic_values = request.POST.getlist('basicvalue[]')
            material_gst_values = request.POST.getlist('gstvalue[]')
            material_sub_totals = request.POST.getlist('subtotal[]')
            for idx in range(len(material_selects)):

                try:
                    # Fetch Material, GST, and Unit instances from their respective lists
                    # material_groupinstance=MaterialGroup.objects.get(pk=materialgroup_selects[idx])
                    try:
                        # Try fetching by primary key
                        material_groupinstance = MaterialGroup.objects.get(pk=materialgroup_selects[idx])
                    except MaterialGroup.DoesNotExist:

                        # If not found by pk, fetch by name
                        material_groupinstance = MaterialGroup.objects.get(name=materialgroup_selects[idx])
                    try:
                        material_instance = Material.objects.get(pk=material_selects[idx])
                    except:

                        material_instance = Material.objects.get(name=material_selects[idx])


                    gst_instance = GST.objects.get(rate=material_gst[idx])
                    unit_instance = Unit.objects.get(name= material_units[idx])

                    # If pk is not None or empty
                    if material_pks[idx]:
                        try:
                            # Use primary key to update if it exists
                            material, created = code_Material.objects.update_or_create(
                                pk=material_pks[idx],
                                defaults={
                                    'group':material_groupinstance,
                                    'mat_name': material_instance,
                                    'material_name': material_selects[idx],
                                    'price': material_rates[idx],
                                    'Required': material_ratios[idx],
                                    'basic_value': material_basic_values[idx],
                                    'gst_value': material_gst_values[idx],
                                    'sub_total': material_sub_totals[idx],
                                    'gst': gst_instance,  # Assign the GST instance from the list
                                    'unit': unit_instance
                                }
                            )
                            # code.code_material.set(material)
                        except Exception as e:
                            print(f"Error updating material with pk {material_pks[idx]}: {e}")
                    else:

                        try:
                            # Create new material if no pk is provided
                            material = code_Material.objects.create(
                                group= material_groupinstance,
                                mat_name=material_instance,
                                price=material_rates[idx],
                                Required=material_ratios[idx],
                                basic_value=material_basic_values[idx],
                                gst_value=material_gst_values[idx],
                                sub_total=material_sub_totals[idx],
                                gst=gst_instance,  # Assign the GST instance from the list
                                unit=unit_instance
                            )
                            code.code_material.add(material)
                        except Exception as e:
                            print(f"Error creating new material: {e}")

                except Material.DoesNotExist:
                    print(f"Material with pk {material_selects[idx]} does not exist.")
                except GST.DoesNotExist:
                    print(f"GST with pk {gst_instance[idx]} does not exist.")
                except Unit.DoesNotExist:
                    print(f"Unit with pk {unit_instance[idx]} does not exist.")
                except Exception as e:
                    print(f"Unexpected error: {e}")
            code.material_total_rate = material_total_rate
            code.material_total_basicvalue = material_basicvalue
            code.material_total_gstvalue =  material_gstvalue
            code.material_subtotal = material_totalvalue
            code.material_total_gst = material_total_gst

            # Handle Executions
            execution_pks = request.POST.getlist('exe_pk[]')
            executiongroup_selects = request.POST.getlist('execution_group[]')
            print(executiongroup_selects)
            execution_selects = request.POST.getlist('exeselect[]')
            execution_rates = request.POST.getlist('exe_rate[]')
            execution_units = request.POST.getlist('exe_unitInput[]')
            execution_ratios = request.POST.getlist('exe_ratio[]')
            execution_basic_values = request.POST.getlist('exe_basicvalue[]')
            execution_gst_values = request.POST.getlist('exe_gstvalue[]')
            execution_sub_totals = request.POST.getlist('exe_subtotal[]')
            execution_gsts = request.POST.getlist('exe_gst[]')
            for idx in range(len(execution_selects)):
                try:
                    try:
                        # Try fetching by primary key
                        execution_groupinstance = ExecutionGroup.objects.get(pk=executiongroup_selects[idx])
                    except ExecutionGroup.DoesNotExist:
                        # If not found by pk, fetch by name
                        execution_groupinstance = ExecutionGroup.objects.get(name=executiongroup_selects[idx])

                    # execution_groupinstance = ExecutionGroup.objects.get(pk= executiongroup_selects[idx])
                    try:
                        execution_instance = Execution.objects.get(pk=execution_selects[idx])
                    except:
                        execution_instance = Execution.objects.get(name=execution_selects[idx])

                    ex_gst_instance = GST.objects.get(rate=str(execution_gsts[idx]))
                    ex_unit_instance = Unit.objects.get(name=str(execution_units[idx]))


                    if execution_pks[idx]:
                        print('pk')
                        try:
                            execution,created = code_Execution.objects.update_or_create(
                                    pk=execution_pks[idx],  # Assuming this is unique
                                    defaults={
                                        'group':execution_groupinstance,
                                        'execution_name': execution_selects[idx],
                                        'ex_name' :  execution_instance,
                                        'price': execution_rates[idx],
                                        'need': execution_ratios[idx],
                                        'basic_value': execution_basic_values[idx],
                                        'gst_value': execution_gst_values[idx],
                                        'sub_total': execution_sub_totals[idx],
                                        'exe_name': execution_instance,
                                        'gst': ex_gst_instance,  # Assign the GST instance from the list
                                        'unit': ex_unit_instance
                                    }
                                )



                        except Exception as e:
                            print(f"Error updating material with pk {material_pks[idx]}: {e}")
                    else:
                        try:
                            print('create')
                            # Create new material if no pk is provided
                            execution = code_Execution.objects.create(
                                group =execution_groupinstance,
                                price=execution_rates[idx],
                                need=execution_ratios[idx],
                                basic_value=execution_basic_values[idx],
                                gst_value=execution_gst_values[idx],
                                sub_total=execution_sub_totals[idx],
                                gst= ex_gst_instance,  # Assign the GST instance from the list
                                ex_name = execution_instance,
                                unit =ex_unit_instance,
                                execution_name = execution_selects
                            )
                            code.code_execution.add(execution)
                        except Exception as e:
                            print(f"Error creating new execution: {e}")
                            print("Traceback details:")
                            print(traceback.format_exc())
                            print(f"Error creating new execution: {e}")

                except Execution.DoesNotExist:
                    print(f"Execution with pk {execution_selects[idx]} does not exist.")
                except GST.DoesNotExist:
                    print(f"GST with pk {gst_instance[idx]} does not exist.")
                except Unit.DoesNotExist:
                    print(f"Unit with pk {unit_instance[idx]} does not exist.")
                except Exception as e:
                    print(f"Unexpected error: {e}")

            code.execution_total_rate = execution_total_rate
            code.execution_total_basicvalue = execution_basicvalue
            code.execution_total_gstvalue = execution_gstvalue
            code.execution_subtotal = execution_totalvalue
            code.execution_total_gst=  execution_gstrate

            # Handle On-Site Expenses
            operational_cost_pk = request.POST.getlist('onside_pk[]')
            operational_cost_names =request.POST.getlist('onsideexpensename', '')
            operational_cost_formula = request.POST.getlist('formula', '')
            operational_costamount = request.POST.getlist('onsideamount', '')
            operational_cost_required = request.POST.getlist('managmentratio', '')
            operational_cost_basic_value = request.POST.getlist('onside_basic_value', '')
            operational_cost_subtotal = request.POST.getlist('onside_subtotal', '')
            operational_costgst = request.POST.getlist('onside_gst', '')
            operational_costgst_value = request.POST.getlist('onside_gst_value', '')
            operational_cost_description=request.POST.getlist('onside_description', '')
            for idx in range(len(operational_cost_names)):
                gst_instance = GST.objects.get(rate=str(operational_costgst[idx]))
                op_formula = Formula.objects.get(pk=operational_cost_formula[idx])
                if operational_cost_pk [idx]:
                    # If pk exists, attempt to update
                    on_site_expense, _ = code_OnSiteExpense.objects.update_or_create(
                        pk=operational_cost_pk[idx],  # Assuming this is unique
                        defaults={
                            'on_value' :operational_costamount[idx],
                            'onsite_expense_name':operational_cost_names[idx],
                            'allow_me': operational_cost_required[idx],
                            'basic_value': operational_cost_basic_value[idx],
                            'sub_total': operational_cost_subtotal[idx],
                            'formula':op_formula,
                            'gst' : gst_instance,
                            'gst_value' : operational_costgst_value[idx],
                            'description': operational_cost_description[idx]
                        }
                    )
                else:
                    on_site_expense, _ = code_OnSiteExpense.objects.create(
                        on_value=operational_costamount[idx],  # Assuming this is unique
                        onsite_expense_name=operational_cost_names[idx],
                        allow_me=operational_cost_required[idx],
                        basic_value=operational_cost_basic_value[idx],
                        sub_total=operational_cost_subtotal[idx],
                        formula =op_formula,
                        gst=gst_instance,
                        gst_value=operational_costgst_value[idx],
                        description=operational_cost_description[idx]
                    )
                code.onsite_expense.add(on_site_expense)
            code.operational_cost_basicvalue = op_basicvalue
            code.operational_cost_subtotal = op_total
            code.operational_cost_gst = op_gst
            code.operational_cost_gst_value = op_gstvalue
            code.op_allowme=op_allowme

            # Handle Off-Site Expenses
            Contract_Margin_pk = request.POST.getlist('offside_pk[]')
            Contract_Margin_expense_names = request.POST.getlist('Contract_Margin_name[]')
            Contract_Margin_amounts = request.POST.getlist('Contract_Marginamount[]')
            Contract_Margin_required = request.POST.getlist('Contract_Marginreqvalue[]')
            Contract_Margin_basic_values = request.POST.getlist('Contract_Marginbasicvalue[]')
            Contract_Margin_gst_values = request.POST.getlist('Contract_Margingstvalue[]')
            Contract_Margin_subtotals = request.POST.getlist('Contract_Marginsubtotal[]')
            Contract_Margin_formula = request.POST.getlist('cm_formula', '')
            Contract_Margin_gst =request.POST.getlist('Contract_Margingst[]')
            Contract_Margin_description= request.POST.getlist('offside_description[]')


            for idx in range(len(Contract_Margin_expense_names)):
                gst_instance = GST.objects.get(rate= Contract_Margin_gst[idx])
                if Contract_Margin_pk[idx]:
                    cm_formula = Formula.objects.get(pk=Contract_Margin_formula[idx])
                    print( cm_formula ,'existornot')
                    # If pk exists, attempt to update
                    off_site_expense, _ = code_OffSiteExpense.objects.update_or_create(
                        pk=Contract_Margin_pk[idx],  # Assuming this is unique
                        defaults={
                            'on_value': Contract_Margin_amounts[idx],
                            'offsite_expense_name':  Contract_Margin_expense_names [idx],
                            'i_need': Contract_Margin_required[idx],
                            'basic_value': Contract_Margin_basic_values[idx],
                            'gst_value': Contract_Margin_gst_values[idx],
                            'sub_total': Contract_Margin_subtotals[idx],
                            'formula':cm_formula,
                            'gst':gst_instance,
                            'description':Contract_Margin_description[idx]
                        }
                    )
                else:
                    # If pk is None or invalid, create a new instance
                    off_site_expense = code_OffSiteExpense.objects.create(
                        on_value=Contract_Margin_amounts[idx],
                        offsite_expense_name =  Contract_Margin_expense_names[idx],
                        i_need=Contract_Margin_required[idx],
                        basic_value=Contract_Margin_basic_values[idx],
                        gst_value=Contract_Margin_gst_values[idx],
                        sub_total=Contract_Margin_subtotals[idx],
                        formula=cm_formula,
                        gst=gst_instance,
                        description=Contract_Margin_description[idx]
                    )

                code.offsite_expense.add(off_site_expense)
            code.margin_totalrate = margin_totalrate
            code.margin_total_basicvalue = margin_total_basicvalue
            code.margin_subtotal = margin_subtotal
            code.margin_total_gst= margin_gst
            code.margin_total_gst_value = margin_gst_value
            code.margin_allowme = margin_allowme
            code.save()
            return redirect(reverse('code:specification'))
        except Exception as e:
            print(f"Error: {str(e)}")
            ic(e.__traceback__.tb_lineno)
            return redirect(reverse('code:code'))


class SpecificationView(ProfileCompletionMixin, TemplateView):
    template_name = "dashboards/specification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the filter parameters from GET request
        code_type_filter = self.request.GET.get('code_type', None)
        unit_filter = self.request.GET.get('unit', None)

        # Start with the default queryset
        specifications = Code.objects.filter(code_type='draft_code', created_by=self.request.user)

        # Apply filters if the values are provided
        if code_type_filter:
            specifications =  specifications.filter(group_name=code_type_filter)

        if unit_filter:
            specifications = specifications.filter(unit=unit_filter)

        # Pass the filtered specifications and other context data
        context['specifications'] = specifications
        context['code_type'] = WorkGroup.objects.all()
        context['unit'] = Unit.objects.filter(engineer_field=True)

        return context


class DuplicateCodeView(LoginRequiredMixin, FormView):
    template_name = 'dashboards/specification.html'
    form_class = CodeDuplicateForm
    success_url = reverse_lazy('code:specification')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'material_code': self.get_object().material_code,
            'execution_code': self.get_object().execution_code,
        }
        return kwargs

    def get_object(self):
        return get_object_or_404(Code, id=self.kwargs['code_id'])

    def form_valid(self, form):
        # Retrieve the original code instance to duplicate
        code = self.get_object()
        material_code = form.cleaned_data['material_code']
        execution_code = form.cleaned_data['execution_code']

        # Duplicate the code instance by copying the existing one
        new_code = Code.objects.get(pk=code.pk)
        new_code.pk = None  # Set pk to None to create a new instance
        new_code.material_code = material_code
        new_code.execution_code = execution_code
        new_code.code_preview = f"{material_code} - {execution_code}"  # Update code_preview
        code_preview = f"{material_code}-{execution_code}"

        if Code.objects.filter(code_preview=code_preview).exists():
            messages.error(self.request, "A code with this name already exists.")
            return redirect(reverse('code:specification'))
        else:
            new_code.save()

            # Duplicate ManyToMany relationships
            new_code.code_material.set(code.code_material.all())
            new_code.code_execution.set(code.code_execution.all())
            new_code.onsite_expense.set(code.onsite_expense.all())
            new_code.offsite_expense.set(code.offsite_expense.all())

            return super().form_valid(form)

    def form_invalid(self, form):
        # Log or print errors for debugging
        print("Form submission failed with errors:", form.errors)  # or use logger if configured
        return super().form_invalid(form)
class SpecificationDeleteView(DeleteView):
    model = Code
    success_url = reverse_lazy('code:specification')
