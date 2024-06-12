from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("services/",views.OurServices.as_view(),name="services"),
    path("add_services/",views.ServiceAdd.as_view(),name="add_services"),
    path("service_details/<int:servid>",views.ServiceDetails.as_view(),name="service_details"),
    path("service_price/<int:servid>/<int:townid>",views.ServicePrice.as_view(),name="service_price"),
    path("edit_services/<int:servid>",views.ServiceEdit.as_view(),name="edit_services"),
    path("delete_service/<int:servid>",views.ServiceDelete.as_view(),name="delete_service"),
    path("myapplications/",views.ApplicationsListing.as_view(),name="myapplications"),
    path("application_details/<int:aplid>",views.ApplicationDetails.as_view(),name="details"),
    path("applicationsreceived/",views.ApplicationsReceived.as_view(),name="received"),
    path("performance/",views.Dashboard.as_view(),name="performance"),
    path("companyProfile/",views.CompanyDetails.as_view(),name="companyProfile"),
    # requirements
    path("requirements/",views.Requirements.as_view(),name="requirements"),
    # pricing
    path("pricing/",views.Pricing.as_view(),name="pricing"),
    path("payments/",views.PaymentUpdates.as_view(),name="payments"),
]
