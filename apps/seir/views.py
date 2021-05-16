from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.seir.diffs import get_dots
from apps.seir.forms import SEIRForm

DEFAULT_FORM = SEIRForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    # 'mu': constants.DEFAULT_MU,
    'alpha': constants.DEFAULT_ALPHA,
})


class SEIRView(EpidemicModelView):
    template_name = 'seir.html'
    form_class = SEIRForm
    success_url = reverse_lazy('seir:plot')
    default_form = DEFAULT_FORM
    model_name = 'SEIR'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_E = get_dots(form)
        # y_S = [list(a) for a in zip(range(form.days), y_S)]
        # y_I = [list(a) for a in zip(range(form.days), y_I)]
        # y_R = [list(a) for a in zip(range(form.days), y_R)]
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_E=y_E),
        )
