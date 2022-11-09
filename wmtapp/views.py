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
    cgfilterstr = request.POST.get('categorygroups')
    preferences = request.POST.get('preferences')
    number = request.POST.get('number')
    filteredquestions = []
    categorylist = []

    #POST gotten str to list
    for category in Category.objects.all():
        categorylist.append(category.cname)
    cgfilterlist = json.loads(cgfilterstr)
    preferenceslist = json.loads(preferences)

    #Remove all categorygroup categories from category list
    for cg in cgfilterlist:
        cgobj = CategoryGroup.objects.get(cgname=cg)
        cgcaregorylist = CategoryGroupCategory.objects.filter(cg=cgobj)
        for cgcaregory in cgcaregorylist:
            categorylist.remove(cgcaregory.c.cname)

    #Get filter questions,by cheking the questioncategories in the category list without duplicates
    questioncategories = list(QuestionCategory.objects.all())
    for category in categorylist:
        for questioncategory in questioncategories:
            if category == questioncategory.c.cname:
                already = False
                for filteredquestion in filteredquestions:
                    if questioncategory.question.question == filteredquestion.question:
                        already= True
                if not already:
                    filteredquestions.append(questioncategory.question)

    #Bubble sort the filteredquestions by priority
    swapped = False
    for i in range(len(filteredquestions)-1):
        for j in range(0,len(filteredquestions)-i-1):
            if filteredquestions[j].priority > filteredquestions[j + 1].priority:
                swapped = True
                filteredquestions[j], filteredquestions[j + 1] = filteredquestions[j + 1], filteredquestions[j]
        if not swapped:
            break;
    
    #Send back the data to the ajax
    question = QuestionCategoryGroup.objects.get(question=filteredquestions[0+int(number)])
    return JsonResponse([filteredquestions[0+int(number)].question,question.cg.cgname],safe=False)