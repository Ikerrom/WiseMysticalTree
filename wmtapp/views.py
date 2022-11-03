from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

###
def createuser(request):
    # Superusuario
    user = User.objects.create_user(
        'myusername', 'myemail@crazymail.com', 'mypassword')

    user.first_name = 'John'
    user.last_name = 'Citizen'
    user.save()
###

def menu(request):
    template = loader.get_template('menu.html')
    return HttpResponse(template.render())
