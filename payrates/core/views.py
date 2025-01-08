from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

class Dashboard( LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        userType = request.user.user_typ
        return render(request, 'core/pages/dashboard.html')  
    
    
class Services( LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/services.html')
    
class ServiceDetail( LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/service_detail.html')
    
class PropertyList( LoginRequiredMixin, View):

    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/property_list.html')

class PropertyDetail( LoginRequiredMixin, View):
    
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/property_detail.html')
    
    
class Applications( LoginRequiredMixin, View):
    
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/applications.html')
    
class CompanyProfile( LoginRequiredMixin, View):
    
    login_url = "users:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(request, 'core/pages/company_profile.html')