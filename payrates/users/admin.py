from django.contrib import admin

# Register your models here.
from .models import CustomUserManager, CustomUser,Profile

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    filter_horizontal = ['groups', 'user_permissions']

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUserManager)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'county')
    list_filter = ('role', 'county')
