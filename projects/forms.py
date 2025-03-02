from django import forms
from projects.models import Project
from boq.models import ClientInfo


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
    client = forms.ModelChoiceField(
        queryset=ClientInfo.objects.all(),
        required=True,
        widget=forms.Select,
        label="Client",
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "project_type",
            "interior_project_photo",
            "exterior_project_photo",
            "project_brocher",
            "place",
            "webside",
            "location_link",
            "construction_area",
            "building_license_no",
            "Building_rera_license",
            "social_link",
            "start_date",
            "end_date",
            "pincode",
            "client",
            'drawings',
            'documents'
        ]

        def clean_client(self):
            client = self.cleaned_data.get("client")
            if not client:
                raise forms.ValidationError("Client is required.")
            return client


class ProjectSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search for Projects",
                "class": "form-control rounded-pill",
            }
        ),
    )
class ClientInfoForm(forms.ModelForm):
    class Meta:
        model = ClientInfo
        fields = ['first_name', 'last_name', 'address', 'pan_no', 'cin_no', 'company_name', 'website', 'social_link']