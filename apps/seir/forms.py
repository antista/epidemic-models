from apps.core.forms import EpidemicForm, CoefficientField


class SEIRForm(EpidemicForm):
    # mu = CoefficientField(
    #     label='μ',
    #     help_text='Mortality coefficient (mu)',
    # )
    alpha = CoefficientField(
        label='α',
        help_text='Incubation period coefficient (alpha)',
    )
