from django.urls import path
from .views import *


app_name = "project"
urlpatterns = [
    path("create_project/", ProjectCreateView.as_view(), name="create_project"),
    path(
        "project/<int:pk>/",
        ProjectInformation.as_view(),
        name="project_information",
    ),
    path("project/<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"
    ),
    path("clients/", clients.as_view(), name="clients"),
    path("add_to_projectlist/<int:pk>/",ProjectActiveView.as_view(), name="addproject_list"),
    path("add-client/", ClientCreateView.as_view(), name="add-client"),
    path("search/", project_search, name="project_search"),
    path("client-search/", client_search, name="client_search"),
    path("clients/add/", ClientCreateView.as_view(), name="add-client"),
    path("clients/download/", DownloadClientsView.as_view(), name="download-clients"),
    path("clients/upload/", BulkUploadClientsView.as_view(), name="upload-clients"),
    path('edit-client/<int:pk>/', EditClientView.as_view(), name='edit-client'),
    path('delete-client/<int:pk>/',DeleteClientView.as_view(), name='delete-client'),
    path(
        "toggle-favorite/<int:client_id>/",
        ToggleFavoriteView.as_view(),
        name="toggle-favorite",
    ),
]
