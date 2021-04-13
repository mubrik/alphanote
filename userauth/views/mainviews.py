from allauth.account.views import (
    LoginView, SignupView,
    PasswordResetView, PasswordChangeView,
    EmailView, LogoutView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

# get the default user for the project/app
UserModel = get_user_model()


class LoginHandler(LoginView):
    template_name = 'account/login.html'


class LogoutHandler(LogoutView):
    template_name = 'account/logout.html'


class SignupHandler(SignupView):
    template_name = 'account/signup.html'


class PasswordChangeHandler(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change.html'


class EmailAccountHandler(LoginRequiredMixin, EmailView):
    template_name = 'account/email.html'


class PasswordResetHandler(PasswordResetView):
    template_name = 'account/password_reset.html'


class AjaxPasswordResetView(LoginRequiredMixin, PasswordResetView):

    template_name = 'userauth/password_reset_ajax.html'
    success_url = reverse_lazy("profile_detail")


class PasswordChangeHandler(LoginRequiredMixin, PasswordChangeView):
    """ subclass to add more contect to view """

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        user = UserModel.objects.get(username=self.request.user.username)
        ret['note_count'] = user.created_notes.count()
        ret['notebook_count'] = user.created_notebooks.count()
        return ret
