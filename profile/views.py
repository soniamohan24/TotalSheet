from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView, View, DeleteView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from execution.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from materials.models import *
from django.shortcuts import get_object_or_404
from codes.models import *
from profile.models import Profession, Profile, JOBProfile, BusinessProfile, Experience
from django.http import JsonResponse
import json
from django.utils import timezone
import logging
from boq.models import ClientInfo
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .mixins import ProfileCompletionMixin
from django.urls import reverse

logger = logging.getLogger(__name__)


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "profile_update.html"  # Your template for profile update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example context data you might want to include
        context["profile"] = None  # or some default value
        return context

    def get_success_url(self):
        return reverse_lazy(
            "profile-update"
        )  # Redirect to profile update page after successful update


class DashboardView(ProfileCompletionMixin, TemplateView):
    template_name = "dashboards/home.html"  # Your template for dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the search query from the request
        query = self.request.GET.get("query", "")
        print(query)

        # Fetch projects based on the query
        if query:
            project = Project.objects.filter(user=self.request.user, is_active=True)
            projects = (
                project.annotate(
                    client_full_name=Concat(
                        "client__first_name", Value(" "), "client__last_name"
                    )
                )
                .filter(
                    Q(name__icontains=query)
                    | Q(client__first_name__icontains=query)
                    | Q(client__last_name__icontains=query)
                    | Q(client_full_name__icontains=query)  # Search by full name
                    | Q(pincode__icontains=query)
                    | Q(place__icontains=query)
                )
                .distinct()
            )
        else:
            projects = Project.objects.filter(user=self.request.user, is_active=True).order_by('-pk')

        # Pagination
        paginator = Paginator(projects, 10)  # Show 10 projects per page
        page_number = self.request.GET.get('page')  # Get the page number from the URL
        page_obj = paginator.get_page(page_number)

        context["projects"] = page_obj  # Paginated projects
        context["clients"] = ClientInfo.objects.filter(created_by=self.request.user)
        context["codes"] = Code.objects.filter(created_by=self.request.user)
        context["query"] = query  # Add query to context if needed in the template
        context["in_active_projects"] = Project.objects.filter(user=self.request.user, is_active=False)

        return context


class SettingseView(TemplateView):
    template_name = "dashboards/settings.html"  # Your template for dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_type'] = BusinessType.objects.all()
        try:
            context["profile"] = Profile.objects.get(id=self.request.user.profile.pk)
        except Profile.DoesNotExist:
            context["profile"] = None
        return context

    def post(self, request):

        profile = Profile.objects.get(id=request.user.profile.pk)

        if profile.profile_type == "jobseeker":
            job_profile, created = JOBProfile.objects.get_or_create()

            job_profile.qualification = request.POST.get("qualification") or None
            job_profile.date_of_birth = request.POST.get("date_of_birth") or None
            job_profile.sex = request.POST.get("sex") or None
            job_profile.current_resident_address = (
                request.POST.get("current_resident_address") or None
            )
            job_profile.business_type = request.POST.get("business_type")
            job_profile.adhar_no = request.POST.get("adhar_no") or None
            job_profile.pan_no = request.POST.get("pan_no") or None
            job_profile.marital_status = request.POST.get("marital_status") or None
            job_profile.spouse_name = request.POST.get("spouse_name") or None
            job_profile.children_count = request.POST.get("children_count") or None
            job_profile.emergency_contact_name = (
                request.POST.get("emergency_contact_name") or None
            )
            job_profile.emergency_contact_phone_no = (
                request.POST.get("emergency_contact_phone_no") or None
            )
            job_profile.emergency_contact_place = (
                request.POST.get("emergency_contact_place") or None
            )
            job_profile.emergency_contact_relationship = (
                request.POST.get("emergency_contact_relationship") or None
            )
            job_profile.passport_no = request.POST.get("passport_no") or None
            job_profile.work_choice = request.POST.get("work_choice") or None
            job_profile.looking_for_international = (
                request.POST.get("looking_for_international") or None
            )
            job_profile.expected_salary_hourly = (
                request.POST.get("expected_salary_hourly") or None
            )
            job_profile.expected_salary_daily = (
                request.POST.get("expected_salary_daily") or None
            )
            job_profile.expected_salary_monthly = (
                request.POST.get("expected_salary_monthly") or None
            )
            job_profile.insurance_policy_no = (
                request.POST.get("insurance_policy_no") or None
            )
            job_profile.insurance_policy_valid_upto = (
                request.POST.get("insurance_policy_valid_upto") or None
            )
            job_profile.insurance_company = (
                request.POST.get("insurance_company") or None
            )
            vehicle_owned = request.POST.get("vehicle_owned") == "on"
            job_profile.vehicle_type = request.POST.get("vehicle_type") or None
            job_profile.vehicle_registration_no = (
                request.POST.get("vehicle_registration_no") or None
            )
            job_profile.vehicle_usage = request.POST.get("vehicle_usage") or None
            job_profile.vehicle_insurance_policy_no = (
                request.POST.get("vehicle_insurance_policy_no") or None
            )
            job_profile.vehicle_insurance_company = (
                request.POST.get("vehicle_insurance_company") or None
            )
            job_profile.vehicle_accident_policy_valid_upto = (
                request.POST.get("vehicle_accident_policy_valid_upto") or None
            )
            if "passport_type_photo" in request.FILES:
                job_profile.passport_type_photo = request.FILES["passport_type_photo"]
            if "medical_report" in request.FILES:
                job_profile.medical_report = request.FILES["medical_report"]
                print(request.FILES["medical_report"])

            job_profile.save()

            job_profile.skills.set(request.POST.getlist("skills"))
            job_profile.physical_fitness.set(request.POST.getlist("physical_fitness"))
            job_profile.work_challenges.set(request.POST.getlist("work_challenges"))
            job_profile.vision.set(request.POST.getlist("vision"))
            job_profile.choice_of_work_place.set(
                request.POST.getlist("choice_of_work_place")
            )

                # Get or create job_profile for the current profile
            job_profile = getattr(profile, 'job_profile', None)
            if job_profile is None:
                # Create a new job_profile if it doesn't exist
                job_profile = JOBProfile.objects.create(profile=profile)

            # Add new Experience entries
            new_experiences = request.POST.getlist("new_experience_job_title")
            print("New experiences:", new_experiences)
            for i in range(len(new_experiences)):
                job_title = new_experiences[i]
                if job_title:
                    # Collect each field for the experience entry
                    experience = Experience(
                        job_title=job_title,
                        company_name=request.POST.getlist("new_experience_company_name")[i],
                        start_date=request.POST.getlist("new_experience_start_date")[i],
                        end_date=request.POST.getlist("new_experience_end_date")[i],
                        role_description=request.POST.getlist("new_experience_role_description")[i],
                    )
                    experience.save()  # Save each new experience
                    job_profile.experience.add(experience)  # Link experience to job_profile

            # Save the updated job_profile and associate it with the profile
            profile.job_profile = job_profile
            profile.save()  # Save profile with job_profile linked

        else:
            business_profile, created = BusinessProfile.objects.get_or_create()
            business_profile.industries = request.POST.get("industries")
            business_profile.business_type = request.POST.get("business_type")
            business_profile.scale = request.POST.get("scale")
            business_profile.company_name = request.POST.get("company_name")
            business_profile.company_type = request.POST.get("company_type")
            business_profile.cin_no = request.POST.get("cin_no")
            business_profile.gst_no = request.POST.get("gst_no")
            business_profile.whatsapp_mobile_no = request.POST.get("whatsapp_mobile_no")
            business_profile.location_link = request.POST.get("location_link")
            business_profile.address = request.POST.get("address")
            business_profile.google_plus_code = request.POST.get("google_plus_code")
            business_profile.work_history = request.POST.get("work_history")
            business_profile.photo_showcase = request.POST.get("photo_showcase")
            business_profile.video_showcase = request.POST.get("video_showcase")
            business_profile.company_size = request.POST.get("company_size")
            business_profile.project_brochures = request.FILES.get(
                "project_brochures", None
            )
            if "project_brochures" in request.FILES:
                business_profile.project_brochures = request.FILES["project_brochures"]

            business_profile.save()
            profile.business_profile = business_profile
            profile.save()

        profile.mid_name = request.POST.get("mid_name")
        profile.first_name = request.POST.get("first_name")
        profile.last_name = request.POST.get("last_name")
        profile.address = request.POST.get("address")
        profile.pan_no = request.POST.get("pan_no")
        profile.facebook_link = request.POST.get("facebook_link")
        profile.linkedin_link = request.POST.get("linkedin_link")
        profile.other_social_link = request.POST.get("other_social_link")
        profile.work_history = request.POST.get("work_history")
        profile.photo_showcase = request.POST.get("photo_showcase")
        profile.video_showcase = request.POST.get("video_showcase")
        profile.advertisement = request.POST.get("advertisement")
        profile.profile_type = profile.profile_type
        profile.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")

        if "profile_photo" in request.FILES:
            profile.profile_photo = request.FILES["profile_photo"]

        profile.save()
        messages.success(request, "Profile Updated Successfully...!")

        return redirect(reverse("profile:settings"))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/profile.html"  # Your template for dashboard

    def get_context_data(self, unique_id, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(unique_id=unique_id)
        return context

    def post(self, request):
        pass


class MasterView(LoginRequiredMixin, View):
    template_name = "dashboards/master.html"  # Your template for master

    def get(self, request, *args, **kwargs):
        context = {}
        executiongroup = ExecutionGroup.objects.all()
        unit = Unit.objects.all()
        brand = Brand.objects.all()
        materialgroup = MaterialGroup.objects.all()
        gst = GST.objects.all()
        workgroup = WorkGroup.objects.all()
        profession = Profession.objects.all()
        business_type = BusinessType.objects.all()
        context["unit"] = unit
        context["profession"] = profession
        context["brand"] = brand
        context["workgroup"] = workgroup
        context["materialgroup"] = materialgroup
        context["executiongroup"] = executiongroup
        context["gst"] = gst
        context["business_type"] = business_type
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        section = request.POST.get("section")
        value = request.POST.get("value")
        pk = request.POST.get("pk")
        new_pk = None

        model_mapping = {
            "units": Unit,
            "materials": MaterialGroup,
            "executiongroup": ExecutionGroup,
            "work_groups": WorkGroup,
            "professions": Profession,
            "business_types": BusinessType,
            "brands": Brand,
        }

        model = model_mapping.get(section)
        if model:
            if pk == "new":
                # Check for duplicates
                if model.objects.filter(name__iexact=value).exists():
                    return JsonResponse({"success": False, "error": "Duplicate entry"})
                else:
                    instance = model(name=value)
                    instance.save()
                    new_pk = instance.pk
            else:
                try:
                    instance = model.objects.get(pk=pk)
                    instance.name = value
                    instance.save()
                except model.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "error": "Invalid primary key"}
                    )

            return JsonResponse({"success": True, "new_pk": new_pk if new_pk else pk})

        return JsonResponse({"success": False, "error": "Invalid section"})


class DProView(LoginRequiredMixin, View):
    template_name = "dashboards/dpro.html"  # Your template for dpro

    def get(self, request, pk, *args, **kwargs):
        context = {}
        execution = Execution.objects.all()
        unit = Unit.objects.all()
        brand = Brand.objects.all()
        material = Material.objects.all()
        material_group = MaterialGroup.objects.all()
        execution_group = ExecutionGroup.objects.all()
        project_product = Material_Product.objects.filter(project=pk)
        exe_project_product = Execution_Product.objects.filter(project=pk)
        operational_cost = Operational_Costs.objects.all()
        operational_cost_product = Operational_Cost_product.objects.filter(project=pk)
        contract_margin = Contract_Margins.objects.all()
        contract_margin_product = Contract_Margin_product.objects.filter(project=pk)
        total_margin_cost = Total_Operational_cost.objects.filter(project=pk).first()
        formula = Formula.objects.all()
        context["unit"] = unit
        context["pk"] = pk
        context["brand"] = brand
        context["formula"] = formula
        context["material_group"] = material_group
        context["execution_group"] = execution_group
        context["material"] = material
        context["execution"] = execution
        context["total_margin_cost"] = total_margin_cost
        context["project_product"] = project_product
        context["exe_project_product"] = exe_project_product
        context["operational_cost"] = operational_cost
        context["operational_cost_product"] = operational_cost_product
        context["contract_margin"] = contract_margin
        context["contract_margin_product"] = contract_margin_product
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = json.loads(
            request.POST.get("data")
        )  # Parse the JSON string into a Python dictionary
        value = data.get("value")
        pk = data.get("pk")
        p_pk = data.get("project_pk")
        project_pk = Project.objects.get(pk=p_pk)
        section = data.get("section")
        print(section, "section")
        print(value, "value")
        print(pk, "pk")
        try:
            if pk == "new":
                # Create new Material_Product
                if section == "group":
                    group = MaterialGroup.objects.get(name=value)
                    material_product = Material_Product.objects.create(group=group)
                    material_product.project = project_pk
                    material_product.save()
                elif section == "unit":
                    unit = Unit.objects.get(pk=value)
                    print(unit, "hello")
                    material_product = Material_Product.objects.create(unit=unit)
                    material_product.project = project_pk
                    material_product.save()
                elif section == "brand":
                    brand = Brand.objects.get(name=value)
                    material_product = Material_Product.objects.create(brand=brand)
                    material_product.project = project_pk
                    material_product.save()
                elif section == "name":
                    material = Material.objects.filter(name=value).first()
                    material_product = Material_Product.objects.create(name=material)
                    material_product.project = project_pk
                    material_product.save()
                elif section == "gst":
                    gst = GST.objects.get(rate=value)
                    material_product = Material_Product.objects.create(gst=gst)
                    material_product.project = project_pk
                    material_product.save()
                else:
                    material_product = Material_Product.objects.create(
                        **{section: value}
                    )
                    material_product.project = project_pk
                    material_product.save()

            else:
                # Update existing Material_Product
                material_product = Material_Product.objects.get(pk=pk)
                if section == "group":
                    group = MaterialGroup.objects.get(name=value)
                    material_product.group = group
                elif section == "unit":
                    unit = Unit.objects.get(pk=value)
                    material_product.unit = unit
                elif section == "brand":
                    brand = Brand.objects.get(name=value)
                    material_product.brand = brand
                elif section == "name":
                    material = Material.objects.filter(name=value).first()
                    material_product.name = material
                elif section == "gst":
                    gst = GST.objects.get(rate=value)
                    material_product.gst = gst
                else:

                    setattr(material_product, section, value)

                material_product.save()

            return JsonResponse({"success": True, "new_pk": material_product.pk})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


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
    return JsonResponse({"materials": list(materials)})


def load_exe_materials(request):
    group = request.GET.get("group")
    if group.isdigit():  # Check if the group is a numeric value (pk)
        executions = Execution.objects.filter(group__pk=group).values(
            "name", "price", "unit__name", "gst__rate"
        )
    else:  # Otherwise, filter by group name
        executions = Execution.objects.filter(group__name=group).values(
            "name", "price", "unit__name", "gst__rate"
        )
    return JsonResponse({"executions": list(executions)})


def load_material_details(request):
    material_name = request.GET.get("material_name")
    material = Material.objects.get(name=material_name)
    gst = GST.objects.get(pk=material.gst.pk)
    unit = Unit.objects.get(pk=material.unit.pk)
    return JsonResponse(
        {
            "price": material.price,
            "gst": gst.rate,
            "brand": material.brand.name,
            "unit": unit.pk,
        }
    )


def load_execution_details(request):
    execution_name = request.GET.get("execution_name")
    execution = Execution.objects.get(name=execution_name)
    gst = GST.objects.get(pk=execution.gst.pk)
    unit = Unit.objects.get(pk=execution.unit.pk)
    return JsonResponse(
        {
            "price": execution.price,
            "gst": gst.rate,
            "brand": execution.name,
            "unit": unit.pk,
        }
    )


class DeleteProfilePhotoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Get the user's profile
        profile = get_object_or_404(Profile, user=request.user)

        # Check if there is a profile photo to delete
        print(profile.profile_photo)
        if profile.profile_photo:
            profile.profile_photo.delete()  # Delete the photo from storage
            profile.profile_photo = None  # Clear the field in the database
            profile.save()  # Save changes to the profile
            return JsonResponse(
                {"success": True, "message": "Profile picture deleted successfully."}
            )
        else:
            return JsonResponse(
                {"success": False, "message": "No profile picture to delete."}
            )


def delete_row(request):
    pk = request.POST.get("pk")
    try:
        material_product = Material_Product.objects.get(pk=pk)
        material_product.delete()
    except:
        pass
    return JsonResponse({"success": True})


def delete_exe_row(request):
    pk = request.POST.get("pk")
    print(pk)
    try:
        execution_product = Execution_Product.objects.get(pk=pk)
        execution_product.delete()
    except:
        pass
    return JsonResponse({"success": True})


def delete_operational_row(request):
    pk = request.POST.get("pk")
    print(pk)
    try:
        operational_product = Operational_Cost_product.objects.get(pk=pk)
        operational_product.delete()
    except:
        pass
    return JsonResponse({"success": True})


def delete_management_row(request):
    pk = request.POST.get("pk")
    print(pk)
    try:
        operational_product = Contract_Margin_product.objects.get(pk=pk)
        operational_product.delete()
    except:
        pass
    return JsonResponse({"success": True})


def delete_operational_row(request):
    pk = request.POST.get("pk")
    print(pk)
    try:
        operational_product = Operational_Cost_product.objects.get(pk=pk)
        operational_product.delete()
    except:
        pass
    return JsonResponse({"success": True})


def exe_save(request):
    data = json.loads(
        request.POST.get("data")
    )  # Parse the JSON string into a Python dictionary
    value = data.get("value")
    pk = data.get("pk")
    section = data.get("section")
    p_pk = data.get("project_pk")
    project_pk = Project.objects.get(pk=p_pk)
    # try:
    if pk == "new":
        # Create new Material_Product
        if section == "group":
            group = ExecutionGroup.objects.get(name=value)
            execution_product = Execution_Product.objects.create(group=group)
            execution_product.project = project_pk
            execution_product.save()
        elif section == "unit":
            unit = Unit.objects.get(pk=value)
            print(unit, "get")
            execution_product = Execution_Product.objects.create(unit=unit)
            print(execution_product, "prod")

            execution_product.project = project_pk
            execution_product.save()
        elif section == "brand":
            brand = Brand.objects.get(name=value)
            execution_product = Execution_Product.objects.create(brand=brand)
            execution_product.project = project_pk
            execution_product.save()
        elif section == "name":
            print(value, "vghhhh")
            execution = Execution.objects.filter(name=value).first()
            execution_product = Execution_Product.objects.create(name=execution)
            execution_product.project = project_pk
            execution_product.save()
        elif section == "gst":
            gst = GST.objects.get(rate=value)
            execution_product = Execution_Product.objects.create(gst=gst)
            execution_product.project = project_pk
            execution_product.save()
        else:
            execution_product = Execution_Product.objects.create(**{section: value})
            execution_product.project = project_pk
            execution_product.save()

    else:
        # Update existing Material_Product
        execution_product = Execution_Product.objects.get(pk=pk)
        if section == "group":
            group = ExecutionGroup.objects.get(name=value)
            execution_product.group = group
        elif section == "unit":
            unit = Unit.objects.get(pk=value)
            print(unit, "get")
            execution_product.unit = unit
        elif section == "brand":
            brand = Brand.objects.get(name=value)
            execution_product.brand = brand
        elif section == "name":
            execution = Execution.objects.filter(name=value).first()
            execution_product.name = execution
        elif section == "gst":
            gst = GST.objects.get(rate=value)
            execution_product.gst = gst
        else:
            setattr(execution_product, section, value)

    execution_product.save()

    return JsonResponse({"success": True, "new_pk": execution_product.pk})
    # except Exception as e:
    return JsonResponse({"success": False, "error": str(e)})


class CalculatorView(ProfileCompletionMixin,TemplateView):
    template_name = "dashboards/calculator.html"  # Your template for calculator


class ProjectInformation(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/project_information.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.get(pk=pk)
        context["project"] = project
        return context


def save_operational_cost(request):
    if request.method == "POST":
        data = json.loads(
            request.POST.get("data")
        )  # Parse the JSON string into a Python dictionary
        value = data.get("value")
        pk = data.get("pk")
        section = data.get("section")
        p_pk = data.get("project_pk")
        project_pk = Project.objects.get(pk=p_pk)

        if pk == "new":
            operational_cost_product = Operational_Cost_product()
            operational_cost_product.project = project_pk
            operational_cost_product.save()
        else:
            try:
                operational_cost_product = Operational_Cost_product.objects.get(pk=pk)
            except Operational_Cost_product.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Record not found"}, status=404
                )

        if section == "name":
            try:
                operational_cost_product.name = Operational_Costs.objects.get(
                    name=value
                )

            except Operational_Costs.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Operational Cost not found"},
                    status=404,
                )
        elif section == "allow_me":
            operational_cost_product.allow_me = value
        elif section == "formula":
            print(value)
            query=Formula.objects.get(name=value)
            print(query)
            operational_cost_product.formula =query
            operational_cost_product.save()
        elif section == "unit":
            try:
                operational_cost_product.unit = Unit.objects.get(pk=value)
            except Unit.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Unit not found"}, status=404
                )
        elif section == "gst":
            try:
                operational_cost_product.gst = GST.objects.get(rate=value)
            except GST.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "GST not found"}, status=404
                )
        elif section == "description":
            operational_cost_product.description = value

        operational_cost_product.save()

        return JsonResponse(
            {"status": "success", "new_pk": operational_cost_product.pk}
        )

    return JsonResponse(
        {"status": "error", "errors": "Invalid request method"}, status=400
    )


def get_operational_cost_data(request):
    if request.method == "GET":
        select_name = request.GET.get(
            "value", ""
        )  # Get the value from the query parameters
        if select_name:
            # Retrieve the operational cost data based on the selected execution_name
            cost_data = Operational_Costs.objects.filter(name=select_name)
            data = []
            if cost_data.exists():
                for item in cost_data:
                    data.append(
                        {
                            "pk": item.pk,
                            "allow_me": item.allow_me,
                            "gst": item.gst.rate,  # Adjust to your actual field
                            "unit": item.unit.pk,  # Assuming unit is a ForeignKey
                            "formula": item.formula.name,
                        }
                    )
                return JsonResponse({"status": "success", "data": data})
            else:
                return JsonResponse(
                    {"status": "error", "errors": "No operational cost data found"}
                )

        return JsonResponse({"status": "error", "errors": "Select name not provided"})

    return JsonResponse({"status": "error", "errors": "Invalid request method"})


def save_management_cost(request):
    if request.method == "POST":
        data = json.loads(
            request.POST.get("data")
        )  # Parse the JSON string into a Python dictionary
        value = data.get("value")
        pk = data.get("pk")
        section = data.get("section")
        print(value)
        p_pk = data.get("project_pk")
        project_pk = Project.objects.get(pk=p_pk)

        if pk == "new":
            contract_margin_product = Contract_Margin_product()
            contract_margin_product.project = project_pk
            contract_margin_product.save()
        else:
            try:
                contract_margin_product = Contract_Margin_product.objects.get(pk=pk)
            except contract_margin_product.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Record not found"}, status=404
                )

        if section == "name":
            try:
                contract_margin_product.name = Contract_Margins.objects.get(name=value)
            except contract_margin_product.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Operational Cost not found"},
                    status=404,
                )
        elif section == "allow_me":
            contract_margin_product.allow_me = value
        elif section == "formula":
            contract_margin_product.formula = Formula.objects.get(name=value)
        elif section == "unit":
            try:
                contract_margin_product.unit = Unit.objects.get(pk=value)
            except Unit.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Unit not found"}, status=404
                )
        elif section == "gst":
            try:
                contract_margin_product.gst = GST.objects.get(rate=value)
            except GST.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "GST not found"}, status=404
                )
        elif section == "description":
            contract_margin_product.description = value

        contract_margin_product.save()

        return JsonResponse({"status": "success", "new_pk": contract_margin_product.pk})

    return JsonResponse(
        {"status": "error", "errors": "Invalid request method"}, status=400
    )


def get_management_cost_data(request):
    if request.method == "GET":
        select_name = request.GET.get(
            "value", ""
        )  # Get the value from the query parameters
        if select_name:
            # Retrieve the operational cost data based on the selected execution_name
            cost_data = Contract_Margins.objects.filter(name=select_name)
            data = []
            if cost_data.exists():
                for item in cost_data:
                    data.append(
                        {
                            "pk": item.pk,
                            "allow_me": item.allow_me,
                            "gst": item.gst.rate,  # Adjust to your actual field
                            "unit": item.unit.pk,  # Assuming unit is a ForeignKey
                            "formula": item.formula.name,
                        }
                    )
                return JsonResponse({"status": "success", "data": data})
            else:
                return JsonResponse(
                    {"status": "error", "errors": "No operational cost data found"}
                )

        return JsonResponse({"status": "error", "errors": "Select name not provided"})

    return JsonResponse({"status": "error", "errors": "Invalid request method"})


def totalsave_operational_cost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Parse the JSON string into a Python dictionary
        value = data.get("value")
        pk = data.get("pk")
        section = data.get("section")
        p_pk = data.get("pk")
        project_pk = Project.objects.get(pk=p_pk)
        operation_cost = Total_Operational_cost.objects.filter(
            project=project_pk
        ).first()
        print(section, "ftgg")

        if not operation_cost:
            operational_cost_product = Total_Operational_cost()
            operational_cost_product.project = project_pk
            operational_cost_product.save()
        else:
            try:
                operational_cost_product = Total_Operational_cost.objects.get(
                    project=project_pk
                )
            except Operational_Cost_product.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Record not found"}, status=404
                )

        if section == "name":
            try:
                operational_cost_product.name = Total_Operational_cost.objects.get(
                    name=value
                )

            except Operational_Costs.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Operational Cost not found"},
                    status=404,
                )
        elif section == "allow_me":
            operational_cost_product.allow_me = value
        elif section == "unit":
            try:
                operational_cost_product.unit = Unit.objects.get(pk=value)
            except Unit.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "Unit not found"}, status=404
                )
        elif section == "gst":
            try:
                operational_cost_product.gst = GST.objects.get(pk=value)
            except GST.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "GST not found"}, status=404
                )
        elif section == "formula":
            try:
                operational_cost_product.formula = Formula.objects.get(name=value)
            except GST.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "errors": "GST not found"}, status=404
                )
        elif section == "description":
            operational_cost_product.description = value

        operational_cost_product.save()

        return JsonResponse(
            {"status": "success", "new_pk": operational_cost_product.pk}
        )

    return JsonResponse(
        {"status": "error", "errors": "Invalid request method"}, status=400
    )


@login_required
def remove_medical_report(request):
    if request.method == "POST":
        # Fetch the profile instance related to the logged-in user
        profile = request.user.profile  # Adjust this if your profile retrieval logic differs

        # Remove the medical report file
        profile.job_profile.medical_report.delete(save=False)  # Deletes the file from storage
        profile.job_profile.medical_report = None  # Clears the field in the database
        profile.job_profile.save()

        return JsonResponse({"status": "success", "message": "Medical report removed successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)