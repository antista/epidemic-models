from apps.core.forms import EpidemicForm, EpidemicVitalForm


class SISForm(EpidemicForm):
    pass


class SISVForm(EpidemicVitalForm, SISForm):
    pass
