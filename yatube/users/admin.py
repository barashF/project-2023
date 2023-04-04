from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "email", "email_confirmation")

admin.site.register(Profile, ProfileAdmin)
# Register your models here.
