from django.urls import path
from .views import *
from . import views
from .api import *

app_name = "profile"


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/<str:unique_id>/", ProfileView.as_view(), name="profile"),
    path("settings/", SettingseView.as_view(), name="settings"),
    path("profile_update/", ProfileUpdateView.as_view(), name="profile-update"),
    path(
        "delete_profilepic/",
        DeleteProfilePhotoView.as_view(),
        name="delete-profile-pic",
    ),
    path("master/", MasterView.as_view(), name="master"),
    path("dpro/<int:pk>/", DProView.as_view(), name="dpro"),
    path("calculator/", CalculatorView.as_view(), name="calculator"),
    path("load-materials/", load_materials, name="load_materials"),
    path("load-material-details/", load_material_details, name="load_material_details"),
    path(
        "save-operational-cost/",
        views.save_operational_cost,
        name="save-operational-cost",
    ),
    path(
        "totalsave-operational-cost/",
        views.totalsave_operational_cost,
        name="totalsave-operational-cost",
    ),
    path(
        "get-operational-cost-data/",
        get_operational_cost_data,
        name="get-operational-cost-data",
    ),
    path(
        "save-management-cost/", views.save_management_cost, name="save-management-cost"
    ),
    path(
        "get-management-cost-data/",
        get_management_cost_data,
        name="get-management-cost-data",
    ),
    path("delete-row/", delete_row, name="delete_row"),
    path(
        "delete-operational-row/", delete_operational_row, name="delete-operational-row"
    ),
    path("delete-management-row/", delete_management_row, name="delete-management-row"),
    path("load-exe-materials/", load_exe_materials, name="load-exe-materials"),
    path(
        "load-execution-details/", load_execution_details, name="load-execution-details"
    ),
    path("delete-exe-row/", delete_exe_row, name="delete-exe-row"),
    path("exe_save/", exe_save, name="exe_save"),
    # API
    path("api/profile-picture/", update_picture, name="profile-picture-upload"),
    path("api/add-social", add_social_link, name="add-social"),
    path("api/add-website", add_website_link, name="add-website"),
    path("api/add-work-history", add_work_history, name="add-work-history"),
    path("api/delete-social", delete_social, name="delete-social"),
    path("api/delete-website", delete_website, name="delete-website"),
path('remove-medical-report/', views.remove_medical_report, name='remove_medical_report'),
]
