# Django imports
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, BaseFormView
from django.views.generic.detail import DetailView
# Local imports
## Model imports
from authors.models import Author
from blog.models import Post
## Forms
from blog.form import CommentForm, AddPostForm
# Third Party imports
from datetime import datetime
from typing import Any 


class BlogRedirectView(RedirectView):
    url = reverse_lazy("blog:home")


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = "-date"
    paginate_by = 2
    
    def get_queryset(self) -> QuerySet[Any]:
        posts = super().get_queryset()
        if self.request.GET.get("category"):
            posts = posts.filter(category__name__iexact=self.request.GET.get("category"))
        if "search_terms" in self.request.POST:
            search_terms = self.request.POST.get("search_terms")
            posts = Post.objects.filter(title__icontains=search_terms).order_by("-date")
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_params'] = self.request.GET.copy()
        return context
    
    def post(self, request, **kwargs):
        self.object_list = self.get_queryset()
        if "search_terms" in self.request.POST:
            self.object_list = Post.objects.filter(
                title__icontains=self.request.POST.get("search_terms")
            ).order_by("-date")
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data()
        return self.render_to_response(context)
        
    

class AddPostView(LoginRequiredMixin, FormView):
    template_name = "blog/add_post.html"
    form_class = AddPostForm
    success_url = reverse_lazy("blog:succes_view")
    login_url = reverse_lazy("authors:login")

    def form_valid(self, form):
        post_object = form.save(commit=False)
        author = self.get_logged_author()
        post_object.author = author
        post_object.date = datetime.now()
        post_object.save()
        post_object.category.add(*form.cleaned_data["category"])
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)    
    
    def get_logged_author(self):
        if self.request.user.is_authenticated:
            return Author.objects.get(user=self.request.user)
        

class SinglePostView(SuccessMessageMixin, DetailView, BaseFormView):
    template_name = "blog/single_post.html"
    form_class = CommentForm
    model = Post
    queryset = Post.objects.all()
    success_message = "Tu comentario ha sido publicado exitosamente"
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comments"] = self.get_object().comment_set.all()
        return context
    
    def form_valid(self, form):
        new_commentary = form.save(commit=False)
        new_commentary.post = self.get_object()
        new_commentary.save()
        return super().form_valid(form)
    
    
    def get_success_url(self):
        return reverse_lazy("blog:single_post", kwargs={"pk": self.get_object().pk})


class SuccessView(TemplateView):
    template_name = "blog/success.html"