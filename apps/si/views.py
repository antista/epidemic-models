from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.si.diffs import get_dots
from apps.si.forms import SIForm

DEFAULT_FORM = SIForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SIView(EpidemicModelView):
    template_name = 'si.html'
    form_class = SIForm
    success_url = reverse_lazy('si:plot')
    default_form = DEFAULT_FORM
    model_name = 'SI'
    about = 'fbvehbvishe'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I = get_dots(form)
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I),
        )


class SIVView(SIView):
    success_url = reverse_lazy('si:vital')
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
