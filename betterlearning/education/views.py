from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages


HOME_TEMPLATE = 'home.html'
HOME_VIEW = 'home_view'
LOGIN_TEMPLATE = ''
LOGIN_VIEW = 'user_login'
COURSES_TEMPLATE = 'courses.html'
REGISTER_TEMPLATE = 'register.html'


class Home(View):
    
    def get(self, request):
        return render(request, HOME_TEMPLATE)
    
class Courses(View):
    
    def get(self, request):
        return render(request, COURSES_TEMPLATE)
    
class Register(View):
    
    def get(self, request):
        return render(request, REGISTER_TEMPLATE)

class Login(View):

    def get(self, request):
        if request.user.is_authenticated():            
            return HttpResponseRedirect(reverse(HOME_VIEW))            
        return render(request, LOGIN_TEMPLATE)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Incorrect username/password.')

        return HttpResponseRedirect(reverse(LOGIN_VIEW))
    
    
class Logout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(LOGIN_VIEW))
