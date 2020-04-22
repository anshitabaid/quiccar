from django.urls import path
from . import views

urlpatterns = [
    path ('signup', views.signup, name = 'signup'),
    path ('signin', views.signin, name = 'signin'),
    path ('insertRide', views.insertRide, name = 'insertRide'), 
    path ('viewRidesByUser', views.viewRidesByUser, name = 'viewRidesByUser'),
    path ('searchRide', views.searchRides, name = 'searchRides')
]