from django.urls import path
from . import views, auth_views, ride_views

urlpatterns = [
    path ('', views.index, name = 'index'),
    path ('signup', auth_views.signup, name = 'signup'),
    path ('signin', auth_views.signin, name = 'signin'),
    path ('signout', auth_views.signout, name = 'signout'),
    path ('pleaseLogin', views.pleaseLogin, name = 'pleaseLogin'),
    path ('insertRide', ride_views.insertRide, name = 'insertRide'), 
    path ('viewRidesByUser', ride_views.viewRidesByUser, name = 'viewRidesByUser'),
    path ('searchRide', ride_views.searchRides, name = 'searchRides'), 
    path('registerToken', auth_views.registerToken, name = 'registerToken'),
    path('verifyToken', auth_views.verifyToken, name = 'verifyToken'), 
    path ('changeRideStatus', ride_views.changeRideStatus, name='changeRideStatus')

]

