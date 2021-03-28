from django.http import request
from django.views.generic import (ListView, UpdateView,
                                  FormView, DeleteView,
                                  DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from notes.forms import CreateNoteForm, CustomNotebookForm
from notes.models import Note
from notebooks.forms import CreateNoteBookForm


class NoteHomeHandler(ListView):

    '''  list of notes and form to create note '''

    template_name = 'notes/note_home.html'
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        """Insert the list object into the context dict, also inserts note creation form into context"""

        context = super().get_context_data(**kwargs)
        context.update({'form': CreateNoteForm(self.request.user,), 'form1': CreateNoteBookForm(),})
        return context

    def get_queryset(self):
        ''' filtered initial queryset so a logged in user can only access their  created notes
            anonymous users cant access view so no worries about that
        '''

        queryset = Note.objects.filter(created_by=self.request.user)
        return queryset


class CreateNoteHandler(FormView):
    ''' processes the post form from listview, adds creator as request user '''

    form_class = CreateNoteForm
    success_url = reverse_lazy('note_home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        if self.object.content :
            print(f'content {self.object.content}')
            self.object.created_by = self.request.user
            self.object = form.save()
            return super().form_valid(form)
        else:
            print(f'note content empty?: {self.object.content}')
            messages.add_message(self.request, messages.INFO, 'Empty Note Deleted')
            return super().form_valid(form)

class NoteHomeView(LoginRequiredMixin, View):

    ''' handles views for note home and posting a new note form
        both action requires login
    '''

    permission_denied_message = 'You need to login'

    def get(self, request, *args, **kwargs):
        view = NoteHomeHandler.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateNoteHandler.as_view()
        return view(request, *args, **kwargs)


class UpdateNoteView(LoginRequiredMixin, UpdateView):
    ''' handles form updates, queryset filtered by request user '''

    template_name = 'notes/note_detail.html'
    success_url = reverse_lazy('note_home')

    def get_queryset(self):
        queryset = Note.objects.filter(created_by=self.request.user)
        return queryset

    def get_form(self):
        return CreateNoteForm(self.request.user, **self.get_form_kwargs())


class DeleteNoteView(LoginRequiredMixin, DeleteView):
    ''' handles form deletion, needs more security '''

    template_name = 'notes/note_delete.html'
    success_url = reverse_lazy('note_home')

    def get_queryset(self):
        ''' filtered initial queryset so a logged in user can only access their  created notes
            anonymous users cant access view so no worries about that
        '''

        queryset = Note.objects.filter(created_by=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class JavaScriptUpdateNote(UpdateView):

    template_name = 'notes/note_update_notebook.html'
    success_url = reverse_lazy('note_home')

    def get_form(self):
        return CustomNotebookForm(user=self.request.user, **self.get_form_kwargs())

    def get_queryset(self):
        queryset = Note.objects.filter(created_by=self.request.user)
        return queryset

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)


class JavaScriptViewNote(UpdateView):
    
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_home')

    def get_form(self):
        return CreateNoteForm(user=self.request.user, **self.get_form_kwargs(), auto_id='field_%s',)

    def get_queryset(self):
        queryset = Note.objects.filter(created_by=self.request.user)
        return queryset

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)