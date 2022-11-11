from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json

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

#@csrf_exempt
#def addtocarrito(request):
#    mealname = request.POST['name']
#    desc = request.POST['desc']
#    price = request.POST['price']
#    photo = request.POST['photo']
#    sukaldariid = request.POST['sukaldari']
#    sukaldariobj = Sukaldari.objects.get(id=sukaldariid)
#    platera = Platera(name = name, desc = desc, price= price, photo = photo, sukaldari = sukaldariobj)
#    platera.save()
#    return HttpResponseRedirect(reverse('platerak',kwargs={'price': 0}))   

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
    intoleranceclist =[]

    meallist = []

    for preference in preferenceslist:
        preferenceobj = CategoryGroup.objects.get(cgname = preference)
        preferencecategorylist = CategoryGroupCategory.objects.filter(cg=preferenceobj)
        for preferencecategory in preferencecategorylist:
            preferenceclist.append(preferencecategory.c)

    for cg in cgfilterlist:
        cgobj = CategoryGroup.objects.get(cgname=cg)
        cgcaregorylist = CategoryGroupCategory.objects.filter(cg=cgobj)
        for cgcaregory in cgcaregorylist:
            intoleranceclist.append(cgcaregory.c)

    for category in preferenceclist:
        meallist = list(MealCategory.objects.filter(c=category))

    swapped = False
    for i in range(len(meallist)-1):
        for j in range(0,len(meallist)-i-1):
            meal1clist = list(MealCategory.objects.filter(meal=meallist[j].meal));
            meal2clist = list(MealCategory.objects.filter(meal=meallist[j + 1].meal));
            if len(meal1clist) > len(meal2clist):
                swapped = True
                meallist[j], meallist[j + 1] = meallist[j + 1], meallist[j]
        if not swapped:
            break

    notallowed = []
    allmealsc = MealCategory.objects.all()
    for mealc in allmealsc:
        for category in intoleranceclist:
            if mealc.c.cname == category.cname:
                already = False;
                for meal in notallowed:
                    if mealc.meal.mealname == meal.meal.mealname:
                        already = True
                if not already:
                    notallowed.append(mealc)


    allmeals = MealCategory.objects.all()     
    for meal in allmeals:
        already = False
        for notallow in notallowed:
            if meal.meal.mealname == notallow.meal.mealname:
                already = True;
        if not already:
            for meall in meallist:
                already2 = False
                if meall.meal.mealname == meal.meal.mealname:
                    already2 = True
            if not already2:
                meallist.append(meal) 
    
    print(meallist)