from apps.core.forms import EpidemicForm, EpidemicVitalForm


class SIForm(EpidemicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['gamma']


class SIVForm(EpidemicVitalForm, SIForm):
    pass
