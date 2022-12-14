from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import render   
from django.template import loader
from django.urls import reverse
from .models import *
import random
import time
import json

def index(request):
    template = loader.get_template('index.html')
    if request.user.id == None:
        return HttpResponse(template.render())
    userdj = request.user
    user = User.objects.get(uid=userdj.id)
    context = {
    'userdj': userdj,
    'user':user
    }
    return HttpResponse(template.render(context, request))

def logged(request):
    template = loader.get_template('logged.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def editprofield(request):
    template = loader.get_template('registration/editprofield.html')
    return HttpResponse(template.render())

def logout(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def register(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            adduser()
            return HttpResponseRedirect(reverse("login"))
    else:
        user = UserCreationForm()
    context = {'form': user}
    return render(request, 'registration/register.html', context)

def adduser():
    Authuser = get_user_model()
    djuser = Authuser.objects.all().last()
    user = User(uid = djuser)
    user.save()

def menu(request):
    meals = Meal.objects.all()
    mealcategories = MealCategory.objects.all()
    template = loader.get_template('menu.html')
    context = {
        'meals': meals,
        'mealcategories' : mealcategories,
        }
    if request.user.id != None:
        userdj = request.user
        user = User.objects.get(uid=userdj.id)
        context = {
        'meals': meals,
        'mealcategories': mealcategories,
        'userdj': userdj,
        'user':user,
        }
    return HttpResponse(template.render(context, request))

def cart(request):
    if request.user.id == None:
        return HttpResponseRedirect(reverse("login"))
    userdj = request.user
    user = User.objects.get(uid=userdj.id)
    batches = UserBatchCart.objects.filter(user=user)
    template = loader.get_template('cart.html')
    context = {
    'batches': batches,
    'userdj' : userdj,
    'user' : user,
    }
    return HttpResponse(template.render(context, request))

def deletebatch(request,id):
    UserBatchCart.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('cart'))

def editprofile(request):
    if request.user.id == None:
        return HttpResponseRedirect(reverse("login"))
    userdj = request.user
    user = User.objects.get(uid=userdj.id)
    template = loader.get_template('registration/editprofile.html')
    context = {
            'user':user
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def addlogo(request):
    logo = request.POST['logo']
    userdj = request.user
    user = User.objects.get(uid=userdj.id)
    user.userphoto = logo
    user.save()
    return HttpResponseRedirect(reverse('index'))

def history(request):
    if request.user.id == None:
        return HttpResponseRedirect(reverse("login"))
    userdj = request.user
    user = User.objects.get(uid=userdj.id)
    usercarts = list(UserBatchHistory.objects.filter(user=user))
    template = loader.get_template('history.html')
    grouped = []
    tmp =""
    for usercart in usercarts:
        if usercart.date != tmp:
            grouped.append(UserBatchHistory.objects.filter(date=usercart.date))
            tmp = usercart.date
    grouped.reverse()
    context = {
    'grouped' : grouped,
    'userdj' : userdj,
    'user' : user,
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def addtocart(request,batch):
    user = request.user
    userobj = User.objects.get(uid=user.id)
    cart = UserBatchCart(user = userobj,batch = batch)
    cart.save()

@csrf_exempt
def carttohistory(request):
    user = request.user
    userobj = User.objects.get(uid=user.id)
    userbatchcarts = UserBatchCart.objects.filter(user=userobj)
    date = time.strftime("%Y-%m-%d %H:%M")
    for cart in userbatchcarts:
            history = UserBatchHistory(user = cart.user,batch = cart.batch,date = date)
            history.save()
    UserBatchCart.objects.filter(user=userobj).delete()
    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def mealtobatch(request,id):
    mealid = request.POST['mealid']
    quantity = request.POST['quantity']
    mealobj = Meal.objects.get(id=mealid)
    batch = Batch(meal = mealobj,quantity = quantity)
    batch.save()
    addtocart(request,batch)
    return HttpResponseRedirect(reverse('addmeal',kwargs={'id':id}))

@csrf_exempt
def addmeal(request,id):
    if str(request.user) == "AnonymousUser":
        return HttpResponseRedirect(reverse("login"))
    meal = Meal.objects.get(id=id)
    mealcategories = MealCategory.objects.filter(meal = meal)
    template = loader.get_template('addmeal.html')
    context = {
        'meal': meal,
        'mealcategories': mealcategories,
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
    
    print(categorylist)
    cgfilterlist = json.loads(cgfilterstr)


    #Remove all categorygroup categories from category list
    for cg in cgfilterlist:
        cgobj = CategoryGroup.objects.get(cgname=cg)
        cgcaregorylist = CategoryGroupCategory.objects.filter(cg=cgobj)
        for cgcaregory in cgcaregorylist:
            try:
                categorylist.remove(cgcaregory.c.cname)
            except:
                break

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
        if len(perfectmatch) == 1:
          index = 0;
        else:
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
        meal.append(str(mealc.meal.id))
        jsonmealist.append(meal)

        mealcategories =MealCategory.objects.filter(meal=mealc.meal)
        for mealcategory in mealcategories: 
            c =[]
            c.append(mealcategory.c.cname)
            c.append(mealcategory.c.cphoto)
            jsonmealist.append(c)
        jsonmealclist.append(jsonmealist)

    return JsonResponse(jsonmealclist,safe=False)