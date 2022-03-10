from django.shortcuts import redirect, render
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.translation import gettext as _
from datetime import datetime
from .models import Post, Author
from .form import CommentForm, AddPostForm



# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = '-date'
    paginate_by = 2
    

class AddPostView(FormView):
    template_name = "blog/add_post.html"
    form_class = AddPostForm
    success_url = "/success/"

    def form_valid(self, form):
        post_object = form.save(commit=False)
        author, created = Author.objects.get_or_create(name=form.cleaned_data["author"])
        post_object.author = author
        post_object.date = datetime.now()
        post_object.save()
        post_object.category.add(*form.cleaned_data["category"])
        return super().form_valid(form)
        


class SinglePostView(View):
    def get(self, request, slug, pk):
        current_post = get_object_or_404(Post, id=pk)
        form = CommentForm()
        context = {
            "post": current_post,
            "comment_form": form,
            "comments": current_post.comment_set.all()
        }
        return render(request, "blog/single_post.html", context)

    def post(self, request, slug, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_commentary = form.save(commit=False)
            new_commentary.post = Post.objects.get(id=pk)
            new_commentary.save()
            return redirect("single_post_view", slug, pk)
        current_post = get_object_or_404(Post, id=pk)
        context = {
            "post": current_post,
            "comment_form": form,
            "comments": current_post.comment_set.all()
        }
        return render(request, "blog/single_post.html", context)


class SuccessView(TemplateView):
    template_name = "blog/success.html"


class CategoryPostsView(ListView):
    template_name = "blog/category-posts.html"
    paginate_by = 2
    context_object_name = "posts"

    def get(self, request, category):
        self.object_list = Post.objects.filter(category__name__iexact=category).order_by("-date")
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


class SearchView(ListView):
    template_name = "blog/category-posts.html"
    paginate_by = 2
    context_object_name = "posts"

    def post(self, request, **kwargs):
        search_terms = request.POST["search_terms"]
        self.object_list = Post.objects.filter(title__icontains=search_terms).order_by("-date")
        context = super().get_context_data(**kwargs)
        return render(request, "blog/search-page.html", context)