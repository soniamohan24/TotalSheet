from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import *
from django.db.models import F
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models import Count, Sum
from django.core.exceptions import FieldDoesNotExist
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
import json
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.core.cache import cache
from codes.models import Code
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView as BaseLogoutView
from materials.models import MaterialGroup, Formula, Brand, Operational_Costs
from execution.models import ExecutionGroup
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from django.urls import reverse
from .utils import get_model_class, get_form_class, get_template_name
from django.shortcuts import redirect, get_object_or_404
from boq.models import CustomUser, BOQ
from profile.models import *
from django.core.exceptions import FieldError
from administrator.models import *



class DynamicCreateView(CreateView):
    def get_form_class(self):
        return get_form_class(self.kwargs["model_name"])

    def form_valid(self, form):
        model_class = get_model_class(self.kwargs["model_name"])
        name = form.cleaned_data.get("name")
        rate = form.cleaned_data.get("rate", None)  # Only for models with 'rate'

        # Check for name duplication
        if name:
            if model_class.objects.filter(name=name).exists(): 
                form.add_error("name", "This name already exists.")
                return self.form_invalid(form)

        # Check for rate duplication if applicable
        if rate is not None and model_class.objects.filter(rate=rate).exists():
            form.add_error("rate", "This rate already exists.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Determine the model_name dynamically or from kwargs
        model_name = self.kwargs.get("model_name", "default_model")

        # Serialize form errors and include modal name
        modal_name = (
            "your_modal_name"  # Replace with your actual modal name or logic to get it
        )
        errors = urlencode(
            {
                "errors": json.dumps(form.errors.get_json_data()),
                "modal_name": modal_name,
            }
        )

        # Build the URL for redirection
        url = f"{reverse('administrator:dynamic-list', kwargs={'model_name': model_name})}?{errors}"

        # Redirect to the URL with query parameters
        return HttpResponseRedirect(url)

    def get_template_names(self):
        return [get_template_name("create", self.kwargs["model_name"])]

    def get_success_url(self):
        return reverse(
            "administrator:dynamic-list",
            kwargs={"model_name": self.kwargs["model_name"]},
        )


class DynamicUpdateView(UpdateView):
    def get_form_class(self):
        return get_form_class(self.kwargs["model_name"])

    def get_template_names(self):
        return [get_template_name("update", self.kwargs["model_name"])]

    def get_queryset(self):
        model_class = get_model_class(self.kwargs["model_name"])
        return model_class.objects.all()

    def get_success_url(self):
        return reverse(
            "administrator:dynamic-list",
            kwargs={"model_name": self.kwargs["model_name"]},
        )


class DynamicDeleteView(DeleteView):
    def get_queryset(self):
        model_class = get_model_class(self.kwargs["model_name"])
        return model_class.objects.all()

    def get_template_names(self):
        return [get_template_name("delete", self.kwargs["model_name"])]

    def get_success_url(self):
        return reverse(
            "administrator:dynamic-list",
            kwargs={"model_name": self.kwargs["model_name"]},
        )


class DynamicDetailView(DetailView):
    def get_template_names(self):
        return [get_template_name("detail", self.kwargs["model_name"])]


class DynamicListView(ListView):
    paginate_by = 20  # Number of items per page

    def get_queryset(self):
        model_class = get_model_class(self.kwargs["model_name"])
        print(model_class)
        queryset = model_class.objects.all()

        # Filtering by group if specified
        group_id = self.request.GET.get("group")
        exgroup_id = self.request.GET.get("exgroup")

        if group_id:
            queryset = queryset.filter(group__id=group_id)
            selected_group = get_object_or_404(MaterialGroup, id=group_id)
            self.related_subgroups = selected_group.sub_groups.all()
        elif exgroup_id:
            print(exgroup_id)
            queryset = queryset.filter(group__id=exgroup_id)
            selected_group = get_object_or_404(ExecutionGroup, id=exgroup_id)
            print(selected_group)
            self.related_subgroups = selected_group.sub_groups.all()

        else:
            self.related_subgroups = SubGroup.objects.all()  # Fetch all if no group filter is applied
            self.related_subgroups = None

       

        subgroup_id = self.request.GET.get('subgroup')
        if subgroup_id and subgroup_id.strip():
            queryset = queryset.filter(subgroup__id=subgroup_id)

        ex_subgroup_id = self.request.GET.get('exsubgroup')
        if ex_subgroup_id and ex_subgroup_id.strip():
            queryset = queryset.filter(subgroup__id=ex_subgroup_id)

        # Searching by keywords
        search_query = self.request.GET.get("search", "")
        if search_query:
            search_fields = self.get_search_fields(model_class)
            search_filters = Q()
            for field in search_fields:
                try:
                    search_filters |= Q(**{field: search_query})
                except FieldError:
                    pass  # Skip fields that raise errors
            queryset = queryset.filter(search_filters)

        # Sorting by specified field and order
        sort_field = self.request.GET.get("sort", "pk")  # Default to primary key
        sort_order = self.request.GET.get("order", "asc")

        if sort_order == "desc":
            sort_field = f"-{sort_field}"

        # Apply ordering with error handling
        try:
            if model_class is GST:
                queryset = queryset.order_by("rate")
            elif model_class is Unit:
                queryset = queryset.order_by("name")
            else:
                queryset = queryset.order_by(sort_field)

        except FieldDoesNotExist:
            if model_class is GST:
                queryset = queryset.order_by("rate")
            else:
                queryset = queryset.order_by("pk")  # Fallback to default ordering

        return queryset

    def get_search_fields(self, model_class):
        search_fields = []

        for field in model_class._meta.get_fields():
            if isinstance(field, models.CharField) or isinstance(
                field, models.TextField
            ):
                search_fields.append(f"{field.name}__icontains")
            elif field.is_relation and field.many_to_one:  # Check if it's a ForeignKey
                related_model = field.related_model
                try:
                    related_field = related_model._meta.get_field("name")
                    if isinstance(related_field, models.CharField):
                        search_fields.append(f"{field.name}__name__icontains")
                except FieldDoesNotExist:
                    pass

                try:
                    related_field = related_model._meta.get_field("rate")
                    if isinstance(
                        related_field, (models.CharField, models.DecimalField)
                    ):
                        search_fields.append(f"{field.name}__rate__icontains")
                except FieldDoesNotExist:
                    pass

        return search_fields

    def get_template_names(self):
        return [get_template_name("list", self.kwargs["model_name"])]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        errors = self.request.GET.get("errors")
        queryset = self.get_queryset()
        print(f"query:{queryset}")
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        form_errors = json.loads(errors) if errors else {}

        # Calculate start index
        start_index = page_obj.start_index() - 1
        # Add context variables
        context["form_errors"] = form_errors
        context["start_index"] = start_index
        context["model_name"] = self.kwargs["model_name"]
        context["page_obj"] = page_obj
        context["items"] = page_obj  # Use the paginated objects directly
        context["groups"] = MaterialGroup.objects.all().order_by("name") 
        context["SubGroup"] = self.related_subgroups
        context["Execution_SubGroup"]=self.related_subgroups
        context['edit_sub']= ExecutionSubGroup.objects.all()

        context['materialedit_sub'] = SubGroup.objects.all()
        
        
        context["ex_groups"] = ExecutionGroup.objects.all().order_by("name")
        context["units"] = Unit.objects.all().order_by("name")
        context["brands"] = Brand.objects.all().order_by("name")
        context["formula"] = Formula.objects.exclude(Q(name__icontains="C"))
        context["contarctmargin_formula"] = Formula.objects.exclude(Q(name__icontains="D"))
        context["gsts"] = GST.objects.all().order_by("rate")
        context["total_allow_me"] = Operational_Costs.total_allow_me()
        context["con_total_allow_me"] = Contract_Margins.total_allow_me()
        # gsts = list(GST.objects.all())
        # sort_gsts=gsts.sort(key=lambda gst: float(gst.rate) if gst.rate.isdigit() else 0)
        # print(gsts,'hh')
        # context['gsts'] = sort_gsts
        context["current_sort_field"] = self.request.GET.get("sort", "pk")
        context["current_sort_order"] = self.request.GET.get("order", "asc")
        context["selected_group"] = self.request.GET.get("group", "")
        context["search_query"] = self.request.GET.get("search", "")
        context["request"] = self.request

        return context


class LoginView(FormView):
    template_name = "administrator/login.html"
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth_login(self.request, user)
                return redirect(
                    "/administrator/dashboard"
                )  # Redirect to a dashboard or home page
            else:
                messages.error(
                    self.request, "You do not have permission to access this site."
                )
                return self.form_invalid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # This method is called when the form is invalid
        return super().form_invalid(form)


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy("administrator:login")

    def get(self, request, *args, **kwargs):
        print(reverse_lazy("administrator:login"))  # Debug print
        return super().get(request, *args, **kwargs)


class DashboardView(TemplateView):
    template_name = "administrator/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = "dashboard_metrics"
        metrics = cache.get(cache_key)

        if not metrics:
            clients = CustomUser.objects.filter(user_type="client")
            metrics = (
                CustomUser.objects.aggregate(total_users=Count("id")),
                BOQ.objects.aggregate(total_boq_created=Count("id")),
                Code.objects.aggregate(total_codes=Count("id")),
                Project.objects.aggregate(total_projects=Count("id")),
                Brand.objects.aggregate(total_brands=Count("id")),
                JOBProfile.objects.aggregate(total_job_seekers=Count("id")),
                BusinessProfile.objects.aggregate(total_business_profiles=Count("id")),
                clients.aggregate(total_clients=Count("id")),
            )
            cache.set(cache_key, metrics, timeout=60 * 15)  # Cache for 15 minutes

        context.update(
            {
                "total_users": metrics[0]["total_users"],
                "total_clients": metrics[7]["total_clients"],
                "total_boq_created": metrics[1]["total_boq_created"],
                "total_codes": metrics[2]["total_codes"],
                "total_projects": metrics[3]["total_projects"],
                "total_brands": metrics[4]["total_brands"],
                "total_job_seekers": metrics[5]["total_job_seekers"],
                "total_business_profiles": metrics[6]["total_business_profiles"],
            }
        )

        return context


class MasterView(TemplateView):
    template_name = "administrator/master.html"


class UserManagementView(TemplateView):
    template_name = "administrator/user.html"


class SubGroupCreateView(View):
    def post(self, request):
        names = request.POST.getlist("sub_group_names[]")
        pk = request.POST.get("pk")
        print(f'PK: {pk}' )
        material_g = MaterialGroup.objects.get(pk=pk)
        sub_groups = []

        for name in names:
            if name:
                sub_group, created = SubGroup.objects.get_or_create(name=name)
                sub_groups.append(sub_group)

        material_g.sub_groups.set(sub_groups)

        return redirect("administrator:dynamic-list", model_name="material_group")


class EXSubGroupCreateView(View):
    def post(self, request):
        names = request.POST.getlist("sub_group_names[]")
        pk = request.POST.get("pk")
        ex_g = ExecutionGroup.objects.get(pk=pk)
        sub_groups = []

        for name in names:
            if name:
                sub_group, created = ExecutionSubGroup.objects.get_or_create(name=name)
                sub_groups.append(sub_group)

        ex_g.sub_groups.set(sub_groups)

        return redirect("administrator:dynamic-list", model_name="execution_group")


class BusinessSubGroupCreateView(View):
    def post(self, request):
        names = request.POST.getlist("sub_group_names[]")
        pk = request.POST.get("pk")
        business_g = BusinessType.objects.get(pk=pk)
        sub_groups = []

        for name in names:
            if name:
                sub_group, created = BusinessSubGroup.objects.get_or_create(name=name)
                sub_groups.append(sub_group)

        business_g.business_sub_groups.set(sub_groups)

        return redirect("administrator:dynamic-list", model_name="businesstype")
    
class WorkGroupSubGroupCreateView(View):
    def post(self, request):
        names = request.POST.getlist("sub_group_names[]")
        pk = request.POST.get("pk")
        work_g = Industry.objects.get(pk=pk)
        sub_groups = []

        for name in names:
            if name:
                sub_group, created = WorkGroupSubGroup.objects.get_or_create(name=name)
                sub_groups.append(sub_group)

        work_g.workgroup_sub_groups.set(sub_groups)
        return redirect("administrator:dynamic-list", model_name="industry")

class CodeGroupSubGroupCreateView(View):
    def post(self, request):
        names = request.POST.getlist("sub_group_names[]")
        pk = request.POST.get("pk")
        code_g = WorkGroup.objects.get(pk=pk)
        sub_groups = []

        for name in names:
            if name:
                sub_group, created = CodesgroupSubGroup.objects.get_or_create(name=name)
                sub_groups.append(sub_group)

        code_g.codesgroup_sub_groups.set(sub_groups)
        return redirect("administrator:dynamic-list", model_name="workgroup")


def remove_logo(request, pk):
    if request.method == "POST":
        item = get_object_or_404(Brand, pk=pk)
        item.logo.delete(save=False)  # Remove logo file
        item.logo = None  # Set the logo field to None
        item.save()
        return redirect("administrator:dynamic-list", model_name="brand")
