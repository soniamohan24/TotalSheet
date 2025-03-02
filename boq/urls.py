from django.urls import path
from . import views
from .views import *

app_name = "boq"

urlpatterns = [
    path("boq/<int:pk>/", BOQVIEW.as_view(), name="boq"),
    path("boq/<int:pk>/create-table/", create_table, name="boq-create-table"),
    path("boq/<int:pk>/total/", save_total, name="boq-total"),
    path("boq/<int:pk>/table-name/", save_table_name, name="boq-table-name"),
    path("contact-list/", ContactList.as_view(), name="contact-list"),
    path("contact-form/", ContactForm.as_view(), name="contact-form"),
    path("load-materials/", load_materials, name="load_materials"),
    path("boq_calculation/", boq_calculation, name="boq_calculation"),
    path('deleterow/',delete_row, name='delete_row'),
]
