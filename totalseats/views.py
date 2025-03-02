from django.shortcuts import redirect
from django.urls import reverse


def redirect_view(request):
    return redirect(reverse("accounts:login"))
