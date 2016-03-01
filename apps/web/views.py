from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, RedirectView, View
from . import models
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from emailusernames.utils import create_user

from django.http import HttpResponse, HttpResponseRedirect

## Import forms
from . import forms


def index(request):
    link_dict = {"Login": 'login_screen', "Register": 'register',
                 "Log out": 'logout_user', "Car Management": 'cars',
                 "User Management": 'user'}
    return render(request, 'web/index.html', {"links": link_dict})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('../../')


class LoginScreen(View):
    header = "Login"

    user_name = None
    user_pass = None
    login_form = forms.LoginForm()
    redirect_bool = False
    info_text = None

    user = None

    def get(self, request):
        return render(request, 'web/login_screen.html', {"form": self.login_form,
                                                         "header": self.header})

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
    header = "User Registration"

    user_mail = None
    user_mail_confirm = None
    user_pass = None
    user_pass_confirm = None
    register_form = forms.RegisterForm()

    correct_day = None
    asked_day = None

    question_ok = False
    user_exists = False

    correct_details = {}

    request = None

    def get(self, request):
        return render(request, 'web/register.html', {"form": self.register_form,
                                                     "header": self.header})

    def post(self, request):
        self.correct_day = self.register_form.correct_day
        self.request = request

        self._post_get_details()
        self._check_security_question()
        self._check_details()
        self._check_existing_user()

        if self.user_exists:
            return HttpResponse("ERROR: USER ALREADY EXISTS!")
        else:
            new_user = create_user(email = self.user_mail, password = self.user_pass)
            new_user.save()
            return HttpResponse("SUCCESS: USER CREATED")

        #return render(request, 'web/register.html', {"form": self.register_form})


    def _post_get_details(self):
        self.user_mail = self.request.POST['user_email']
        self.user_mail_confirm = self.request.POST['user_email_confirm']
        self.user_pass = self.request.POST['user_password']
        self.user_pass_confirm = self.request.POST['user_password_confirm']

        self.asked_day = self.request.POST['random_antibot']


    def _check_security_question(self):
        self.correct_day = self.register_form.correct_day
        if self.correct_day == self.asked_day:
            self.question_ok = True
        else:
            return HttpResponse("ERROR: INVALID CONTROL ANSWER!")


    def _check_details(self):
        self.correct_details.update({"correct_name": self.user_mail == self.user_mail_confirm})
        self.correct_details.update({"correct_pass": self.user_pass == self.user_pass_confirm})

        if False in self.correct_details:
            return HttpResponse("ERROR: Some data you entered does not match")


    def _check_existing_user(self):
        test_auth = authenticate(username = self.user_mail, password = self.user_pass)
        if test_auth:
            self.user_exists = True
        else:
            self.user_exists = False



class CarManagement(View):
    header = "Car Management page"

    model = None
    owner = None
    name = None
    color = None

    air_conditioning = False
    animals_allowed = False
    has_wifi = False
    has_highway_sign = False
    smoking_allowed = False

    register_sign = None
    reg_notice = ("NOTE", "If you really don't want to, you DO NOT have\
                     to enter your national car sign. Hovever, if\
                    you fill it, you will make it easier for\
                     passengers to find you.")

    form = forms.CarManageForm()
    inp_method = None
    message = None

    def get(self, request):
        self.model = models.Vehicle.objects.filter(owner=request.user)
        return render(request, 'web/cars.html', {"form": self.form,
                                                 "car_list": self.model,
                                                 "message": self.message,
                                                 "reg_notice": self.reg_notice,
                                                 "header": self.header})

    def post(self, request):
        self.inp_method = request.POST.get('method')
        print (request.POST)
        if self.inp_method == 'add_vehicle':
            return self._add_car(request)
        elif self.inp_method == 'remove_vehicle':
            return self._delete_car(request)
        else:
            return HttpResponse("UNKOWN ERROR WITH DATABASE.")

    def _delete_car(self, in_request):
        self.owner = in_request.user
        remove_id = in_request.POST.get('car_id')
        models.Vehicle.objects.filter(owner = self.owner, id = remove_id).delete()
        return HttpResponseRedirect(".")

    def _add_car(self, in_request):
        self.owner = in_request.user
        self.name = in_request.POST.get('car_name')
        self.color = in_request.POST.get('color')

        self.air_conditioning = in_request.POST.get('air_conditioning', False)
        self.animals_allowed = in_request.POST.get('animals_allowed', False)
        self.has_wifi = in_request.POST.get('has_wifi', False)
        self.has_highway_sign = in_request.POST.get('has_highway_sign', False)
        self.smoking_allowed = in_request.POST.get('smoking_allowed', False)

        self.register_sign = in_request.POST.get('register_sign')
        return self._check_required()

    def _check_required(self):
        if self.name and self.color:
            new_car = models.Vehicle(owner=self.owner, name=self.name,
                                     color=self.color, register=self.register_sign,
                                     air_conditioning=self.air_conditioning,
                                     animals_allowed=self.animals_allowed,
                                     wifi_on_board=self.has_wifi,
                                     smoking_allowed=self.smoking_allowed,
                                     highway_mark=self.has_highway_sign)
            new_car.save()
            return HttpResponseRedirect(".")
        else:
            return HttpResponse("FAILED TO SAVE, MISSING DATA!")


class UserManagement(View):
    header = "User control panel and information page"
    form = forms.ManageForm

    def get(self, request):
        return render(request, 'web/user.html', {"form": self.form,
                                                 "header": self.header})
    def post(self, request):
        pass


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
