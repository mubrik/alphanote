from django.contrib import admin
from .models import NoteBook


class NoteBookAdmin(admin.ModelAdmin):

    pass

admin.site.register(NoteBook, NoteBookAdmin)