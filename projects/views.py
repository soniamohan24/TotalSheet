from django.shortcuts import render, redirect
from django.db import transaction  #
from profile.mixins import ProfileCompletionMixin
from .models import Project
from materials.models import *
from codes.models import *
from .forms import ClientInfoForm
from boq.models import *
from django.http import HttpResponseRedirect
from execution.models import *
from django.views.generic import UpdateView, TemplateView, DeleteView, CreateView
from django.views import View
from django.urls import reverse_lazy
from .forms import ProjectForm, ProjectSearchForm
from boq.models import CustomUser, ClientInfo
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from openpyxl import Workbook
import pandas as pd
from django.http import JsonResponse

import logging

logger = logging.getLogger(__name__)


# Create your views here.
class ProjectView(TemplateView):
    template_name = "dashboards/project_detail.html"

    def get_context_data(self, id):
        project_obj = Project.objects.get(pk=id)

        context = {
            "project": project_obj,
        }
        return context





class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboards/home.html"
    success_url = reverse_lazy("profile:dashboard")

    def form_valid(self, form):
        # Set user and client
        form.instance.user = self.request.user
        get_client_id = form.cleaned_data.get("client")
        client = ClientInfo.objects.get(pk=get_client_id.pk)
        form.instance.client = client
        project = form.save()
        import_type = self.request.POST.get("import_type")
        # Handle the selected import type
        if import_type == "master":
            all_materials = Material.objects.all()
            all_executions = Execution.objects.all()
            all_operational_costs = Operational_Costs.objects.all()
            all_contract_margins = Contract_Margins.objects.all()

            # Use atomic transaction to ensure that either all records are created, or none in case of an error
            with transaction.atomic():
                for material in all_materials:
                    # Copy fields from Material and create a new Material_Product entry
                    Material_Product.objects.create(
                        name=material,
                        group=material.group,
                        gst=material.gst,
                        gst_value=(
                            str(material.gst_value) if material.gst_value else None
                        ),
                        unit=material.unit,
                        brand=material.brand,
                        price=material.price,
                        sale_price=material.sale_price,
                        project=project,  # Now project.pk exists
                    )
                for execution in all_executions:
                    # Copy fields from Execution and create a new Execution_Product entry
                    Execution_Product.objects.create(
                        name=execution,
                        group=execution.group,
                        gst=execution.gst,
                        unit=execution.unit,
                        gst_value=(
                            str(execution.gst_value) if execution.gst_value else None
                        ),
                        description=execution.description,
                        price=execution.price,
                        sale_price=execution.sale_price,
                        project=project,  # Now project.pk exists
                    )
                for operational_cost in all_operational_costs:
                    Operational_Cost_product.objects.create(
                        name=operational_cost,
                        gst=operational_cost.gst,
                        allow_me=operational_cost.allow_me,
                        unit=operational_cost.unit,
                        project=project,  # Now project.pk exists
                    )
                for contract_margin in all_contract_margins:
                    Contract_Margin_product.objects.create(
                        name=contract_margin,
                        gst=contract_margin.gst,
                        allow_me=contract_margin.allow_me,
                        unit=contract_margin.unit,
                        formula=contract_margin.formula,  # Copy formula field
                        project=project,  # Now project.pk exists
                    )

        elif import_type == "previous_project":
            # Logic
            selected_project_id = self.request.POST.get("select_project")
            if selected_project_id:
                previous_project = Project.objects.get(pk=selected_project_id)
                material_products = Material_Product.objects.filter(
                    project=previous_project
                )
                execution_products = Execution_Product.objects.filter(
                    project=previous_project
                )
                operational_cost_products = Operational_Cost_product.objects.filter(
                    project=previous_project
                )
                contract_margin_products = Contract_Margin_product.objects.filter(
                    project=previous_project
                )

                # Use atomic transaction to ensure all records are created or none
                with transaction.atomic():
                    # Copy material products
                    for material_product in material_products:
                        Material_Product.objects.create(
                            name=material_product.name,
                            group=material_product.group,
                            gst=material_product.gst,
                            gst_value=material_product.gst_value,
                            unit=material_product.unit,
                            brand=material_product.brand,
                            price=material_product.price,
                            sale_price=material_product.sale_price,
                            project=project,  # Link to the new project
                        )

                    # Copy execution products
                    for execution_product in execution_products:
                        Execution_Product.objects.create(
                            name=execution_product.name,
                            group=execution_product.group,
                            gst=execution_product.gst,
                            unit=execution_product.unit,
                            gst_value=execution_product.gst_value,
                            description=execution_product.description,
                            price=execution_product.price,
                            sale_price=execution_product.sale_price,
                            project=project,  # Link to the new project
                        )

                    # Copy operational cost products
                    for operational_cost_product in operational_cost_products:
                        Operational_Cost_product.objects.create(
                            name=operational_cost_product.name,
                            gst=operational_cost_product.gst,
                            allow_me=operational_cost_product.allow_me,
                            unit=operational_cost_product.unit,
                            project=project,  # Link to the new project
                        )

                    # Copy contract margin products
                    for contract_margin_product in contract_margin_products:
                        Contract_Margin_product.objects.create(
                            name=contract_margin_product.name,
                            gst=contract_margin_product.gst,
                            allow_me=contract_margin_product.allow_me,
                            unit=contract_margin_product.unit,
                            formula=contract_margin_product.formula,
                            project=project,  # Link to the new project
                        )

        elif import_type == "code":
            # Logic for importing by selecting a code
            selected_code_id = self.request.POST.get("select_code")
            if selected_code_id:
                code = Code.objects.get(pk=selected_code_id)
                code_materials = code.code_material.all()
                code_executions = code.code_execution.all()
                with transaction.atomic():
                    for code_material in code_materials:
                        Material_Product.objects.create(
                            name=code_material.material_name or code_material.mat_name,
                            group=code_material.group,
                            gst=code_material.gst,
                            gst_value=code_material.gst_value,
                            unit=code_material.unit,
                            price=code_material.price,
                            sale_price=code_material.sub_total,  # Adjust as needed
                            project=project,  # Link to the new project
                        )
                    for code_execution in code_executions:
                        Execution_Product.objects.create(
                            name=code_execution.ex_name,
                            group=code_execution.group,
                            gst=code_execution.gst,
                            unit=code_execution.unit,
                            gst_value=code_execution.gst_value,
                            price=code_execution.price,
                            sale_price=code_execution.sub_total,  # Adjust as needed
                            project=project,  # Link to the new project
                        )

        # Redirect to the success URL after custom saving logic
        return redirect("profile:dashboard")

    def form_invalid(self, form):
        print(form.errors)

        return super().form_invalid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboards/home.html"

    def form_valid(self, form):
        # Ensure the form is valid before saving
        if form.is_valid():
            get_client_id = form.cleaned_data.get("client")
            print( get_client_id)
            # user = CustomUser.objects.get(username=get_client_id.email)
            client = ClientInfo.objects.get(user =get_client_id.user )
            project = form.save(commit=False)
            form.instance.client = client
            form.save()

            return redirect("profile:dashboard")
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("profile:dashboard")


class ProjectDeleteView(View):
    model = Project
    success_url = reverse_lazy("profile:dashboard")

    def post(self, request, *args, **kwargs):
        # Get the project instance
        project = self.get_object()
        # Set is_active to False for a soft delete
        project.is_active = False
        project.save()
        # Redirect to the success URL
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        # Fetch the project instance based on the primary key in the URL
        return self.model.objects.get(pk=self.kwargs['pk'])


class ProjectInformation(TemplateView):
    template_name = "dashboards/project_information.html"

    def get_context_data(self, **kwargs):
        # Extract 'pk' from kwargs
        pk = self.kwargs.get('pk') 
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, pk=pk)  # Ensure project is fetched correctly
        context["project"] = project  # Add project to context
        projects = Project.objects.all()
        context["projectss"] = projects
        project_boq = BOQ.objects.filter(project=project)
        context["projects_boq"] = project_boq
        return context
    
    def post(self, request, *args, **kwargs):
        # Extract 'pk' from self.kwargs
        pk = self.kwargs.get('pk')
        boq_name = request.POST.get('boq_name')

        # Fetch the project using pk and create a BOQ
        project = get_object_or_404(Project, pk=pk)
        boq_names = BOQ.objects.create(boq_name=boq_name, project=project)

        # Redirect to the 'boq' page with pk
        return redirect('boq:boq', pk=pk)


class clients(ProfileCompletionMixin, TemplateView):
    template_name = "dashboards/clients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all ClientInfo objects created by the logged-in user
        client_obj = ClientInfo.objects.filter(created_by=self.request.user)

        # Set up pagination
        paginator = Paginator(client_obj, 50)  # 50 clients per page
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Add the paginated client object and other context
        context["page_obj"] = page_obj
        context["messages"] = get_messages(self.request)  # Add messages to context

        return context


class ToggleFavoriteView(View):
    def post(self, request, client_id, *args, **kwargs):

        try:
            client = ClientInfo.objects.get(id=client_id)
            if client.is_favorite:
                client.is_favorite = False
            else:
                client.is_favorite = True
            client.save()

            return JsonResponse({"is_favorite": client.is_favorite})
        except ClientInfo.DoesNotExist:
            return JsonResponse({"error": "Client not found"}, status=404)


class ClientCreateView(View):
    template_name = "dashboards/clients.html"
    success_url = reverse_lazy("project:clients")

    def get(self, request, *args, **kwargs):
        # Just render the empty form when GET is called
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get the data from the POST request
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        pan_no = request.POST.get("pan_no")
        cin_no = request.POST.get("cin_no")
        company_name = request.POST.get("company_name")
        website = request.POST.get("website")
        social_link = request.POST.get("social_link")

        # Check if the email is already associated with a ClientInfo record

        client_info = CustomUser.objects.filter(email=email).first()

        if client_info:
            existing_client_info = ClientInfo.objects.filter(user=client_info, created_by=request.user).first()
            # If the ClientInfo exists and was created by the current user
            if existing_client_info:
                messages.error(request, "You have already created a ClientInfo with this email.")
                return redirect("project:clients")  # Redirect back with error

            # If the ClientInfo exists but was created by another user, allow creating a new client without any message
            else:
                user=CustomUser.objects.get(email=email)
                try:
                    print('hrlloohgg')
                    client_info = ClientInfo(
                        user=user,
                        first_name=first_name,
                        last_name=last_name,
                        address=address,
                        pan_no=pan_no,
                        cin_no=cin_no,
                        company_name=company_name,
                        website=website,
                        social_link=social_link,
                        created_by=request.user,  # Add the current user as creator
                    )
                    client_info.save()  # Save the ClientInfo object

                    # Success message and redirect
                    messages.success(request, "Client created successfully.")
                    print('rrrr')
                    return redirect("project:clients")

                except Exception as e:
                    # Handle errors when saving ClientInfo
                    messages.error(request, f"Error creating ClientInfo: {str(e)}")

                    print(e)
                    return redirect("project:clients")  # Redirect or render with error

        else:
            # If no ClientInfo exists, create a new CustomUser and ClientInfo
            try:
                user = CustomUser(
                    email=email,
                    phone_number=phone_number,
                    first_name=first_name,
                    last_name=last_name,
                    user_type="client",  # Set user type to 'client'
                    username=email,  # Use email as username
                )
                user.save()  # Save the CustomUser object

                # Create the associated ClientInfo object
                client_info = ClientInfo(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    pan_no=pan_no,
                    cin_no=cin_no,
                    company_name=company_name,
                    website=website,
                    social_link=social_link,
                    created_by=request.user,  # Add the current user as creator
                )
                client_info.save()  # Save the ClientInfo object

                # Success message and redirect
                messages.success(request, "Client created successfully.")
                return HttpResponseRedirect(self.success_url)

            except Exception as e:
                # Handle errors when saving CustomUser or ClientInfo
                messages.error(request, f"Error creating ClientInfo: {str(e)}")
                return redirect("project:clients")  # Redirect or render with error

class EditClientView(UpdateView):
    model = ClientInfo
    form_class = ClientInfoForm
    template_name = 'edit_client.html'

    def get_success_url(self):
        return reverse_lazy('project:clients')



def project_search(request):
    form = ProjectSearchForm(request.GET or None)
    projects = Project.objects.all()
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            projects = projects.filter(
                Q(name__icontains=query)
                | Q(client__first_name__icontains=query)
                | Q(client__last_name__icontains=query)
                | Q(client__user__email__icontains=query)  # Search by client email
                | Q(pincode__icontains=query)
            ).distinct()
            print(f"Queryset: {projects.query}")

    context = {"form": form, "projects": projects}
    query_params = request.GET.urlencode()
    return redirect(f'{reverse("profile:dashboard")}?{query_params}')


def client_search(request):
    query = request.GET.get("query", "")  # Get the search query from the GET request

    if query:
        # Filter clients based on the query across multiple fields
        client_obj = ClientInfo.objects.filter(
            Q(first_name__icontains=query)  # Search in first name
            | Q(last_name__icontains=query)  # Search in last name
            | Q(user__email__icontains=query)  # Search in email from CustomUser
            | Q(
                user__phone_number__icontains=query
            )  # Search in phone number from CustomUser
            | Q(address__icontains=query)  # Search in address
            | Q(company_name__icontains=query),
            created_by=request.user,  # Search in company name
        )
    else:
        client_obj = ClientInfo.objects.filter(
            created_by=request.user
        )  # If no query, return an empty queryset

    context = {
        "page_obj": client_obj,
        "query": query,
    }

    return render(request, "dashboards/clients.html", context)


class DownloadClientsView(View):
    def get(self, request, *args, **kwargs):
        clients = ClientInfo.objects.filter(created_by=self.request.user)
        # Create an Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Clients"

        # Add headers
        headers = [
            "First Name",
            "Last Name",
            "Email",
            "Phone Number",
            "Address",
            "Company Name",
            "Website",
            "Social Link",
        ]
        ws.append(headers)

        # Add client data
        for client in clients:
            ws.append(
                [
                    client.first_name,
                    client.last_name,
                    client.user.email,
                    client.user.phone_number,
                    client.address,
                    client.company_name,
                    client.website,
                    client.social_link,
                ]
            )

        # Prepare response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=clients.xlsx"

        wb.save(response)
        return response


class BulkUploadClientsView(View):
    def post(self, request, *args, **kwargs):
        client_file = request.FILES["client_file"]

        # Verify file format
        if client_file.name.endswith(".xlsx"):
            # Read the Excel file
            df = pd.read_excel(client_file)

            # Track successful uploads and duplicates
            total_uploaded = 0
            duplicate_entries = 0

            # Process each row in the DataFrame
            for _, row in df.iterrows():
                email = row.get("Email")

                # Check for existing client with the same email and creator

                # If the ClientInfo exists and was created by the current user
                existing_client_info=ClientInfo.objects.filter(user__email=email, created_by=self.request.user)
                if existing_client_info:
                    duplicate_entries += 1
                    continue  # Skip if duplicate

                # Create new CustomUser if email does not exist in the database
                if not CustomUser.objects.filter(email=email).exists():
                    user = CustomUser.objects.create(
                        first_name=row.get("First Name"),
                        last_name=row.get("Last Name"),
                        email=email,
                        phone_number=row.get("Phone Number"),
                        username=email,
                        user_type="client",
                    )
                else:
                    user = CustomUser.objects.get(email=email)

                # Create the associated ClientInfo
                ClientInfo.objects.create(
                    user=user,
                    first_name=row.get("First Name"),
                    last_name=row.get("Last Name"),
                    address=row.get("Address"),
                    pan_no=row.get("PAN Number"),
                    cin_no=row.get("CIN Number"),
                    company_name=row.get("Company Name"),
                    website=row.get("Website"),
                    social_link=row.get("Social Link"),
                    created_by=request.user,
                )
                total_uploaded += 1

            # Success message with upload status
            messages.success(
                request,
                f"Upload successful! {total_uploaded} clients were added. "
                f"{duplicate_entries} clients already exist."
            )
        else:
            # Error message for invalid file format
            messages.error(request, "Invalid file format. Please upload a .xlsx file.")

        return redirect("project:clients")
class DeleteClientView(View):
    def post(self, request, pk):
        client = get_object_or_404(ClientInfo, pk=pk)
        client.delete()
        return redirect('project:clients')  # Redirect to the client list page after deletion

class ProjectActiveView(View):
    model = Project
    success_url = reverse_lazy("profile:dashboard")

    def post(self, request, *args, **kwargs):
        # Get the project instance
        project = self.get_object()
        # Set is_active to False for a soft delete
        project.is_active = True
        project.save()
        # Redirect to the success URL
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        # Fetch the project instance based on the primary key in the URL
        return self.model.objects.get(pk=self.kwargs['pk'])