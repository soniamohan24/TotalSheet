from django.urls import path
from . import views
from .views import *

app_name = "code"

urlpatterns = [
    path("code/", CodeView.as_view(), name="code"),
    path("update_code/<int:code_id>/", CodeView.as_view(), name="update_code"),
    path("specification/", SpecificationView.as_view(), name="specification"),
    path('duplicate_code/<int:code_id>/', DuplicateCodeView.as_view(), name='duplicate_code'),
    path('specification/<int:pk>/delete/', SpecificationDeleteView.as_view(), name='specification_delete'),
]