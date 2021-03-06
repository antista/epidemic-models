from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.sird.diffs import get_dots
from apps.sird.forms import SIRDForm

DEFAULT_FORM = SIRDForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'mu': constants.DEFAULT_MU,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SIRDView(EpidemicModelView):
    template_name = 'models/sird.html'
    form_class = SIRDForm
    success_url = reverse_lazy('sird:plot')
    default_form = DEFAULT_FORM
    model_name = 'SIRD'
    about = 'about/sird.html'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_D = self._prepare_plot_data(form.days, get_dots(form))
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_D=y_D),
        )


class SIRDVView(SIRDView):
    success_url = reverse_lazy('sird:vital')
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
