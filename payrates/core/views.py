from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from users.models import Profile
from .models import *
from users.forms import LoginForm
# Create your views here.


def index(request):
    return render(request, "core/index.html")


class Dashboard(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"
    property = Property.objects.all()
    profile = Profile.objects.all()

    def get(self, request):
        userType = self.profile.get(user=request.user).role
        if userType == "user":  # normal user
            prop = self.property.filter(client=request.user)
        elif userType == "superAdmin":  # super admin
            prop = self.property.all()
        elif userType == "admin":  # county admin
            county = self.profile.filter(user=request.user).county
            prop = self.property.filter(county=county)

        return render(
            request,
            "core/pages/dashboard.html",
            context={
                "property": prop,
            },
        )


class Services(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/services.html")


class ServiceDetail(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/service_detail.html")


class PropertyList(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    profile = Profile.objects.all()
    form  = LoginForm()
    def get(self, request):
        usertype = self.profile.get(user=request.user).role
        return render(
                request,
                "core/pages/property_list.html",
                context={"usertype": usertype, "form": self.form},
            )


class PropertyDetail(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/property_detail.html")


class Applications(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/applications.html")


class CompanyProfile(LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/company_profile.html")
