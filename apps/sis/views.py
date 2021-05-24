from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.sis.diffs import get_dots
from apps.sis.forms import SISForm, SISVForm

DEFAULT_FORM = SISForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
})
DEFAULT_VITAL_FORM = SISVForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SISView(EpidemicModelView):
    template_name = 'sis.html'
    form_class = SISForm
    success_url = reverse_lazy('sis:plot')
    default_form = DEFAULT_FORM
    model_name = 'SIS'
    about = 'fbvehbvishe'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I = get_dots(form)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I),
        )


class SISVView(EpidemicModelView):
    template_name = 'sis.html'
    form_class = SISVForm
    success_url = reverse_lazy('sis:vital')
    default_form = DEFAULT_VITAL_FORM
    model_name = 'SIS'
    vital = True
    about = 'fbvehbvishe'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I = get_dots(form, True)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I),
        )
