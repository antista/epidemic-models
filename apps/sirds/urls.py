from django.urls import path

from apps.sirds.views import SIRDSView, SIRDSVView

urlpatterns = [
    path('', SIRDSView.as_view(), name='plot'),
    path('vital', SIRDSVView.as_view(), name='vital'),
]
