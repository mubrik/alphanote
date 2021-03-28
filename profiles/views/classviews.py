from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from profiles.forms import UpdateProfileForm
from profiles.models import BaseProfile

# get the default user for the project/app
UserModel = get_user_model()



class ProfileUpdate(LoginRequiredMixin, UpdateView):
    # login required for obvious use, user passes test for test_func SECURITY

    login_url = reverse_lazy('account_login')
    template_name = 'profiles/profile_detail.html'
    model = BaseProfile
    form_class = UpdateProfileForm

    def get_object(self, queryset=None):
        pk = self.request.user.id
        obj = BaseProfile.objects.get(user_id=pk) 
        return obj
    
    def get_context_data(self, **kwargs):
        """Insert the single object and notes into the context dict."""
        data = super().get_context_data(**kwargs)
        user = UserModel.objects.get(username=self.request.user.username)
        data['note_count'] = user.created_notes.count()
        data['notebook_count'] = user.created_notebooks.count()
        return data
