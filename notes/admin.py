from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Note

# Apply summernote to all TextField in model.
class SNoteAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    ''' making textfield all user summer note editor '''
    summernote_fields = ('content',)

admin.site.register(Note, SNoteAdmin)
