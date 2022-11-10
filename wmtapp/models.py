from pyexpat import model
from django.db import models
from django.contrib.auth.models import User as djangouser

class Category(models.Model):
    cname = models.CharField(max_length=255)
    cphoto = models.CharField(max_length=255)
    def __str__(self):
        return u'%s'%self.cname

class CategoryGroup(models.Model):
    cgname = models.CharField(max_length=255)
    cgphoto = models.CharField(max_length=255)
    def __str__(self):
        return u'%s'%self.cgname

class CategoryGroupCategory(models.Model):
    cg = models.ForeignKey(CategoryGroup, on_delete=models.PROTECT)
    c = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.cg

class Meal(models.Model):
    mealname = models.CharField(max_length=255)
    mealdesc = models.TextField()
    mealphoto = models.CharField(max_length=255,null = True)
    price = models.FloatField()
    discount = models.FloatField(null = True)
    def __str__(self):
        return u'%s'%self.mealname

class MealCategory(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.PROTECT)
    c = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.meal

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
    preference = models.BooleanField(default = False)
    def __str__(self):
        return u'%s'%self.question

class QuestionCategory(models.Model):
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    c = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return u'%s'%self.question

class QuestionCategoryGroup(models.Model):
    question = models.ForeignKey(Question,on_delete=models.PROTECT)
    cg = models.ForeignKey(CategoryGroup,on_delete=models.PROTECT, null = True)
    def __str__(self):
        return u'%s'%self.question