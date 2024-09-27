from django.shortcuts import render
from django.views import View
# Create your views here.
from email.message import EmailMessage
from multiprocessing import context
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
# from .models import Account
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# verification email modules
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:services")
        return render(request, 'accounts/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been logged in!')
                return redirect('core:services')
            else:
                return HttpResponse('Your account is not active!')
        else:
            # print(request, 'Invalid Credentials!')
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:login')
    
    
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:services")
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        try:
            formdata  = request.POST
            print(formdata)
            username  = formdata['email']
            email     = formdata['email']
            password1 = formdata['password']
            password2 = formdata['password2']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.first_name = formdata['firstName']
            user.last_name  = formdata['lastName']
            user.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect("accounts:login")
        except Exception as e:
            print(e)
            messages.error(request, f'Something went wrong! {e}')
            return  redirect('accounts:register')
    
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

class ProfileView(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    
    def get(self,request):
        return render(request,"accounts/profile.html")
    
    def post(self,request):
        profile_info = request.POST
        firstName = profile_info['firstName']
        lastName = profile_info['lastName']
        email = profile_info['email']
        # update user table
        user = request.user
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.save()
        # update profile table
        profile = request.user.profile
        profile.phone = profile_info['phone']
        profile.county = profile_info['county']
        profile.town = profile_info['town']
        profile.municipality = profile_info['municipality']
        profile.save()
        return redirect('accounts:myprofile')

