# APP: validation
from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name = 'login'),
    url(r'^validate/(?P<route>(reg|login))$', views.validateUser, name = 'validate'),
    url(r'^logout/$', views.logOut, name = 'logout'),

]
