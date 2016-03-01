"""jizdoteka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),

    ## Nutne pro prihlaseni
    url(r'^login_screen/$', views.LoginScreen.as_view(), name="login_screen"),
    url(r'^logout_user/$', views.logout_user, name="logout_user"),
    url(r'^register/$', views.RegisterScreen.as_view(), name="register"),
    url(r'^user/$', views.UserManagement.as_view(), name="user"),

    url(r'^cars/$', views.CarManagement.as_view(), name="cars"),

    #url(r'^user_mgmt/$', views.user_mgmt, name = "user_mgmt"),


    #url(r'^(?P<pk>[0-9]+)$', views.JourneyDetail.as_view(), name='journey_detail'),

    ## Login pro facebook
    #url(r'accounts/', include('allauth.urls'))
]
