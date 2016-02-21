from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, RedirectView, View
from . import models
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseRedirect

## Import forms
from . import forms

def index(request):
    return render(request, 'web/index.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('../../')

class LoginScreen(View):
    user_name = None
    user_pass = None
    login_form = forms.LoginForm()
    redirect_bool = False

    user = None

    def get(self, request):
        return render(request, 'web/login_screen.html', {"form": self.login_form})

    def post(self, request):
        self.user_name = request.POST['user_name']
        self.user_pass = request.POST['user_pass']
        self._check_credentials()

        if self.user:
            login(request, self.user)
        else:
            return HttpResponse("INVALID CREDENTIALS!")
        return HttpResponseRedirect('../../')

    def _check_credentials(self):
        if self.user_name and self.user_pass:
            self.user = authenticate(username = self.user_name, password = self.user_pass)
        else:
            return HttpResponse("MISSING CREDENTIALS!")

class RegisterScreen(View):
    user_mail = None
    user_pass = None
    register_form = forms.RegisterForm()

    correct_day = None
    asked_day = None
    question_ok = False

    request = None

    def get(self, request):
        return render(request, 'web/register.html', {"form": self.register_form})

    def post(self, request):
        self.correct_day = self.register_form.correct_day
        self.request = request

        self._post_get_details()
        self._check_security_question()
        return render(request, 'web/register.html', {"form": self.register_form})

    def _post_get_details(self):
        self.user_mail = self.request.POST['user_email']
        user_mail_confirm = self.request.POST['user_email_confirm']
        self.user_pass = self.request.POST['user_password']
        user_pass_confirm = self.request.POST['user_password_confirm']

        self.asked_day = self.request.POST['random_antibot']

    def _check_security_question(self):
        self.correct_day = self.register_form.correct_day
        if self.correct_day == self.asked_day:
            self.question_ok = True

#@login_required
#def user_mgmt(request):
#    manage_form = forms.ManageForm()
#    return render(request, 'web/user_mgmt.html', {"form": manage_form})

class JourneyList(ListView):
    model = models.Journey


class JourneyDetail(DetailView):
    model = models.Journey

    def get_context_data(self, **kwargs):
        context = super(JourneyDetail, self).get_context_data(**kwargs)
        obj = context['object']
        passangers = {}

        class Passanger(object):
            start = None
            _length = 0
            _rest = 0
            _sum = 0
            user = None

            def __init__(self, start, user, sum):
                self.start = start
                self.user = user
                self._sum = sum

            @property
            def length(self):
                return self._length

            @length.setter
            def length(self, val):
                self._length = val
                self._rest = self._sum - self.start - self._length

            @property
            def rest(self):
                return self._sum - self.start - self._length

            def __repr__(self):
                return '%s, start=%s, len=%s' % (self.user, self.start, self.length)

        wpts = obj.journeywaypoints_set
        wpts_count = wpts.count()
        for waypoint in wpts.order_by('order'):
            for p in waypoint.passangers.all():
                pobj = passangers.get(
                    p.id,
                    Passanger(start=waypoint.order, user=p, sum=wpts_count))
                pobj.length += 1
                passangers[p.id] = pobj

        context['passangers'] = passangers

        return context


class UserDetail(DetailView):
    model = models.User
