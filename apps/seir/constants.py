from apps.seir.forms import SEIRForm

DEFAULT_FORM = SEIRForm({'N': 10000, 'days': 100, 'beta': 0.1, 'gamma': 0.2})
# Initialize cleaned_data field of DEFAULT_FORM to use it in templates.
DEFAULT_FORM.is_valid()

CONTEXT = {'model_name': 'SEIR'}


def get_context_data(model_name, form):
    return {**form.cleaned_data, 'model_name': model_name, 'form': form}
