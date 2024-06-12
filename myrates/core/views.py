import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


from accounts.models import Profile
from .models import (
    ApplicationFiles,
    ApplicationRecords,
    CompanyProfile,
    Services,
    ServiceRequirements,
    Towns,
    Prices,
)
from django.core.files.storage import FileSystemStorage

# Create your views here.


class Dashboard( LoginRequiredMixin, View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        enquiries = ApplicationRecords.objects.all()
        context = {
            "total_enquiries": enquiries.count(),
            "new": enquiries.filter(resolution="New").count(),
            "queued": enquiries.filter(resolution="Queued").count(),
            "closed": enquiries.filter(resolution="Closed").count(),
        }
        return render(request, "core/dashboard.html", context)


class Requirements(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    def post(self, request):
        requirements = request.POST
        requirement = requirements["requirement"]
        requirement = ServiceRequirements(requirement=requirement)
        requirement.save()
        return redirect("core:add_services")


class OurServices(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    def get(self, request):
        services = Services.objects.all()
        context = {"services": services}
        return render(request, "core/services.html", context)


class ServiceAdd(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    def get(self, request):
        requirements = ServiceRequirements.objects.all()
        context = {"requirements": requirements}
        return render(request, "core/pages/new_service.html", context)

    def post(self, request):
        try:
            service_details = request.POST
            title = service_details["title"]
            description = service_details["description"]
            requirements = service_details["requirement"]
            service = Services(
                title=title, description=description, requirements=requirements
            )
            service.save()
            messages.success(request, "Service added successfully!")
            return redirect("core:services")
        except Exception as e:
            messages.error(request, f"Something went wrong! {e}")
            return render(request, "core/pages/new_service.html")


class ServiceDetails(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    def get(self, request, servid):
        service = Services.objects.get(id=servid)
        towns = Towns.objects.all()
        companyinfo = CompanyProfile.objects.all().last()
        context = {"service": service, "towns": towns, "companyinfo": companyinfo}
        return render(request, "core/pages/service_details.html", context)

    def post(self, request, servid):
        try:
            if request.POST["formid"] == "apply":

                uploadedfiles = request.FILES
                fs = FileSystemStorage()
                uploaded_file_urls = []
                for file in uploadedfiles.keys():
                    file_uploaded = uploadedfiles[file]
                    fileName = f"{file}_{request.user.id}_{servid}_{file_uploaded.name}"
                    fs.save(fileName, file_uploaded)
                    uploaded_file_urls.append(fileName)
                apl = ApplicationRecords(
                    user=User.objects.get(id=request.user.id),
                    service=Services.objects.get(id=servid),
                    amount=request.POST["amount"],
                    paymentStatus="Pending",
                    resolution="New",
                    transactioncode=request.POST["transactioncode"],
                    filesUploaded=",".join(uploaded_file_urls),
                )
                apl.save()
                messages.success(request, "Application submitted successfully!")
                return redirect("core:services")
            elif request.POST["formid"] == "paymentupdate":
                application = ApplicationRecords.objects.get(
                    id=request.POST["applicationid"]
                )
                application.amount = request.POST["amount"]
                application.transactioncode = request.POST["transactioncode"]
                application.save()
                messages.success(request, "Payment details updated successfully!")
                return redirect("core:details", aplid=application.id)
        except Exception as e:
            messages.error(f"An error occured!{e}")
            return redirect("core:services")


class ServiceEdit(LoginRequiredMixin,View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    def get(self, request, servid):
        service = Services.objects.get(id=servid)
        context = {"service": service}
        return render(request, "core/pages/edit_services.html", context)

    def post(self, request, servid):
        try:
            service_details = request.POST
            title = service_details["title"]
            description = service_details["description"]
            service = Services.objects.get(id=servid)
            service.title = title
            service.description = description
            service.save()
            messages.success(request, "Service updated successfully!")
            return redirect("core:services")
        except Exception as e:
            messages.error(request, f"Something went wrong! {e}")
            return redirect("core:services")


class ServiceDelete(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, servid):
        try:
            service = Services.objects.get(id=servid)
            service.delete()
            messages.success(request, f"Service delete successfully!")
            return redirect("core:services")
        except Exception as e:
            messages.error(request, f"Error occured!,{e}")
            return redirect("core:services")


class ServicePrice(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, servid, townid):
        try:

            service = Services.objects.get(id=servid)
            town = Towns.objects.get(id=townid)
            price = get_object_or_404(Prices, service=service, town=town)
            context = {"price": price.amount}
            return JsonResponse(context)
        except Exception as e:
            context = {"message": f"Error occured!,{e}"}
            return JsonResponse(context)


class ApplicationsListing(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        try:
            applications = ApplicationRecords.objects.filter(user=request.user)
            if request.user.is_staff:
                applications = ApplicationRecords.objects.all()
            new = applications.filter(paymentStatus="Pending", resolution="New")
            onque = applications.filter(paymentStatus="Paid", resolution="Queued")
            closed = applications.filter(paymentStatus="Paid", resolution="Closed")
            context = {
                "new": new, "onque": onque, 
                "closed": closed
                }
            return render(request, "core/myapplications.html", context)
        except Exception as e:
            messages.error(request, f"Error occured!,{e}")
            return HttpResponse(f"Something went wrong! ,{e}")


class ApplicationDetails(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, aplid):
        application = ApplicationRecords.objects.get(id=aplid)
        profile = Profile.objects.get(user=request.user)
        companyDetails = CompanyProfile.objects.all().last()
        context = {
            "application": application,
            "companyDetails": companyDetails,
            "profile": profile,
        }
        return render(request, "core/application_details.html", context)

    def post(self, request, aplid):
        application = ApplicationRecords.objects.get(id=aplid)
        formdetails = request.POST
        if formdetails["resolution"] in ["Closed", "Queued"]:
            application.resolution = formdetails["resolution"]
            application.paymentStatus = "Paid"
            if "invoice" in request.FILES.keys():
                # upload invoice
                fs = FileSystemStorage()
                file_uploaded = request.FILES["invoice"]
                fileName = f"INVOICE_{request.user.id}_{aplid}_{file_uploaded.name}"
                fs.save(fileName, file_uploaded)
                application.invoice = fileName
            application.save()
            messages.success(request, "Application progress updated successfully!")
            return redirect("core:myapplications")
        else:
            messages.error(request, "Something went wrong!")
            return redirect("core:details", aplid=aplid)


class ApplicationsReceived(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/applicationsreceived.html")


class Pricing(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        services = Services.objects.all()
        towns = Towns.objects.all()
        prices = Prices.objects.all()
        context = {"services": services, "towns": towns, "prices": prices}
        return render(request, "core/pages/pricing.html", context)

    def post(self, request):
        formdata = request.POST
        try:
            if formdata["formid"] == "towns":
                towns = Towns(
                    county=formdata["county"],
                    town=formdata["town"],
                    municipality=formdata["municipality"],
                )
                towns.save()
                messages.success(request, "New Town added successfully")
            elif formdata["formid"] == "pricing":
                price = Prices(
                    service=Services.objects.get(id=formdata["service"]),
                    town=Towns.objects.get(id=formdata["town"]),
                    amount=formdata["amount"],
                )
                price.save()
                messages.success(request, "New Price added successfully")
            elif formdata["formid"] == "priceEdit":
                price = Prices.objects.get(id=formdata["priceid"])
                price.amount = formdata["amount"]
                price.save()
                messages.success(request, "Price updated successfully")
            elif formdata["formid"] == "priceDelete":
                price = Prices.objects.get(id=formdata["priceid"])
                price.delete()
                messages.success(request, "Price record deleted successfully")

            return redirect("core:pricing")
        except Exception as e:
            messages.error(request, f"An error occured!{e}")
            return redirect("core:pricing")


class CompanyDetails(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        company = CompanyProfile.objects.all().last()
        print(company)
        context = {"company": company}
        return render(request, "core/pages/company_details.html", context)

    def post(self, request):
        formdata = request.POST
        company_id = 1

        # Fetch or create the CompanyProfile with id=1
        company, created = CompanyProfile.objects.get_or_create(id=company_id)

        # Update the company's fields with form data
        company.name = formdata["company"]
        company.email = formdata["email"]
        company.address = formdata["address"]
        company.mobile = formdata["mobile"]
        company.accountno = formdata["accountno"]
        company.tillno = formdata["tillno"]
        company.paybill = formdata["paybill"]

        # Save the company
        company.save()

        # Set success message
        if created:
            messages.success(request, "Company details added successfully")
        else:
            messages.success(request, "Company details updated successfully")

        return redirect("core:companyProfile")
    
class PaymentUpdates(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/payment_updates.html")
    
class Notifications(LoginRequiredMixin,View):
    
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        return render(request, "core/pages/notifications.html")
