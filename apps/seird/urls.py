from django.urls import path

from apps.seird.views import SEIRDView, SEIRDVView

urlpatterns = [
    path('', SEIRDView.as_view(), name='plot'),
    path('vital', SEIRDVView.as_view(), name='vital'),
]
