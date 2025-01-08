from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('services/', views.Services.as_view(), name='services'),
    path('property_list/', views.PropertyList.as_view(), name='property_list'),
    path('applications/', views.Applications.as_view(), name='applications'),
    path('companyProfile/', views.CompanyProfile.as_view(), name='companyProfile'),
]