from apps.core.forms import EpidemicForm


class SIForm(EpidemicForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['gamma']


# class SIVForm(EpidemicVitalForm, SIForm):
#     pass
