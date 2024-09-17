from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
# Local imports
from authors.forms import RegisterAuthorForm, ModifyAuthorForm, AuthorProfilePictureForm
from authors.models import Author


class RegisterAuthorView(SuccessMessageMixin, CreateView):
    model = Author
    form_class = RegisterAuthorForm
    template_name = 'authors/register.html'
    success_url = reverse_lazy('authors:login')
    success_message = "Ya puedes ingresar con tus credenciales"
    
    
class AuthorInformationView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Author
    form_class = ModifyAuthorForm
    template_name = 'authors/author_update_form.html'
    login_url = reverse_lazy('authors:login')
    success_url = reverse_lazy('common:alert')
    success_message = "La información del autor ha sido actualizada correctamente"
    
    
    def get_object(self):
        return self.request.user.author
    
    def test_func(self) -> bool:
        return self.get_object().user == self.request.user
    

class UpdateAuthorProfilePictureView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Author
    form_class = AuthorProfilePictureForm
    template_name = 'authors/snippets/author_profile_picture.html'
    login_url = reverse_lazy('authors:login')
    success_url = reverse_lazy('authors:update-profile-picture')
    
    
    def get_object(self):
        return self.request.user.author
    
    def test_func(self) -> bool:
        return self.get_object().user == self.request.user