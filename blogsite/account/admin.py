from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    """class representing how the model will be displayed in the admin panel"""
    list_display = ['user', 'role', 'photo']
