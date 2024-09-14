# Django imports
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin


"""
    This view is dedicated exclusively to return the alert_container
    template for htmx calls that need a alert response
"""
class AlertMessageView(SuccessMessageMixin, TemplateView):
    template_name = 'common/snippets/alert_container.html'
