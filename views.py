from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from datetime import date
from .models import Post


# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = '-date'
    paginate_by = 2


class AddPostView(View):
    def get(self, request):
        return render(request, "blog/add_post.html")


class SinglePostView(View):
    def get(self, request, slug):
        return render(request, "blog/single_post.html")