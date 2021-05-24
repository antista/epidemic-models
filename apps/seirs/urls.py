from django.urls import path

from apps.seirs.views import SEIRSView, SEIRSVView

urlpatterns = [
    path('', SEIRSView.as_view(), name='plot'),
    path('vital', SEIRSVView.as_view(), name='vital'),
]
