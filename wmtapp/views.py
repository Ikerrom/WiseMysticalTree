from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

def MainPage(request):
    return HttpResponseRedirect(reverse('MainPage'))

def Login(request):
    return HttpResponseRedirect(reverse('Login'))

def GuessPage(request):
    return HttpResponseRedirect(reverse('GuessPage'))

def Carta(request):
    return HttpResponseRedirect(reverse('Carta'))