from apps.core.forms import EpidemicForm, EpidemicVitalForm


class SIRForm(EpidemicForm):
    pass


class SIRVForm(EpidemicVitalForm, SIRForm):
    pass
