from django.urls import reverse_lazy

from apps.core.views import EpidemicModelView
from apps.seir.forms import SEIRForm


class SIRView(EpidemicModelView):
    template_name = 'sir.html'
    form_class = SEIRForm
    success_url = reverse_lazy('sir:plot')
    default_form = SEIRForm(
        {'N': 10000, 'days': 100, 'beta': 0.1, 'gamma': 0.2}
    )
    model_name = 'SIR'
