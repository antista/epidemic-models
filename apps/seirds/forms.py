from apps.core import forms as f


class SEIRDSForm(
    f.VitalForm,
    f.KsiForm,
    f.MuForm,
    f.AlphaForm,
    f.GammaForm,
    f.BetaForm,
):
    pass
