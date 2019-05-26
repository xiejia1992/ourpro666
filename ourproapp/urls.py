from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ourproapp import views

# Create your views here.

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^api/users$', views.user_list),
    url(r'^api/users/(?P<id>(\d+))/$', views.user_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)