from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
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
    intolerances = request.POST.get('intolerances')
    preferences = request.POST.get('preferences')
    categories = Category.objects.all()

    filteredquestions = []
    categorylist = []

    for category in categories:
        categorylist.append(category.categoryname)
    intoleranceslist = json.loads(intolerances)
    preferenceslist = json.loads(preferences)

    for intolerance in intoleranceslist:
        intoleranceobj = Intolerance.objects.get(intolerancename=intolerance)
        intolerancecaregorylist = IntoleranceCategory.objects.filter(intolerance=intoleranceobj)

        for intolerancecaregory in intolerancecaregorylist:
            categorylist.remove(intolerancecaregory.category.categoryname)

    questioncategories = list(QuestionCategory.objects.all())
    for category in categorylist:
        for questioncategory in questioncategories:
            if category == questioncategory.category.categoryname:
                already = False
                for filteredquestion in filteredquestions:
                    if questioncategory.question.question == filteredquestion.question:
                        already= True
                if not already:
                    filteredquestions.append(questioncategory.question)

    swapped = False
    for i in range(len(filteredquestions)-1):
        for j in range(0,len(filteredquestions)-i-1):
            if filteredquestions[j].priority > filteredquestions[j + 1].priority:
                swapped = True
                filteredquestions[j].priority, filteredquestions[j + 1].priority = filteredquestions[j + 1].priority, filteredquestions[j].priority
        if not swapped:
            break;
    
    question = QuestionIntolerance.objects.get(question=filteredquestions[0])

    return JsonResponse([filteredquestions[0].question,question.intolerance.intolerancename],safe=False)
    

 