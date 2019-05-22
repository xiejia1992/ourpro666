from django.conf.urls import url
from ourproapp import views

# Create your views here.

urlpatterns = [
    url(r'^$', views.login),
]