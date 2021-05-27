from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.sirs.diffs import get_dots
from apps.sirs.forms import SIRSForm

DEFAULT_FORM = SIRSForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'ksi': constants.DEFAULT_KSI,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SIRSView(EpidemicModelView):
    template_name = 'sirs.html'
    form_class = SIRSForm
    success_url = reverse_lazy('sirs:plot')
    default_form = DEFAULT_FORM
    model_name = 'SIRS'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R = get_dots(form)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R),
        )


class SIRSVView(SIRSView):
    success_url = reverse_lazy('sirs:vital')
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R = get_dots(form, True)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R),
        )
