from apps.core.forms import EpidemicForm, CoefficientField, EpidemicVitalForm


class SIRDForm(EpidemicForm):
    mu = CoefficientField(
        label='μ',
        help_text='Коэффициент смертности (mu)',
    )


class SIRDVForm(EpidemicVitalForm, SIRDForm):
    pass
