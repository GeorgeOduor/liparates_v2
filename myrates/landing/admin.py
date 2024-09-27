from django.contrib import admin

# Register your models here.
from .models import *

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'subject', 'message',)
    search_fields = ('name', 'mobile',)
    list_filter = ('created_at',)
    
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at',)
    search_fields = ('question', 'answer',)
    list_filter = ('created_at',)
    
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)