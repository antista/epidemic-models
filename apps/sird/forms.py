from apps.core.forms import EpidemicForm, CoefficientField


class SIRDForm(EpidemicForm):
    mu = CoefficientField(
        label='μ',
        help_text='Mortality coefficient (mu)',
    )
