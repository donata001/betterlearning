from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.timezone import now


HOME_TEMPLATE = 'home.html'
HOME_VIEW = 'home_view'
LOGIN_TEMPLATE = 'login.html'
LOGIN_VIEW = 'user_login'
COURSES_TEMPLATE = 'courses.html'
REGISTER_TEMPLATE = 'register.html'
REGISTER_VIEW = 'register_view'
ERROR_TEMPLATE = 'error.html'
CHOSE_LEVEL_TEMPLATE = 'chose_level.html'
CHOSE_LEVEL_VIEW = 'chose_level'
COURSES_VIEW = 'courses_view'
BEGIN_COURSE_VIEW = 'begin_course.html'
IN_COURSE_VIEW = 'course_question_process'


class Home(View):
    
    def get(self, request):
        return render(request, HOME_TEMPLATE)
    
class Courses(View):
    
    def get(self, request):
        return render(request, COURSES_TEMPLATE)
    
class Register(View):
    
    def get(self, request, step=0, uid=0):

        if uid:
            try:
                user = User.objects.get(pk=int(uid))
            except:
                user = None
          
        content_pk = ContentLookUp.objects.get(level=0, step=int(step), course=0).content_pk
        content = Messages.objects.get(pk=content_pk).content
        
        if '{name}' in content and user:            
            name = user.first_name
            content = content.replace('{name}', name)
        if '{username}' in content and user:            
            name = user.username
            content = content.replace('{username}', name)
        if step == '4':
            blink = True
        else:
            blink = False
            
        return render(request, REGISTER_TEMPLATE, {"content":content,
                                                   "step":int(step)+1,
                                                   "uid":uid,
                                                   "blink":blink                                          
                                                   })
    
    def post(self, request, step, uid):
        data = request.POST

        if uid:
            try:
                user = User.objects.get(pk=int(uid))
            except:
                user = None
        if step == '1' and data.get('ques'):
            user = User.objects.create_user(password='sesame',
                                          last_login=now(), 
                                          username=data.get('ques').replace(" ", ""),
                                          first_name=data.get('ques').split()[0], 
                                          last_name=data.get('ques').split()[1], 
                                          email=data.get('ques').replace(" ", "")+'@fake.com')  
            uid = user.pk
        elif step == '2' and data.get('ques') and user:
            UserProfile.objects.create(user=user,
                                       age=int(data.get('ques'))) 

        elif step == '3' and data.get('ques') and user:
            up = UserProfile.objects.get(user=user)
            up.hobby = data.get('ques')
            up.save()
            
        elif step == '4' and data.get('ques') and user:
            user.set_password(data.get('ques'))
            user.save()

        return HttpResponseRedirect(reverse(REGISTER_VIEW, kwargs={'step': int(step),
                                                                   'uid': uid}))
        

class BeginCourse(View):
    
    def get(self, request, course, level=0, step=0):
        if not request.user.is_authenticated():   
            return error_response(request, "Oops, you are not in, please signin first!")     
        user = request.user       
 
        clp = ContentLookUp.objects.get(course=int(course), 
                                               level=int(level), step=int(step))
        clp_id = clp.pk
        content_pk = clp.content_pk
        content = Messages.objects.get(pk=content_pk).content
        sid = None
        
        if '{name}' in content and user:            
            name = user.first_name
            content = content.replace('{name}', name)

        if int(step) == 0:
            button = True
        else:
            button = False

        if 0<int(step) < 6:
            quiz = True
            # start an session
            sec = Sessions.objects.create(course=int(course),
                                        level=int(level),
                                        step=int(step),
                                        user=user)
            sid = sec.pk
        else:
            quiz = False

        return render(request, BEGIN_COURSE_VIEW, {"content":content,
                                                   "step":int(step)+1,
                                                   'course': course,
                                                   'level': level,
                                                   'button': button,
                                                   'quiz': quiz,
                                                   'clp_id': clp_id,
                                                   'sid': sid                                       
                                                   })
    
    def post(self, request, course, level, step):
        
        if not request.user.is_authenticated():   
            return error_response(request, "Oops, you are not in, please signin first!")     
        data = request.POST
        
        quiz, clp_id, ques, sid = data.get('quiz'), data.get('clp_id'), data.get('ques'), data.get('sid')
        Messages.objects.create(type=1,
                                content=ques,
                                session_id=sid,
                                user=request.user)
        
        if quiz and clp_id and sid:
            try:
                clp = ContentLookUp.objects.get(pk=clp_id)
                sec = Sessions.objects.get(pk=sid)
            except:
                return error_response(request, "Session error, please redo session") 
            ans = clp.answer
            if ans == ques:
                sec.correct = True
            else:
                sec.correct = False
            sec.end = now()
            sec.save()

        return HttpResponseRedirect(reverse(IN_COURSE_VIEW, kwargs={'step': int(step),
                                                                   'course': course,
                                                                   'level': level}))
        

class ChoseLevel(View):
    
    def get(self, request, course):
        if request.user.is_authenticated():  
            return render(request, CHOSE_LEVEL_TEMPLATE, {
                                                          'course':course})
        else:
            return error_response(request, "Oops, you are not in, please login!")

        

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
            return error_response(request, 'Incorrect username/password.')

        return HttpResponseRedirect(reverse(COURSES_VIEW))
    
    
class Logout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(LOGIN_VIEW))
    
def error_response(request, message):
    return render(request, ERROR_TEMPLATE, {'message': message})
