from django.views.generic import TemplateView
from allauth.account.views import (LoginView, PasswordChangeView,
                                   PasswordResetView, PasswordChangeView)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

# get the default user for the project/app
UserModel = get_user_model()


class LoginHandler(LoginView):

    pass


class AjaxPasswordChangeView(PasswordChangeView):

    template_name = 'userauth/password_change_ajax.html'
    success_url = reverse_lazy("profile_detail")


class AjaxPasswordResetView(PasswordResetView):

    template_name = 'userauth/password_reset_ajax.html'
    success_url = reverse_lazy("profile_detail")

class PasswordChangeHandler(PasswordChangeView):
    """ subclass to add more contect to view """

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user = UserModel.objects.get(username=self.request.user.username)
        ret['note_count'] = user.created_notes.count()
        ret['notebook_count'] = user.created_notebooks.count()
        return ret