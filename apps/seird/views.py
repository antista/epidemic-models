from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.seird.diffs import get_dots
from apps.seird.forms import SEIRDForm

DEFAULT_FORM = SEIRDForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'alpha': constants.DEFAULT_ALPHA,
    'mu': constants.DEFAULT_MU,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SEIRDView(EpidemicModelView):
    template_name = 'seird.html'
    form_class = SEIRDForm
    success_url = reverse_lazy('seird:plot')
    default_form = DEFAULT_FORM
    model_name = 'SEIRD'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_E, y_I, y_R, y_D = get_dots(form)
        return render(
            request,
            self.template_name,
            self.get_context_dict(
                form,
                y_S=y_S,
                y_E=y_E,
                y_I=y_I,
                y_R=y_R,
                y_D=y_D,
            ),
        )


class SEIRDVView(SEIRDView):
    success_url = reverse_lazy('seird:vital')
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_E, y_I, y_R, y_D = get_dots(form, True)
        return render(
            request,
            self.template_name,
            self.get_context_dict(
                form,
                y_S=y_S,
                y_E=y_E,
                y_I=y_I,
                y_R=y_R,
                y_D=y_D,
            ),
        )
