from django.contrib import admin
from .models import UserProfile, Film


admin.site.register(Film)
admin.site.register(UserProfile)