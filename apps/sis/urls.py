from django.urls import path

from apps.sis.views import SISView

urlpatterns = [
    path('', SISView.as_view(), name='plot'),
]
