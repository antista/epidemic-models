from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.seir.diffs import get_dots
from apps.seir.forms import SEIRForm, SEIRVForm

DEFAULT_FORM = SEIRForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'alpha': constants.DEFAULT_ALPHA,
})
DEFAULT_VITAL_FORM = SEIRVForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'alpha': constants.DEFAULT_ALPHA,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
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
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_E=y_E),
        )


class SEIRVView(EpidemicModelView):
    template_name = 'seir.html'
    form_class = SEIRVForm
    success_url = reverse_lazy('seir:vital')
    default_form = DEFAULT_VITAL_FORM
    model_name = 'SEIR'
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_E = get_dots(form, True)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_E=y_E),
        )
