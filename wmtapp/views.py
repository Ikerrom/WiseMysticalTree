from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

def MainPage(request):
    return HttpResponseRedirect(reverse('MainPage'))

def Login(request):
    return HttpResponseRedirect(reverse('Login'))

def GuessPage(request):
    return HttpResponseRedirect(reverse('GuessPage'))

###
def CreateUser(request):
    #Superusuario
    user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
    
    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
###

def Carta(request):
    return HttpResponseRedirect(reverse('Carta'))