from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^home$', Home.as_view(), name='home_view'),
    url(r'^login$', Login.as_view(), name='user_login'),
    url(r'^logout$', Logout.as_view(), name='user_logout'),
    url(r'^courses', Courses.as_view(), name='courses_view'),   
    url(r'^register/(?P<step>[0-9]+)/(?P<uid>[0-9]+)$', Register.as_view(), name='register_view'),
    url(r'^register', Register.as_view(), name='register_view'),
    url(r'^question_process/(?P<step>[0-9]+)/(?P<uid>[0-9]+)$', Register.as_view(), name='question_process'),
    url(r'^chose_level/(?P<course>[0-9]+)$', ChoseLevel.as_view(), name='chose_level'),
    url(r'^begin_course/(?P<course>[0-9]+)/(?P<level>[0-9]+)$', BeginCourse.as_view(), name='begin_course_view'),
    url(r'^course_question_process/(?P<course>[0-9]+)/(?P<level>[0-9]+)/(?P<step>[0-9]+)$', BeginCourse.as_view(), name='course_question_process'),
    
     
]