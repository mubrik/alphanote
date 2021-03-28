from django.urls import path
from .views import (NoteHomeView, UpdateNoteView,
                    DeleteNoteView, JavaScriptUpdateNote,
                    SearchResultView, JavaScriptViewNote)

urlpatterns = [
    path('', NoteHomeView.as_view(), name='note_home'),
    path('search/', SearchResultView.as_view(), name='search_results'),
    path('note/<str:pk>/', UpdateNoteView.as_view(), name='note_detail'),
    path('delete/<str:pk>/', DeleteNoteView.as_view(), name='note_delete'),
    path('update/<str:pk>/', JavaScriptUpdateNote.as_view(), name='note__notebook_update'),
    path('view/<str:pk>/', JavaScriptViewNote.as_view(), name='note_view_form'),
]