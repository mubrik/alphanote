from django.urls import path, include
from .views import (
    LoginHandler, LogoutHandler,
    AjaxPasswordResetView, PasswordChangeHandler,
    EmailAccountHandler,
    SignupHandler, PasswordResetHandler
)

urlpatterns = [
    path('login/', LoginHandler.as_view(), name='account_login'),
    path('logout/', LogoutHandler.as_view(), name='account_logout'),
    path('signup/', SignupHandler.as_view(), name='account_signup'),
    path('email/', EmailAccountHandler.as_view(), name='account_email'),
    path('password/reset/', PasswordResetHandler.as_view(),
         name='account_reset_password'),
    path('password/change/', PasswordChangeHandler.as_view(),
         name='account_change_password'),
    path('password/reset/ajax', AjaxPasswordResetView.as_view(),
         name='ajax_password_reset'),
]
