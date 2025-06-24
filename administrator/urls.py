from django.urls import path
from .views import *

app_name = "administrator"
#dddddd
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("master/", MasterView.as_view(), name="master"),
    path("user-management/", UserManagementView.as_view(), name="user_management"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("search/", DynamicListView.as_view(), name="search"),
    path(
        "<str:model_name>/create/", DynamicCreateView.as_view(), name="dynamic-create"
    ),
    path(
        "<str:model_name>/<int:pk>/update/",
        DynamicUpdateView.as_view(),
        name="dynamic-update",
    ),
    path(
        "<str:model_name>/<int:pk>/delete/",
        DynamicDeleteView.as_view(),
        name="dynamic-delete",
    ),
    path(
        "<str:model_name>/<int:pk>/", DynamicDetailView.as_view(), name="dynamic-detail"
    ),
    path("<str:model_name>/", DynamicListView.as_view(), name="dynamic-list"),
    path("material_group/subgroups/", SubGroupCreateView.as_view(), name="subgroups"),
    path(
        "execution_group/ex_subgroups/",
        EXSubGroupCreateView.as_view(),
        name="ex_subgroups",
    ),
    path(
        "business_type/business_subgroups/",
        BusinessSubGroupCreateView.as_view(),
        name="business_subgroups",
    ),
    path("brand/<int:pk>/remove-logo/", remove_logo, name="remove-logo"),
    path(
        "industry/industry_subgroups/",
        WorkGroupSubGroupCreateView.as_view(),
        name="workgroup_subgroups",
    ),
    path(
        "workgroup/workgroup_subgroups/",
        CodeGroupSubGroupCreateView.as_view(),
        name="codegroup_subgroups",
    ),
]
