from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^home$', Home.as_view(), name='home_view'),
    url(r'^login$', Login.as_view(), name='user_login'),
    url(r'^logout$', Logout.as_view(), name='user_logout'),
    url(r'^courses', Courses.as_view(), name='courses_view'),
    url(r'^register', Register.as_view(), name='register_view'),
    
    
]