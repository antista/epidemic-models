from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.sirds.diffs import get_dots
from apps.sirds.forms import SIRDSForm

DEFAULT_FORM = SIRDSForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'mu': constants.DEFAULT_MU,
    'ksi': constants.DEFAULT_KSI,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SIRDSView(EpidemicModelView):
    template_name = 'models/sird.html'
    form_class = SIRDSForm
    success_url = reverse_lazy('sirds:plot')
    default_form = DEFAULT_FORM
    model_name = 'SIRDS'
    about = 'about/sirds.html'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_D = self._prepare_plot_data(form.days, get_dots(form))
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_D=y_D),
        )


class SIRDSVView(SIRDSView):
    success_url = reverse_lazy('sirds:vital')
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_D = self._prepare_plot_data(
            form.days,
            get_dots(form, True),
        )
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_D=y_D),
        )
