from apps.core.forms import EpidemicForm, CoefficientField


class SEIRDForm(EpidemicForm):
    alpha = CoefficientField(
        label='α',
        help_text='Коэффициент инкубационного периода (alpha)',
    )
    mu = CoefficientField(
        label='μ',
        help_text='Коэффициент смертности (mu)',
    )
    field_order = [
        'N',
        'days',
        'beta',
        'gamma',
        'alpha',
        'mu',
        'birth',
        'death',
    ]
