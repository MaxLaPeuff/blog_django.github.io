from django.urls import path
from .views import List, detailView
from blog import views

urlpatterns = [
    path('home', List.as_view(), name='home'),
   path('detail/<slug:slug>',detailView,name='detailView'),
    
    path('',views.maison, name='maison'),
    path('register',views.register,name='register'),
    path('login',views.logIn,name='login'),
    path('logout',views.logOut,name='logout'),
    path('activate/<uidb64>/<token>' , views.activate , name="activate")
   
]