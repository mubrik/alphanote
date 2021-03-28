from django.views.generic import (ListView,
                                  FormView, DeleteView,
                                  DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from notebooks.models import NoteBook
from notebooks.forms import CreateNoteBookForm
from notes.forms import CreateNoteForm


class NotebookHomeView(LoginRequiredMixin, ListView):

    '''  list of notebooks and form to create notebook '''

    template_name = 'notebooks/notebook_list.html'
    context_object_name = 'notebooks'
    permission_denied_message = 'You need to login'

    def get_context_data(self, **kwargs):
        """Insert the list object into the context dict."""
        context = super().get_context_data(**kwargs)
        context.update({'form1': CreateNoteBookForm(), 'form': CreateNoteForm(self.request.user), })
        return context

    def get_queryset(self):
        queryset = NoteBook.objects.filter(created_by=self.request.user)
        return queryset


class NotebookDetailView(LoginRequiredMixin, DetailView):
    ''' details about a notebook and list of notes 
        should filter notebook query*
        add security*
    '''

    template_name = 'notebooks/notebook_detail.html'
    model = NoteBook
    context_object_name = 'notebook'

    def get_context_data(self, **kwargs):
        """Insert the single object and notes into the context dict."""
        data = super().get_context_data(**kwargs)
        data['notes'] = self.object.notes_query()
        data['form'] = CreateNoteForm(self.request.user)
        data['form1'] = CreateNoteBookForm()
        return data

    def get_queryset(self):
        queryset = NoteBook.objects.filter(created_by=self.request.user)
        return queryset


class CreateNotebookHandler(LoginRequiredMixin, FormView):
    ''' processes the post form to create notebook, adds creator as request user
    add security*
    '''

    form_class = CreateNoteBookForm
    success_url = reverse_lazy('notebook_home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class DeleteNotebookView(LoginRequiredMixin, DeleteView):
    ''' processes the post form to delete notebook
    add security*
    '''

    template_name = 'notebooks/notebook_delete.html'
    success_url = reverse_lazy('notebook_home')

    def get_queryset(self):
        queryset = NoteBook.objects.filter(created_by=self.request.user)
        return queryset
