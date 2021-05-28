"""epidemic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.core.urls', 'core'))),
    path('sir/', include(('apps.sir.urls', 'sir'))),
    path('sirs/', include(('apps.sirs.urls', 'sirs'))),
    path('seir/', include(('apps.seir.urls', 'seir'))),
    path('seirs/', include(('apps.seirs.urls', 'seirs'))),
    path('si/', include(('apps.si.urls', 'si'))),
    path('sis/', include(('apps.sis.urls', 'sis'))),
    path('sird/', include(('apps.sird.urls', 'sird'))),
    path('sirds/', include(('apps.sirds.urls', 'sirds'))),
    path('seird/', include(('apps.seird.urls', 'seird'))),
    path('seirds/', include(('apps.seirds.urls', 'seirds'))),
]
