from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView


class AboutView(TemplateView):
    template_name = "about.html"


class EpidemicModelView(FormView):
    """Base view to views for plot epidemic models."""

    default_form = None
    model_name = None

    def __init__(self, **kwargs):
        """Check default_form is in class attributes."""
        cls = type(self)
        if not getattr(cls, 'model_name', None):
            raise ValueError(
                'No model name to show. Provide a model_name.'
            )
        if not getattr(cls, 'default_form', None):
            raise ValueError(
                'No default form to show. Provide a default_form.'
            )
        # Initialize cleaned_data field of default_form to use it in templates.
        self.default_form.is_valid()
        super().__init__(**kwargs)

    def get_context_dict(self, form):
        """Return context dict for view."""
        return {
            **form.cleaned_data,
            'model_name': self.model_name,
            'form': form,
        }

    def get(self, request, **kwargs):
        """Fill initial form and add values to template."""
        return render(
            request,
            self.template_name,
            self.get_context_dict(self.default_form),
        )

    def post(self, request, **kwargs):
        """Fill form and add values to template."""
        form = self.form_class(request.POST)
        if form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context_dict(form),
            )
        return redirect(request.path)
