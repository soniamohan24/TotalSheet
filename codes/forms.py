from django import forms



class CodeDuplicateForm(forms.Form):
    material_code = forms.CharField(max_length=100, required=True)
    execution_code = forms.CharField(max_length=100, required=True)