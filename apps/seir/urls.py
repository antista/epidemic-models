from django.urls import path

from apps.seir.views import SEIRView, SEIRVView

urlpatterns = [
    path('', SEIRView.as_view(), name='plot'),
    path('vital', SEIRVView.as_view(), name='vital'),
]
