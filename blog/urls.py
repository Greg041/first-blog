from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="index_view"),
    path('add-post', views.AddPostView.as_view(), name="add_post_view"),
    path('posts/<slug:slug>', views.SinglePostView.as_view(), name="single_post_view")
]