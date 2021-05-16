from django.urls import path

from apps.sird.views import SIRDView

urlpatterns = [
    path('', SIRDView.as_view(), name='plot'),
]
