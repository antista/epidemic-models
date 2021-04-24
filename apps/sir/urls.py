from django.urls import path

from apps.sir.views import SIRView

urlpatterns = [
    path('', SIRView.as_view(), name='plot'),
]
