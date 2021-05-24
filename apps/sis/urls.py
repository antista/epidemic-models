from django.urls import path

from apps.sis.views import SISView, SISVView

urlpatterns = [
    path('', SISView.as_view(), name='plot'),
    path('vital', SISVView.as_view(), name='vital'),
]
