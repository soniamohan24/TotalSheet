from django.urls import path
from .views import *


app_name = "materials"

urlpatterns = [
    path("fetch-subgroups/", fetch_subgroups, name="fetch_subgroups"),
     path('get-subgroups/<int:group_id>/', get_subgroups, name='get_subgroups'),
]
