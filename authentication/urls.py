from django.contrib import admin
from . import views
from authentication.views import login_view,register_view, signup,logout_view
from django.urls import path,include


urlpatterns = [
 path('',views.home, name='home'),
   path('signup', views.signup, name='signup'),
   path('signin', views.signin, name='signin'),
   path('signout', views.signout, name='signout'),
   path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
