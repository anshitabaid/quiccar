from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name = 'index'),
    path ('signup', views.signup, name = 'signup'),
    path ('signin', views.signin, name = 'signin'),
    path ('signout', views.signout, name = 'signout'),
    path ('pleaseLogin', views.pleaseLogin, name = 'pleaseLogin'),
    path ('insertRide', views.insertRide, name = 'insertRide'), 
    path ('viewRidesByUser', views.viewRidesByUser, name = 'viewRidesByUser'),
    path ('searchRide', views.searchRides, name = 'searchRides')
]