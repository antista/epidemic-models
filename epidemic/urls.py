from django.urls import path
from epidemic.views import AboutView, SEIRView, SIRView

urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('sir/', SIRView.as_view(), name='sir'),
    path('seir/', SEIRView.as_view(), name='seir'),
]
