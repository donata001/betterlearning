import re
from django.shortcuts import render
from random import randint
import random
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import IntegrityError
from .models import *
from django.utils.timezone import now
from uuid import uuid1
from sklearn.externals import joblib
import pandas as pd


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
BEGIN_COURSE_VIEW = 'begin_course2.html'
IN_COURSE_VIEW = 'course_question_process'
feature = ['accumalated', 'current_level', 'correct_num', 'max_currect_momentum', 
           'aver_speed_at_correct', 'best_speed_at_correct']

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
        q = data.get('ques')
        if step == '1' and q:
            try:
                user = User.objects.create_user(password='sesame',
                                              last_login=now(), 
                                              username=q.replace(" ", ""),
                                              first_name=q.split()[0], 
                                              last_name=q.split()[-1] if len(q) > 1 else None, 
                                              email=q.replace(" ", "")+'@fake.com')  
            except IntegrityError:
                return error_response(request, "Name already taken, please add your nick name at the end.") 
            uid = user.pk
        elif step == '2' and q and user:
            UserProfile.objects.create(user=user,
                                       age=int(data.get('ques'))) 

        elif step == '3' and q and user:
            up = UserProfile.objects.get(user=user)
            up.hobby = data.get('ques')
            up.save()
            
        elif step == '4' and q and user:
            user.set_password(q)
            user.save()

        return HttpResponseRedirect(reverse(REGISTER_VIEW, kwargs={'step': int(step),
                                                                   'uid': uid}))
        

class BeginCourse(View):
    
    def get(self, request, course, suuid=0, level=0, step=0):
        if not request.user.is_authenticated():   
            return error_response(request, "Oops, you are not in, please signin first!")     
        user = request.user       
        
        if not suuid:
            suuid = uuid1().hex
        
        if level == '99':           

            # getting existing max level
            all_records = Sessions.objects.filter(course=int(course),
                                                user=user
                                                ).order_by('-level', '-step')
            if all_records:
                max_level = all_records[0]
                level = max_level.level                  
                step = max_level.step
                suuid = max_level.uuid
            else:
                return error_response(request, "Oops, you don't have any session, begin a new session please!")    
        
        # getting all previous steps to records
        records = Sessions.objects.filter(course=int(course),
                                                level=int(level),
                                                user=user,
                                                uuid=suuid).exclude(end=None)
        clp_id = None
        sid = None 
        button = False
        operand = ""
        show_video = None
        show_cheat = False
        if int(step) == 0 and int(level) > 0:
            # summary and redirect to next level
            base = '{name}, based on our evaluation.'
            if records:
                content = base + ' You need to practice more in current level' 
                if int(level) > 2 and int(level) < 7:
                    show_video = 1  
                    content += ". Watch this lesson will help you"    
                elif int(level) == 7:
                    show_cheat = True 
                    content += ". Review the magic sheet will help you"
                elif int(level) in [8, 9]:
                    show_video = 2       
                    content += ". Watch this lesson will help you."                             
            else:               
                content = ' you are prompted to level ' + level
            content += '. Click on ready to proceed.'    
            suuid = uuid1().hex        
        elif int(level) == 0 and int(step) == 0:                       
            # prepare blackboard content
            clp = ContentLookUp.objects.get(course=int(course), 
                                                   level=int(level), step=int(step))
            clp_id = clp.pk
            content_pk = clp.content_pk
            content = Messages.objects.get(pk=content_pk).content
        elif int(level) == 0:
            num1 = randint(0, 10)
            num2 = randint(0, num1)
            operand = random.choice(["+", "-"])
        elif int(level) == 1:
            num1 = randint(10, 50)
            num2 = randint(0, 10)
            operand = random.choice(["+", "-"])    
        elif int(level) == 2:
            num1 = randint(10, 99)
            num2 = randint(0, 10)
            operand = random.choice(["+", "-"])   
        elif int(level) == 3:
            num2 = randint(10, 50)
            num1 = randint(50, 99)
            operand = random.choice(["+", "-"])
        elif int(level) == 4:
            num1 = randint(100, 999)
            num2 = randint(1, 10)
            operand = random.choice(["+", "-"])
        elif int(level) == 5:
            num1 = randint(100, 999)
            num2 = randint(10, 99)
            operand = random.choice(["+", "-"])
        elif int(level) == 6:
            num1 = randint(100, 999)
            num2 = randint(100, num1)
            operand = random.choice(["+", "-"])
        elif int(level) == 7:
            num1 = randint(1, 10)
            num2 = randint(1, 10)
            operand = "*"
        elif int(level) == 8:
            num1 = randint(1, 10)
            num2 = randint(10, 99)
            operand = "*"
        elif int(level) == 9:
            num1 = randint(1, 10)
            num2 = randint(100, 999)
            operand = "*"
        if operand:
            content = str(num1) + " " + operand + " " + str(num2) + " ="
                                
        if '{name}' in content and user:            
            name = user.first_name
            content = content.replace('{name}', name)

        if int(step) == 0:
            button = True
        if 0<int(step) < 6:
            quiz = True
            # start an session
            sec = Sessions.objects.create(course=int(course),
                                        level=int(level),
                                        step=int(step),
                                        user=user,
                                        uuid=suuid)
            sid = sec.pk
        else:
            quiz = False

        return render(request, BEGIN_COURSE_VIEW, {"content":content,
                                                   "step":int(step) + 1,
                                                   'course': course,
                                                   'level': level,
                                                   'button': button,
                                                   'quiz': quiz,
                                                   'clp_id': clp_id,
                                                   'sid': sid,
                                                   'records': records,
                                                   'suuid': suuid,
                                                   'show_video': show_video,
                                                   "show_cheat":show_cheat                             
                                                   })
    
    def post(self, request, course, suuid, level, step):
        
        if not request.user.is_authenticated():   
            return error_response(request, "Oops, you are not in, please signin first!")     
        data = request.POST
        
        quiz, clp_id, ques, sid, exp = data.get('quiz'), data.get('clp_id'), data.get('ques'), data.get('sid'), data.get('content')
        Messages.objects.create(type=1,
                                content=ques,
                                session_id=sid,
                                user=request.user)
        
        if quiz and clp_id and sid and exp:
            # 123 + 45 = 
            l = exp.split()
            num1 = int(l[0])
            oprand = l[1]
            num2 = int(l[2])
            if oprand == '+':
                ans = num1 + num2
            elif oprand == '-':
                ans = num1 - num2
            elif oprand == '*':
                ans = num1 * num2
            elif oprand == '/':
                ans = num1 // num2
                                
            try:
                #clp = ContentLookUp.objects.get(pk=clp_id)
                sec = Sessions.objects.get(pk=sid)
            except:
                return error_response(request, "Session error, please redo session") 

            if str(ans) == ques:
                sec.correct = True
            else:
                sec.correct = False
            sec.end = now()
            sec.save()
            
        # step 6 data collecting to prediction table
        
        if int(step) == 6:
            secs = Sessions.objects.filter(level=int(level),
                                                user=request.user,
                                                course=int(course),
                                                correct=True, 
                                                uuid=suuid).order_by('step')
            # if all 5 got wrong
            if not secs:
                return HttpResponseRedirect(reverse(IN_COURSE_VIEW, kwargs={'step': 0,
                                                                   'course': course,
                                                                   'level': level,
                                                                   'suuid': suuid}))
                                                
            # max_correct_momentum
            max_len = 0
            prev = None
            counter = 0
            for s in secs:
                if prev == None:
                    max_len = 1
                    counter = 1
                    prev = s.step
                    continue
                if s.step - prev == 1:
                    counter += 1   
                    max_len = max(max_len, counter)
                else:
                    counter = 1     
                prev = s.step                     
                                
            # aver_speed_at_correct
            aver_speed_at_correct = sum([(sec.end-sec.begin).seconds for sec in secs])*1.0 / secs.count()
            
            # best_speed_at_correct
            best_speed_at_correct = min([(sec.end-sec.begin).seconds for sec in secs]) 
            # accumalated gets all the past level correct number sum
            
            max_levels = Prediction.objects.filter(user=request.user).order_by('-current_level', '-accumalated', '-correct_num')

            if max_levels:
                max_level = max_levels[0]
                acc = max_level.accumalated
                acc += secs.count()
            else:
                acc = secs.count()

            p = Prediction.objects.create(base_personal=10,
                                      base_general=10,
                                      accumalated=acc,
                                      current_level=int(level),
                                      correct_num=secs.count(),
                                      max_currect_momentum=max_len,
                                      aver_speed_at_correct=aver_speed_at_correct,
                                      best_speed_at_correct=best_speed_at_correct,
                                      predict=True,
                                      user=request.user
                                      )
            
            df =  pd.DataFrame(list(Prediction.objects.filter(pk=p.pk).values()))
            ft = df[feature]
            ft['age'] = request.user.userprofile.age
            model = joblib.load('./models/model.pkl')    
            p.next_level = model.predict(ft) [0]    
            p.save()
            
            level = p.next_level
            step = '0'
        return HttpResponseRedirect(reverse(IN_COURSE_VIEW, kwargs={'step': int(step),
                                                                   'course': course,
                                                                   'level': level,
                                                                   'suuid': suuid}))
        

class ChoseLevel(View):
    
    def get(self, request, course):
        if request.user.is_authenticated():  
            return render(request, CHOSE_LEVEL_TEMPLATE, {
                                                          'course':course})
        else:
            return error_response(request, "Oops, you are not in, please login!")


class ComingSoon(View):
    
    def get(self, request):
        return error_response(request, "Coming soon!")
                

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
