from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Code)
admin.site.register(code_Execution)
admin.site.register(code_Material)
admin.site.register(code_OnSiteExpense)
admin.site.register(code_OffSiteExpense)
