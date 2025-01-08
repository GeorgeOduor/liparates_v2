from django.contrib import admin
from .models import (
    Service,
    Property,
    Application,
    ApplicationService,
    Payment,
    PaymentService,
    Invoice,
    CompanyProfile,
)


# Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "base_fee")
    search_fields = ("name",)


# Property Admin
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "lr_number",
        "county",
        "town",
        "property_type",
        "title_type",
        "client",
    )
    search_fields = ("lr_number", "county", "town", "client__username")
    list_filter = ("county", "town", "property_type", "title_type")


# Application Admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "property", "status", "submission_date")
    list_filter = ("status", "submission_date")
    search_fields = ("client__username", "property__property_number", "id")


# ApplicationService Admin
@admin.register(ApplicationService)
class ApplicationServiceAdmin(admin.ModelAdmin):
    list_display = ("application", "service", "quantity", "requested_at")
    list_filter = ("requested_at",)
    search_fields = ("application__id", "service__name")


# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "mpesa_transaction_id",
        "application",
        "total_amount_paid",
        "payment_date",
        "payment_status",
    )
    list_filter = ("payment_status", "payment_date")
    search_fields = ("mpesa_transaction_id", "application__id")


# PaymentService Admin
@admin.register(PaymentService)
class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ("payment", "application_service", "amount_paid")
    search_fields = (
        "payment__mpesa_transaction_id",
        "application_service__service__name",
    )


# Invoice Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("application", "issued_date")
    search_fields = ("application__id",)
    list_filter = ("issued_date",)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "email",
        "mpesa_paybill",
        "mpesa_till",
        "updated_at",
    )
    search_fields = ("name", "phone_number", "email")
