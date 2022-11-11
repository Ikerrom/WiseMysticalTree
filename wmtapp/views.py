from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import random

from django.contrib.auth.models import User as UserDj
from django.shortcuts import get_object_or_404

##
def index(request):
    
    
    if request.user.id == None:
        template = loader.get_template('index.html')
        return HttpResponse(template.render())
    
    user = UserDj.objects.get(id = request.user.id)
    return render(request, 'index.html', {'user': user})

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def logout(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())
##


def menu(request):
    meal = Meal.objects.all()
    mealcategory = MealCategory.objects.all()
    template = loader.get_template('menu.html')
    context = {
    'meal': meal,
    'mealcategory' : mealcategory,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def mealtobatch(request):
    meal = request.POST['meal']
    quantity = request.POST['quantity']
    mealobj = Meal.objects.get(id=meal)
    batch = Batch(meal = mealobj,quantity = quantity)
    batch.save()
    return HttpResponseRedirect(reverse('menu'))

@csrf_exempt
def addtocarrito(request):
    user = request.POST['user']
    batch = request.POST['batch']
    userobj = User.objects.get(id=user)
    batchobj = Batch.objects.get(id=batch)
    karritoa = UserBatchCart(user = userobj,batch = batchobj)
    karritoa.save()
    return HttpResponseRedirect(reverse('menu'))   

@csrf_exempt
def addmeal(request,id):
    template = loader.get_template('addmeal.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
@csrf_exempt
def filterquestion(request):
    cgfilterstr = request.POST.get('categorygroups')
    number = request.POST.get('number')
    filteredquestions = []
    categorylist = []

    #POST gotten str to list
    for category in Category.objects.all():
        categorylist.append(category.cname)
    cgfilterlist = json.loads(cgfilterstr)


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
            break

    if int(number) < len(filteredquestions):
        #Send back the data to the ajax
        question = QuestionCategoryGroup.objects.get(question=filteredquestions[0+int(number)])
        return JsonResponse([question.question.question,question.cg.cgname,question.question.preference],safe=False)
    else:
        return JsonResponse(["","",False],safe=False)
    

@csrf_exempt
def filtermeal(request):
    preferencesstr = request.POST.get('preferences')
    cgfilterstr = request.POST.get('categorygroups')
    preferenceslist = json.loads(preferencesstr)
    cgfilterlist = json.loads(cgfilterstr)

    preferenceclist = []
    cgfilterc =[]
    intoleranceclist = []
    meallist = []
    perfectmatch = []
    notperfecto = []

    for preference in preferenceslist:
        preferenceobj = CategoryGroup.objects.get(cgname = preference)
        preferencecategorylist = CategoryGroupCategory.objects.filter(cg=preferenceobj)
        for preferencecategory in preferencecategorylist:
            preferenceclist.append(preferencecategory.c)

    for cg in cgfilterlist:
        cgobj = CategoryGroup.objects.get(cgname=cg)
        cgcaregorylist = CategoryGroupCategory.objects.filter(cg=cgobj)
        for cgcaregory in cgcaregorylist:
            cgfilterc.append(cgcaregory.c)

    for category in cgfilterc:
        already1 = False
        for preference in preferenceclist:
            if category.cname == preference.cname:
                already1 = True
        if not already1:
            already = False
            for intolerance in intoleranceclist:
                if category.cname == intolerance.cname:
                    already = True
            if not already:
                intoleranceclist.append(category)

    allmeals = Meal.objects.all()
    for meal in allmeals:
        allmatch = True
        mealcategorymeals = list(MealCategory.objects.filter(meal = meal))
        for mealc in mealcategorymeals:
            isin = False
            for preference in preferenceclist:
                if mealc.c.cname == preference.cname:
                    isin = True
            if not isin:
                allmatch = False
        if allmatch:
            isthere = False
            for mealc in mealcategorymeals:
                for intolerance in intoleranceclist:
                    if intolerance.cname == mealc.c.cname:
                        isthere = True
            if not isthere:
                perfectmatch.append(mealc)
        if not allmatch:
            isthere = False
            for mealc in mealcategorymeals:
                for intolerance in intoleranceclist:
                    if intolerance.cname == mealc.c.cname:
                        isthere = True
            if not isthere:
                notperfecto.append(mealc)

    swapped = False
    for i in range(len(notperfecto)-1):
        for j in range(0,len(notperfecto)-i-1):
            notperfecto1 = list(MealCategory.objects.filter(meal=notperfecto[j].meal));
            notperfecto2 = list(MealCategory.objects.filter(meal=notperfecto[j + 1].meal));
            if len(notperfecto1) > len(notperfecto2):
                swapped = True
                notperfecto[j], notperfecto[j + 1] = notperfecto[j + 1], notperfecto[j]
        if not swapped:
            break
    
    if len(perfectmatch) > 0:
        index = random.randrange(0, len(perfectmatch)-1)
        meallist.append(perfectmatch[index])
        perfectmatch.pop(index)

    for obj in perfectmatch:
        meallist.append(obj)
    for obj in notperfecto:
        meallist.append(obj)

    jsonmealclist =[]
    for mealc in meallist:
        jsonmealist =[]
        meal =[]
        meal.append(mealc.meal.mealname)
        meal.append(mealc.meal.mealdesc)
        meal.append(mealc.meal.mealphoto)
        meal.append(str(mealc.meal.price))
        meal.append(str(mealc.meal.discount))

        jsonmealist.append(meal)

        mealcategories =MealCategory.objects.filter(meal=mealc.meal)
        for mealcategory in mealcategories: 
            c =[]
            c.append(mealcategory.c.cname)
            c.append(mealcategory.c.cphoto)
            jsonmealist.append(c)
        jsonmealclist.append(jsonmealist)

    return JsonResponse(jsonmealclist,safe=False)