from django.contrib import admin

# Register your models here.
from .models import ApplicationRecords, CompanyProfile, Prices, Services

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    
class PricingAdmin(admin.ModelAdmin):
    list_display = ('service', 'town', 'amount', 'created_at', 'updated_at')
    search_fields = ('service', 'town', 'amount')
    list_filter = ('created_at', 'updated_at')
    
class ApplicationRecordsAdmin(admin.ModelAdmin):
    list_display = ('user', 'service','amount', 'paymentStatus', 'created_at', 'updated_at')
    search_fields = ('user', 'service')
    
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'mobile', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'email', 'mobile')
    list_filter = ('created_at', 'updated_at')
    

    
admin.site.register(Services, ServicesAdmin)
admin.site.register(Prices, PricingAdmin)
admin.site.register(ApplicationRecords, ApplicationRecordsAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
