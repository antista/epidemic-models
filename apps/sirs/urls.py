from django.urls import path

from apps.sirs.views import SIRSView, SIRSVView

urlpatterns = [
    path('', SIRSView.as_view(), name='plot'),
    path('vital', SIRSVView.as_view(), name='vital'),
]
