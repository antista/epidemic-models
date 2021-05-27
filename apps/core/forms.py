from decimal import Decimal

from django import forms


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
        label='Популяция',
        help_text='Число людей в популяции',
        min_value=100,
        max_value=8000000000,
        widget=forms.NumberInput(attrs={'step': 100}),
    )
    days = forms.IntegerField(
        label='Дни',
        help_text='Количество дней для моделирования',
        min_value=10,
        max_value=5000,
        widget=forms.NumberInput(attrs={'step': 1}),
    )

    def get_prepared_form(self):
        self.is_valid()
        for f_n, f_v in self.cleaned_data.items():
            if type(f_v) == Decimal:
                f_v = float(f_v)
            self.__setattr__(f_n, f_v)


class VitalForm(EpidemicForm):
    birth = CoefficientField(
        label='Рождаемость',
        help_text='Коэффициент рождаемости популяции, умноженный на 100',
    )
    death = CoefficientField(
        label='Смертность',
        help_text='Коэффициент смертности популяции, умноженный на 100',
    )


class BetaForm(EpidemicForm):
    beta = CoefficientField(
        label='β',
        help_text='Коэффициент интенсивности контактов',
    )


class GammaForm(EpidemicForm):
    gamma = CoefficientField(
        label='γ',
        help_text='Коэффициент выздоровления',
    )
    basic_reproduction_number = forms.DecimalField(
        label='R0',
        help_text='Базовое репродуктивное число (β/γ)',
        widget=forms.NumberInput(attrs={'readonly': True}),
    )


class KsiForm(EpidemicForm):
    ksi = CoefficientField(
        label='ξ',
        help_text='Скорость потери иммунитета',
    )


class AlphaForm(EpidemicForm):
    alpha = CoefficientField(
        label='α',
        help_text='Коэффициент инкубационного периода',
    )


class MuForm(EpidemicForm):
    mu = CoefficientField(
        label='μ',
        help_text='Коэффициент смертности',
    )
