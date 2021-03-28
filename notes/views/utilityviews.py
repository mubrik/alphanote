from django.views.generic import (ListView, )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from notes.models import Note
from notes.forms import CreateNoteForm
from notebooks.models import NoteBook
from notebooks.forms import CreateNoteBookForm


class SearchResultView(LoginRequiredMixin, ListView):

    model = Note
    template_name = 'notes/search_view.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('search_bar')
        object_list = Note.objects.filter(created_by=self.request.user).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        self.extra_context = {
            'notebooks': NoteBook.objects.filter(created_by=self.request.user).filter(name__icontains=query)}
        return object_list
    
    def get_context_data(self, **kwargs):
        """Insert the list object into the context dict, also inserts note creation form into context"""
        context = super().get_context_data(**kwargs)
        context.update({'form': CreateNoteForm(self.request.user), 'form1': CreateNoteBookForm(),})
        return context