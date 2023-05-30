



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

from .models import *
from django.contrib.auth.forms import UserCreationForm

class CustomAdminForm(UserCreationForm):
    class Meta:
        fields='__all__'
    

class CustomUserAdmin(ModelAdmin):
    # Add the email field to the UserAdmin fieldsets
    list_display=['username','email']
    form=CustomAdminForm
    

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Destination)
admin.site.register(Package)
admin.site.register(Order)

    