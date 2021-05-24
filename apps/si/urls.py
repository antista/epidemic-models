from django.urls import path

from apps.si.views import SIView, SIVView

urlpatterns = [
    path('', SIView.as_view(), name='plot'),
    path('vital', SIVView.as_view(), name='vital'),
]
