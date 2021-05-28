from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.sir.diffs import get_dots
from apps.sir.forms import SIRForm

DEFAULT_FORM = SIRForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SIRView(EpidemicModelView):
    template_name = 'models/sir.html'
    form_class = SIRForm
    success_url = reverse_lazy('sir:plot')
    default_form = DEFAULT_FORM
    model_name = 'SIR'
    about = 'about/sir.html'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R = self._prepare_plot_data(form.days, get_dots(form))
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R),
        )


class SIRVView(SIRView):
    success_url = reverse_lazy('sir:vital')
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R = self._prepare_plot_data(
            form.days,
            get_dots(form, True),
        )
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R),
        )
