from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

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

@csrf_exempt
def filterquestion(request):
    categories = request.POST.get('categories')
    intolerances = request.POST.get('intolerances')
    preferences = request.POST.get('preferences')
    categorieslist = json.loads(categories)
    intoleranceslist = json.loads(intolerances)
    preferenceslist = json.loads(preferences)

    #questions = list(Question.objects.all().values())

    