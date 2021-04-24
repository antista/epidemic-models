from django.urls import path

from apps.seir.views import SEIRView

urlpatterns = [
    path('', SEIRView.as_view(), name='plot'),
]
