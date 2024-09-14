# Django imports
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
# Local imports
from authors import views
from authors.forms import AuthorAuthenticationForm


app_name='authors'
urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='authors/login.html', 
        authentication_form=AuthorAuthenticationForm, 
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterAuthorView.as_view(), name='register'),
    path('profile/', views.AuthorInformationView.as_view(), name='profile'),
    path('update-profile-picture/', views.UpdateAuthorProfilePictureView.as_view(), name='update-profile-picture'),
]
