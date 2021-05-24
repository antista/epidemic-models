from apps.core.forms import EpidemicForm, CoefficientField, EpidemicVitalForm


class SEIRSForm(EpidemicForm):
    alpha = CoefficientField(
        label='α',
        help_text='Коэффициент инкубационного периода (alpha)',
    )
    ksi = CoefficientField(
        label='ksi',
        help_text='Коэффициент инкубационного периода (ksi)',
    )


class SEIRSVForm(EpidemicVitalForm, SEIRSForm):
    pass
