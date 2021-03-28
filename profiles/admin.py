from django.contrib import admin
from .models import BaseProfile


class ProfileAdmin(admin.ModelAdmin):

    pass

admin.site.register(BaseProfile, ProfileAdmin)
