from django.urls import path
from django.views.generic.base import RedirectView
from .views import (CreateNotebookHandler,
                    NotebookHomeView, NotebookDetailView,
                    DeleteNotebookView)


urlpatterns = [
    path('', NotebookHomeView.as_view(), name='notebook_home'),
    path('notebook/<str:pk>/', NotebookDetailView.as_view(), name='notebook_detail'),
    path('delete/<str:pk>/', DeleteNotebookView.as_view(), name='notebook_delete'),
    path('new/', CreateNotebookHandler.as_view(), name='notebook_new'),
]