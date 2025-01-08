from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.core.mail import send_mail


# Create your views here.
class LoginView(View):
    template_name = "users/login.html"
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data.get("remember_me", False)
            # authentication
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                # set expiry time for session
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                messages.success(request, "You have successfully logged in.")
                return redirect("core:dashboard")
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("users:login")
        else:
            return redirect("users:login")


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            # check if passwords match
            # if password != confirm_password:
            #     messages.error(request, 'Passwords do not match.')
            #     return redirect('users:register')
            # create user
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            if user:
                messages.success(request, "You have successfully registered.")
                return redirect("users:login")
            else:
                messages.error(request, "Registration failed.")
                return redirect("users:register")
        else:
            return redirect("users:register")


class ResetPasswordView(View):
    template_name = "users/reset-password.html"

    def get(self, request):
        return render(request, self.template_name)


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/reset-password.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")
    
    def form_valid(self, form):
        # Add custom logic here (e.g., logging or notifications)
        response = super().form_valid(form)
        user_email = form.cleaned_data.get('email')
        send_mail(
            subject="Password Reset Request",
            message="We received a request to reset your password.",
            from_email="noreply@yourdomain.com",
            recipient_list=[user_email],
        )
        return response


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/reset-password-done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/reset-password-confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/reset-password-complete.html"
