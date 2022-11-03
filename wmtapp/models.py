from pyexpat import model
from django.db import models

class Category(models.Model):
    categoryname = models.CharField(max_length=255)
    categoryphoto = models.CharField(max_length=255)

class Intolerance(models.Model):
    intolerancename = models.CharField(max_length=255)
    intolerancephoto = models.CharField(max_length=255)

class IntoleranceCategory(models.Model):
    intolerance = models.ForeignKey(Intolerance, on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

class Meal(models.Model):
    mealname = models.CharField(max_length=255)
    mealdesc = models.TextField()
    price = models.FloatField()
    mealphoto = models.CharField(max_length=255,null = True)
    discount = models.FloatField(null = True)

class MealCategory(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

class User(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    userphoto = models.CharField(max_length=255, null = True)

class UserMealCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)

class UserMealHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)

class Question(models.Model):
    question = models.TextField()
    priority = models.IntegerField()

class QuestionCategory():
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

class QuestionIntolerance():
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    intolerance = models.ForeignKey(Intolerance,on_delete=models.PROTECT)