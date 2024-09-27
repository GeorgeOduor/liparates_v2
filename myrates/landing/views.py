from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from core.models import Services, CompanyProfile
from .models import FAQ, ContactMessage

# Create your views here.


class HomeView(View):

    def get(self, request):
        # print(contacts.values())
        company_profiles_dict = [
            {
                "email": profile.email,
                "mobile": profile.mobile,
                "address": profile.address,
                # Add other fields as needed
            }
            for profile in CompanyProfile.objects.all()
        ][0]
        context = {
            "services": Services.objects.all(),
            "faqs": FAQ.objects.all(),
            "contacts": company_profiles_dict,
        }
        return render(request, "landing/home.html", context)

    def post(self, request):
        # check if user is logged in and is admin
        form_data = request.POST
        # print(form_data)
        form_name = form_data["form-name"]
        if (
            request.user.is_authenticated
            and request.user.is_staff
            and form_name != "contactus"
        ):
            if form_name == "add":
                new_faq = FAQ(
                    question=form_data["question"], answer=form_data["answer"]
                )
                new_faq.save()
                return redirect("landing:home")
            elif form_name == "edit":
                # Assuming form_data is a dictionary coming from a form submission
                faq_id = form_data["faq_id"]

                # Step 1: Retrieve the existing FAQ instance
                faq = get_object_or_404(FAQ, id=faq_id)

                # Step 2: Update the fields
                faq.question = form_data["question"]  # Update question
                faq.answer = form_data["answer"]  # Update answer

                # Step 3: Save the changes
                faq.save()

                return redirect("landing:home")
            elif form_name == "delete":
                faq = FAQ.objects.get(id=form_data["faq_id"])
                faq.delete()
                return redirect("landing:home")

        if form_name == "contactus":
            contactus = ContactMessage(
                name=form_data["name"],
                mobile=form_data["mobile"],
                subject=form_data["subject"],
                message=form_data["message"],
            )
            contactus.save()
            return redirect("landing:home")



def toc(request):
    company_profiles_dict = [
            {
                "email": profile.email,
                "mobile": profile.mobile,
                "address": profile.address,
                # Add other fields as needed
            }
            for profile in CompanyProfile.objects.all()
        ][0]
    context = {
           
            "contacts": company_profiles_dict,
        }
    return render(request,"landing/toc.html",context)