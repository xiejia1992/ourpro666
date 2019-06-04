from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from ourproapp import user_api_views

# Create your views here.

urlpatterns = [
    url(r'^check_register$', user_api_views.check_register),
    url(r'^register$', user_api_views.register),
    url(r'^login$', user_api_views.login),
    url(r'^api/users$', user_api_views.user_list),
    #url(r'^api/users/(?P<id>(\d+))/$', views.user_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)