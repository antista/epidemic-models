from django.urls import reverse_lazy

from apps.core.views import EpidemicModelView
from apps.sis.forms import SISForm


class SISView(EpidemicModelView):
    template_name = 'sis.html'
    form_class = SISForm
    success_url = reverse_lazy('sis:plot')
    default_form = SISForm(
        {'N': 10000, 'days': 100, 'beta': 0.1, 'gamma': 0.2}
    )
    model_name = 'SEIR'
