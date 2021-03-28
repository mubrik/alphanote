from profiles.models import BaseProfile
from django import forms

class CustomFileField(forms.ClearableFileInput):
    template_name = 'profiles/clearable_file_input.html'

class UpdateProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = BaseProfile
        widgets = {'birth_date': forms.SelectDateWidget(years=list(range(1960, 2015))), 'profile_picture': CustomFileField()}
        fields = ['birth_date', 'profile_picture', ]