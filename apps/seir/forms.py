from apps.core.forms import EpidemicForm, CoefficientField


class SEIRForm(EpidemicForm):
    alpha = CoefficientField(
        label='α',
        help_text='Коэффициент инкубационного периода (alpha)',
    )
    field_order = ['N', 'days', 'beta', 'gamma', 'alpha', 'birth', 'death']
