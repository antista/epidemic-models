from django.urls import path

from apps.sir.views import SIRView, SIRVView

urlpatterns = [
    path('', SIRView.as_view(), name='plot'),
    path('vital', SIRVView.as_view(), name='vital'),
]
