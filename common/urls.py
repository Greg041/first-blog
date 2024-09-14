# Django imports
from django.urls import path
# Local imports
## Views
from common import views


app_name='common'
urlpatterns = [
    path('alert-message/', views.AlertMessageView.as_view(), name='alert')
]
