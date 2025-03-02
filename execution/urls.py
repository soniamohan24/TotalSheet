from django.urls import path
from .views import *


app_name = "execution"

urlpatterns = [
    path("fetch-subgroups/", fetch_subgroups, name="fetch_subgroups"),
]