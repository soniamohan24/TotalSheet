from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("request-otp/", request_otp, name="request_otp"),
    path("resend-otp", resend_otp, name="resend_otp"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("set-password/", set_password, name="set_password"),
    path("login/", ClientLoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("email-sent/", EmailSentView.as_view(), name="email-sent"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("complete-registration/", complete_registration, name="complete_registration"),
]
