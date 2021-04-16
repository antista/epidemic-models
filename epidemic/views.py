from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"


class SIRView(TemplateView):
    template_name = "sir.html"


class SEIRView(TemplateView):
    template_name = "seir.html"
