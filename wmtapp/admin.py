from django.contrib import admin
from wmtapp.models import *

admin.site.register(Category)
admin.site.register(Intolerance)
admin.site.register(IntoleranceCategory)
admin.site.register(Meal)
admin.site.register(MealCategory)
admin.site.register(User)
admin.site.register(UserMealCart)
admin.site.register(UserMealHistory)
admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(QuestionIntolerance)
# Register your models here.
