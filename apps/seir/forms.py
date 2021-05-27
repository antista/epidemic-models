from apps.core import forms as f


class SEIRForm(
    f.VitalForm,
    f.AlphaForm,
    f.GammaForm,
    f.BetaForm,
):
    pass
