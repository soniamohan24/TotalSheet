from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import Profile  # Adjust the import based on your app structure


class ProfileCompletionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                incomplete_fields = profile.incomplete_fields()

                if incomplete_fields:
                    fields_list = " and ".join(incomplete_fields)
                    messages.error(
                        request,
                        f"Please enter your {fields_list} to proceed with accessing the Dashboard."
                        # f"Please fill in the following information before continuing your profile: {fields_list} ",
                    )
                    return redirect(
                        reverse("profile:settings")
                    )  # Replace with your actual profile update URL

            except Profile.DoesNotExist:
                return redirect(reverse("profile:settings"))

        return super().dispatch(request, *args, **kwargs)
