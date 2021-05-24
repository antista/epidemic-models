from django.urls import path

from apps.sird.views import SIRDView, SIRDVView

urlpatterns = [
    path('', SIRDView.as_view(), name='plot'),
    path('vital', SIRDVView.as_view(), name='vital'),
]
