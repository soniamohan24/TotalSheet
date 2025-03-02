from .models import *
from .utils_models import Socials, Website
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64, json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


def update_picture(request):
    try:
        profile = Profile.objects.get(id=request.POST.get("id"))

        image_data = request.POST.get("img")
        if image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            filename = f"profile_picture_{profile.id}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=filename)
            profile.profile_photo.save(filename, data, save=True)
        return JsonResponse({"status": "success"})

    except Profile.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "Profile not found"})
    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)})


def add_social_link(request):
    data = request.POST
    profile = Profile.objects.get(id=data.get("id"))
    social = Socials.objects.create(
        social_type=data.get("social_type"), link=data.get("link")
    )
    profile.social_link.add(social)

    return redirect(reverse("profile:settings"))


def add_website_link(request):
    data = request.POST
    profile = Profile.objects.get(id=data.get("id"))
    social = Website.objects.create(url=data.get("url"))
    profile.website.add(social)
    return redirect(reverse("profile:settings"))


def add_work_history(request):
    data = request.POST
    profile = Profile.objects.get(id=data.get("id"))

    print(data)
    if not profile.job_profile:
        profile.job_profile = JOBProfile.objects.create()
        profile.save()

    profile.job_profile.short_work_history = data.get("short_history")
    profile.job_profile.work_history = data.get("long_history")
    profile.job_profile.save()

    return redirect(reverse("profile:settings"))


@require_POST
@csrf_exempt
def delete_social(request):

    try:
        data = json.loads(request.body)
        social_id = data.get("id")
        print(social_id)

        if not social_id:
            return JsonResponse({"success": False, "error": "No social ID provided"})

        social = Socials.objects.filter(pk=social_id).first()
        print(social)

        if not social:
            return JsonResponse({"success": False, "error": "Social link not found"})

        profile = Profile.objects.filter(social_link=social, user=request.user).first()

        if not profile:
            return JsonResponse(
                {"success": False, "error": "Unauthorized to delete this social link"}
            )

        profile.social_link.remove(social)

        social.delete()

        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_POST
@csrf_exempt
def delete_website(request):
    try:
        data = json.loads(request.body)
        website_id = data.get("id")

        if not website_id:
            return JsonResponse({"success": False, "error": "No website ID provided"})

        website = Website.objects.filter(id=website_id).first()

        if not website:
            return JsonResponse({"success": False, "error": "Website link not found"})

        profile = Profile.objects.filter(website=website, user=request.user).first()

        if not profile:
            return JsonResponse(
                {"success": False, "error": "Unauthorized to delete this website link"}
            )

        profile.website.remove(website)

        website.delete()

        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
