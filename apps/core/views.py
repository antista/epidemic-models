from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView


class AboutView(TemplateView):
    template_name = "about.html"


class EpidemicModelView(FormView):
    """Base view to views for plot epidemic models."""

    default_form = None
    model_name = None
    about = None
    vital = False

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
        if not getattr(cls, '_get_response_data', None):
            raise ValueError(
                'No method to get response data. '
                'Provide a _get_response_data method.'
            )
        # Initialize cleaned_data field of default_form to use it in templates.
        self.default_form.is_valid()
        super().__init__(**kwargs)

    def get_context_dict(self, form, **kwargs):
        """Return context dict for view."""
        data = {
            **form.cleaned_data,
            'model_name': self.model_name,
            'about': self.about,
            'vital': self.vital,
            'form': form,
        }
        data.update(**kwargs)
        return data

    # def get(self, request, **kwargs):
    #     """Fill initial form and add values to template."""
    #     return render(
    #         request,
    #         self.template_name,
    #         self.get_context_dict(self.default_form),
    #     )

    # def post(self, request, **kwargs):
    #     """Fill form and add values to template."""
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         return render(
    #             request,
    #             self.template_name,
    #             self.get_context_dict(form),
    #         )
    #     return redirect(request.path)

    def get(self, request, **kwargs):
        """Fill initial form and add values to template."""
        super().get(request, **kwargs)
        form = self.default_form
        return self._get_response_data(request, form)

    def post(self, request, **kwargs):
        super().post(request, **kwargs)
        form = self.form_class(data=request.POST)
        return self._get_response_data(request, form)
