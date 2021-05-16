from decimal import Decimal

from django import forms

FIELDS = {
    'N': forms.IntegerField(
        label='Population',
        help_text='Number of population',
        min_value=100,
        max_value=8000000000,
        widget=forms.NumberInput(attrs={'step': 100}),
    ),
    'days': forms.IntegerField(
        label='Days',
        help_text='Number of days to model',
        min_value=10,
        max_value=500,
        widget=forms.NumberInput(attrs={'step': 1}),
    ),
    'beta': forms.DecimalField(
        label='β',
        help_text='Spreading coefficient (beta)',
        min_value=0,
        max_value=1,
        decimal_places=3,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': 0.005}),
    ),
    'gamma': forms.DecimalField(
        label='γ',
        help_text='Healing coefficient (gamma)',
        min_value=0,
        max_value=1,
        decimal_places=3,
        widget=forms.NumberInput(
            attrs={'a': 1, 'type': 'range', 'step': 0.005}),
    )
}


class CoefficientField(forms.DecimalField):
    def __init__(self, **kwargs):
        super().__init__(
            min_value=0,
            max_value=1,
            decimal_places=3,
            widget=forms.NumberInput(attrs={'type': 'range', 'step': 0.005}),
            **kwargs
        )


class EpidemicForm(forms.Form):
    N = forms.IntegerField(
        label='Population',
        help_text='Number of population',
        min_value=100,
        max_value=8000000000,
        widget=forms.NumberInput(attrs={'step': 100}),
    )
    days = forms.IntegerField(
        label='Days',
        help_text='Number of days to model',
        min_value=10,
        max_value=500,
        widget=forms.NumberInput(attrs={'step': 1}),
    )
    beta = CoefficientField(
        label='β',
        help_text='Spreading coefficient (beta)',
    )
    gamma = CoefficientField(
        label='γ',
        help_text='Recovery coefficient (gamma)',
    )

    def get_prepared_form(self):
        self.is_valid()
        for f_n, f_v in self.cleaned_data.items():
            if type(f_v) == Decimal:
                f_v = float(f_v)
            self.__setattr__(f_n, f_v)
