from django.urls import path
from . import views


app_name="blog"
urlpatterns = [
    path('', views.BlogRedirectView.as_view(), name="home"),
    path('posts/', views.IndexView.as_view(), name="home"),
    path('add-post/', views.AddPostView.as_view(), name="add_post_view"),
    path('success/', views.SuccessView.as_view(), name="succes_view"),
    path('posts/<uuid:pk>', views.SinglePostView.as_view(), name="single_post"),
]