from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .form import CommentForm


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
        current_post = get_object_or_404(Post, slug=slug)
        form = CommentForm()
        context = {
            "post": current_post,
            "comment_form": form,
            "comments": current_post.comment_set.all()
        }
        return render(request, "blog/single_post.html", context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("single_post_view", slug)
        current_post = get_object_or_404(Post, slug=slug)
        context = {
            "post": current_post,
            "comment_form": form,
            "comments": current_post.comment_set.all()
        }
        return render(request, "blog/single_post.html", context)
