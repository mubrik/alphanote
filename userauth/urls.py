from django.urls import path, include
from .views import LoginHandler, AjaxPasswordChangeView, AjaxPasswordResetView, PasswordChangeHandler

urlpatterns = [
    path('login/', LoginHandler.as_view(), name='account_login'),
    path('password/change/', PasswordChangeHandler.as_view(), name='account_change_password'),
    path('password/change/ajax', AjaxPasswordChangeView.as_view(), name='ajax_password_change'),
    path('password/reset/ajax', AjaxPasswordResetView.as_view(), name='ajax_password_reset'),
]