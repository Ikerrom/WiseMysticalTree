from django.db import models

class Category(models.Model):
    categoryname = models.CharField(max_length=255)
    categoryphoto = models.CharField(max_length=255)

class Intolerances(models.Model):
    intolerancename = models.CharField(max_length=255)
    intolerancephoto = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)

class Meal(models.Model):
    mealname = models.CharField(max_length=255)
    mealdesc = models.TextField()
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    mealphoto = models.CharField(max_length=255,null = True)
    discount = models.FloatField(null = True)

class User(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    userphoto = models.CharField(max_length=255, null = True)
    cart = models.ManyToManyField(Meal)
    history = models.ManyToManyField(Meal)

class Question(models.Model):
    question = models.TextField()
    questioncategory = models.ManyToManyField(Category)
    yes = models.ManyToManyField(Intolerances, null = True)
    no = models.ManyToManyField(Intolerances, null = True)