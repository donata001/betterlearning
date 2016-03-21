from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from django.utils.timezone import now


HOME_TEMPLATE = 'home.html'
HOME_VIEW = 'home_view'
LOGIN_TEMPLATE = ''
LOGIN_VIEW = 'user_login'
COURSES_TEMPLATE = 'courses.html'
REGISTER_TEMPLATE = 'register.html'
REGISTER_VIEW = 'register_view'


class Home(View):
    
    def get(self, request):
        return render(request, HOME_TEMPLATE)
    
class Courses(View):
    
    def get(self, request):
        return render(request, COURSES_TEMPLATE)
    
class Register(View):
    
    def get(self, request, step=0, uid=0):
        data = request.GET

        if uid:
            try:
                user = User.objects.get(pk=int(uid))
            except:
                user = None
          
        content_pk = ContentLookUp.objects.get(level=0, step=int(step)).content_pk
        content = Messages.objects.get(pk=content_pk).content
        
        if '{name}' in content and user:            
            name = user.first_name
            content = content.replace('{name}', name)
        return render(request, REGISTER_TEMPLATE, {"content":content,
                                                   "step":int(step)+1,
                                                   "uid":uid
                                                   })
    
    def post(self, request, step, uid):
        data = request.POST
        print step, uid
        if uid:
            try:
                user = User.objects.get(pk=int(uid))
            except:
                user = None
        if step == '1' and data.get('ques'):
            user = User.objects.create_user(password='sesame',
                                          last_login=now(), 
                                          username=data.get('ques'),
                                          first_name=data.get('ques').split()[0], 
                                          last_name=data.get('ques').split()[1], 
                                          email='fake@fa.com')  
            uid = user.pk
        elif step == '2' and data.get('ques') and user:
            p = UserProfile.objects.create(user=user,
                                       age=int(data.get('ques'))) 

        elif step == '3' and data.get('ques') and user:
            up = UserProfile.objects.get(user=user)
            up.hobby = data.get('ques')
            up.save()
        return HttpResponseRedirect(reverse(REGISTER_VIEW, kwargs={'step': int(step),
                                                                   'uid': uid}))

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
