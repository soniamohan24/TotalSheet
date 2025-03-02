from django.contrib.auth import get_user_model
import random
import json, time
from django.db import IntegrityError
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
from boq.models import CustomUser
from profile.models import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from .forms import PhoneNumberForm, PasswordForm, OTPRequestForm
from boq.models import *
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.signing import Signer, BadSignature


def register(request):
    if request.method == "GET":

        return render(request, "account/register.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("accounts:login"))


def request_otp(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            print( phone_number)
            # Check if email already exists in the database
            if email and CustomUser.objects.filter(username=email).exists():
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Email already exists. Please use a different email.",
                    }
                )

            otp_value = generate_otp()
            print(otp_value)

            # Create user or get existing user

            # Save OTP to database
            otp = OTP(email=email, otp_value=otp_value)
            otp.save()

            # Send OTP to user
            if email:
                send_mail(
                    "Total Sheets - OTP",
                    f"Your OTP code is {otp_value}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

            elif phone_number:
                # Send OTP via SMS
                pass

            request.session["user_info"] = {
                "email": email,
                "phone_number": phone_number,
            }
            return JsonResponse({"success": True, "message": "OTP sent successfully."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})


def resend_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone_number = request.POST.get("number")
        get_otp_value = OTP.objects.filter(email=email).last()
        otp_value = get_otp_value.otp_value

        # Send OTP to user
        if email:
            send_mail(
                "Total Sheets - OTP",
                f"Your OTP code is {otp_value}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

        elif phone_number:
            # Send OTP via SMS
            pass

        return JsonResponse({"success": True, "message": "OTP resent successfully."})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})


def verify_otp(request):
    if request.method == "POST":
        user_info = request.session.get("user_info")
        if not user_info:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Session expired. Please request OTP again.",
                }
            )

        email = user_info.get("email")
        phone_number = user_info.get("phone_number")
        print(phone_number,'user')
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            otp_value = form.cleaned_data["otp"]

            try:
                otp = OTP.objects.filter(email=email, otp_value=otp_value).latest(
                    "created_at"
                )
                if otp.is_expired():
                    return JsonResponse(
                        {"success": False, "message": "OTP has expired."}
                    )
                else:
                    normalized_email = email.lower().strip()
                    print("hello")
                    user = CustomUser.objects.create(
                        username=normalized_email, email=normalized_email,phone_number= phone_number
                    )
                    # Profile.objects.create(user=user)
                    otp.is_verified = True
                    otp.save()
                    request.session["user_id"] = user.id
                    return JsonResponse(
                        {"success": True, "message": "OTP verified successfully."}
                    )
            except OTP.DoesNotExist:
                return JsonResponse({"success": False, "message": "Invalid OTP."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "message": "Invalid request method."})


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(user, otp, identifier):
    if "@" in identifier:
        # Send OTP via email (if you have implemented email sending logic)
        pass
    else:
        # Send OTP via SMS using Twilio
        client = settings.TWILIO_CLIENT
        message_body = f"Your OTP is: {otp}"
        try:
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=identifier,
            )
            print(f"Sent OTP to {identifier}")
        except Exception as e:
            print(f"Failed to send OTP to {identifier}: {e}")
            # Handle error (log, retry, etc.)


def set_password(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        print("User ID from session:", user_id)
        if not user_id:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Session expired. Please request OTP again.",
                }
            )

        try:
            user = CustomUser.objects.get(pk=user_id)
            print("User retrieved:", user)
        except CustomUser.DoesNotExist:
            print("User does not exist with the provided user_id")
            return JsonResponse({"success": False, "message": "User does not exist."})

        form = PasswordForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            if password == confirm_password:
                user.set_password(password)
                user.email = user.username
                print("Password hashed and set for user:", user.email)
                user.save()
                print("User saved with new password")

                # Double-check the password was set correctly
                if not user.check_password(password):
                    print("Password was not set correctly")
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "Failed to set password. Please try again.",
                        }
                    )

                # Attempt to authenticate the user
                print("Attempting to authenticate user with email:", user.email)
                user = authenticate(request, email=user.email, password=password)
                print("Authentication attempt result:", user)
                if user is not None:
                    login(request, user)
                    print("User logged in successfully")
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Password set successfully. Logging in...",
                            "redirect_url": "/dashboard/",
                        }
                    )
                else:
                    print("Authentication failed with provided credentials")
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "Authentication failed. Please try again.",
                        }
                    )
            else:
                print("Passwords do not match")
                return JsonResponse(
                    {"success": False, "error": "Passwords do not match."}
                )
        else:
            print("Form errors:", form.errors)
            return JsonResponse({"success": False, "errors": form.errors})


class ClientLoginView(TemplateView):
    template_name = "account/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("profile:dashboard"))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        remember_me = "rememberme" in request.POST
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            return redirect(reverse("profile:dashboard"))
        return render(
            request, self.template_name, {"error": "Invalid email or password"}
        )


class ForgotPasswordView(TemplateView):
    template_name = "account/forgot_password.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if not email:
            return render(request, self.template_name, {"error": "Email is required."})

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user:
                signer = Signer()
                token = signer.sign(str(time.time()))
                send_mail(
                    "Password Reset Request",
                    f'Hello {user.first_name if user.first_name else "User"}, \nHere is your password reset link: {request.build_absolute_uri(reverse("accounts:reset-password"))}?token={token} \nNote: The token expires in 3 mins',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            return redirect("accounts:email-sent")
        except User.DoesNotExist:
            return render(
                request,
                self.template_name,
                {"error": "No user is registered with this email address."},
            )


class EmailSentView(TemplateView):
    template_name = "account/email_sent.html"


class ResetPasswordView(TemplateView):
    template_name = "account/reset_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = kwargs.get("user_id")
        context["token"] = kwargs.get("token")  # Include token in the context
        return context

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        user_id = kwargs.get("user_id")

        if not token:
            return render(request, self.template_name, {"error": "Invalid token."})

        signer = Signer()
        try:
            timestamp = float(signer.unsign(token))
            if time.time() - timestamp > 180:  # Token expires in 3 minutes
                return render(
                    request,
                    self.template_name,
                    {"error": "Token has expired.", "check": False},
                )

            context = self.get_context_data(user_id=user_id, token=token)
            context["check"] = True
            return render(request, self.template_name, context)
        except BadSignature:
            return render(request, self.template_name, {"error": "Invalid token."})

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        user_id = request.POST.get("user_id")
        token = request.POST.get("token")
        print(token)
        User = get_user_model()

        if not password or not confirm_password:
            return render(
                request, self.template_name, {"error": "Both fields are required."}
            )

        if password != confirm_password:
            return render(
                request, self.template_name, {"error": "Passwords do not match."}
            )

        signer = Signer()
        try:
            # Verify the token
            timestamp = float(signer.unsign(token))
            if time.time() - timestamp > 180:  # Token expires in 3 minutes
                return render(
                    request, self.template_name, {"error": "Token has expired."}
                )

            User = get_user_model()
            user = User.objects.get(id=user_id)
            user.password = make_password(password)
            user.save()
            return redirect(
                "accounts:login"
            )  # Redirect to login after successful reset
        except (User.DoesNotExist, BadSignature):
            return render(
                request, self.template_name, {"error": "Invalid token or user."}
            )


@login_required  # Ensure the user is logged in
@csrf_exempt
def complete_registration(request):
    if request.method == "POST":
        # Retrieve the profile type from the POST request
        profile_type = request.POST.get("type")

        # Validate the profile type
        if profile_type not in ["jobseeker", "business"]:
            return JsonResponse({"success": False, "error": "Invalid profile type."})

        # Update or create UserProfile based on the profile type
        user = request.user
        profile_exists = Profile.objects.filter(user=user).exists()

        if not profile_exists:
            try:
                # Create a new Profile instance
                profile = Profile.objects.create(user=user)

                profile.save()
                print("A new profile was created.")
            except IntegrityError as e:
                print("Error: IntegrityError -", e)
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Profile creation failed due to an integrity error.",
                    }
                )
        else:
            profile = Profile.objects.get(user=user)
            print("Profile already exists.")

        # Update the profile type and save
        profile.type = profile_type
        profile.save()

        # Redirect to login
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})
