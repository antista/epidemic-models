from django.shortcuts import render
from django.urls import reverse_lazy

from apps.core import constants
from apps.core.views import EpidemicModelView
from apps.seirs.diffs import get_dots
from apps.seirs.forms import SEIRSForm

DEFAULT_FORM = SEIRSForm({
    'N': constants.DEFAULT_POPULATION,
    'days': constants.DEFAULT_DAYS,
    'beta': constants.DEFAULT_BETA,
    'gamma': constants.DEFAULT_GAMMA,
    'alpha': constants.DEFAULT_ALPHA,
    'ksi': constants.DEFAULT_KSI,
    'birth': constants.DEFAULT_BIRTH,
    'death': constants.DEFAULT_DEATH,
})


class SEIRSView(EpidemicModelView):
    template_name = 'models/seir.html'
    form_class = SEIRSForm
    success_url = reverse_lazy('seirs:plot')
    default_form = DEFAULT_FORM
    model_name = 'SEIRS'
    about = 'about/seirs.html'

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_E = self._prepare_plot_data(form.days, get_dots(form))
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_E=y_E),
        )


class SEIRSVView(SEIRSView):
    success_url = reverse_lazy('seirs:plot')
    vital = True

    def _get_response_data(self, request, form):
        form.get_prepared_form()
        y_S, y_I, y_R, y_E = self._prepare_plot_data(
            form.days,
            get_dots(form, True),
        )
        return render(
            request,
            self.template_name,
            self.get_context_dict(form, y_S=y_S, y_I=y_I, y_R=y_R, y_E=y_E),
        )
