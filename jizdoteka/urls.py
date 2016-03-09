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
from apps.web.views import journey, index, user, car

urlpatterns = [
    ## Zaklady
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),

    ## Nutne pro prihlasen
    url(r'^login_screen/$', user.LoginScreen.as_view(), name="login_screen"),
    url(r'^logout_user/$', user.logout_user, name="logout_user"),
    url(r'^register/$', user.RegisterScreen.as_view(), name="register"),

    ## Jizdy
    url(r'^journey/$', journey.JourneyList.as_view(), name='journey'),
    url(r'^journey/new/$', journey.JourneyCreate.as_view(), name='journey_new'),
    url(r'^journey/update/(?P<pk>[0-9]+)$', journey.JourneyUpdate.as_view(), name='journey_update'),
    url(r'^journey/(?P<pk>[0-9]+)$', journey.JourneyDetail.as_view(), name='journey_detail'),

    ## Managing
    url(r'^user/$', user.User.as_view(), name="user"),
    url(r'^cars/$', car.Car.as_view(), name="cars"),

]
