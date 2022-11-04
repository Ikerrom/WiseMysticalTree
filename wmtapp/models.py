from pyexpat import model
from django.db import models
from django.contrib.auth.models import User as djangouser

class Category(models.Model):
    categoryname = models.CharField(max_length=255)
    categoryphoto = models.CharField(max_length=255)
    def __str__(self):
        return u'%s'%self.categoryname

class Intolerance(models.Model):
    intolerancename = models.CharField(max_length=255)
    intolerancephoto = models.CharField(max_length=255)
    def __str__(self):
        return u'%s'%self.intolerancename

class IntoleranceCategory(models.Model):
    intolerance = models.ForeignKey(Intolerance, on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.category

class Meal(models.Model):
    mealname = models.CharField(max_length=255)
    mealdesc = models.TextField()
    price = models.FloatField()
    mealphoto = models.CharField(max_length=255,null = True)
    discount = models.FloatField(null = True)
    def __str__(self):
        return u'%s'%self.mealname

class MealCategory(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.category

class User(models.Model):
    uid = models.ForeignKey(djangouser,on_delete=models.PROTECT, null = True)
    userphoto = models.CharField(max_length=255, null = True)
    def __str__(self):
        return u'%s'%self.uid

class UserMealCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.meal

class UserMealHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.meal

class Question(models.Model):
    question = models.TextField()
    priority = models.IntegerField()
    def __str__(self):
        return u'%s'%self.question

class QuestionCategory(models.Model):
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.category

class QuestionIntolerance(models.Model):
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    intolerance = models.ForeignKey(Intolerance,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.intolerance