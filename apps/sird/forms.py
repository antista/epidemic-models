from apps.core.forms import EpidemicForm, CoefficientField


class SIRDForm(EpidemicForm):
    mu = CoefficientField(
        label='μ',
        help_text='Коэффициент смертности (mu)',
    )
    field_order = ['N', 'days', 'beta', 'gamma', 'mu', 'birth', 'death']
