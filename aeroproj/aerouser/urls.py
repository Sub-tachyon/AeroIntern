from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login, name="login"),
    path("signup",views.signup, name="signup" ),
    path("forgot/",views.forgot, name="forgot"),
    path("otp_verification",views.otp, name="otp_verification"),
    path("password_change/<str:token>",views.password_reset, name="password_change"),
]
