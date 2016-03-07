from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^betterlearningforkids/', include('education.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
