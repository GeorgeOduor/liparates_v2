from django.contrib import admin

from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'county', 'town', 'municipality', 'created', 'updated')
    search_fields = ('user', 'phone', 'county', 'town', 'municipality')	
    list_filter = ('created', 'updated')


admin.site.register(Profile, ProfileAdmin)