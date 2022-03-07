from django.shortcuts import redirect, render
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from datetime import date
from .models import Post, Comment, Author
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
        author = Author.objects.get_or_create(name=form.cleaned_data["author"])
        print(author)
        post_object.date = date.today()
        print(post_object.date)



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
            new_commentary = form.save(commit=False)
            new_commentary.post = Post.objects.get(slug=slug)
            new_commentary.save()
            return redirect("single_post_view", slug)
        current_post = get_object_or_404(Post, slug=slug)
        context = {
            "post": current_post,
            "comment_form": form,
            "comments": current_post.comment_set.all()
        }
        return render(request, "blog/single_post.html", context)


class SuccessView(TemplateView):
    template_name = "success.html"

