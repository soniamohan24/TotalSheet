from django.urls import path
from .views import *
from . import views

app_name = "report"
urlpatterns = [
    path("report/<int:pk>/", ReportView.as_view(), name="report"),
]
