from django.urls import path

from apps.seirds.views import SEIRDSView, SEIRDSVView

urlpatterns = [
    path('', SEIRDSView.as_view(), name='plot'),
    path('vital', SEIRDSVView.as_view(), name='vital'),
]
