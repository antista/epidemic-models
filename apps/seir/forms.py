from django import forms


class SEIRForm(forms.Form):
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
        widget=forms.NumberInput(attrs={'step': 10}),
    )
    beta = forms.DecimalField(
        label='beta',
        help_text='Spreading coefficient',
        min_value=0,
        max_value=1,
        decimal_places=3,
        widget=forms.NumberInput(attrs={'step': 0.005}),
    )
    gamma = forms.DecimalField(
        label='gamma',
        help_text='Healing coefficient',
        min_value=0,
        max_value=1,
        decimal_places=3,
        widget=forms.NumberInput(attrs={'step': 0.005}),
    )
