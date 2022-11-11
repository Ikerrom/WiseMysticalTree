from django.contrib import admin
from wmtapp.models import *

admin.site.register(Category)
admin.site.register(CategoryGroup)
admin.site.register(CategoryGroupCategory)
admin.site.register(Meal)
admin.site.register(MealCategory)
admin.site.register(User)
admin.site.register(UserBatchCart)
admin.site.register(UserBatchHistory)
admin.site.register(Question)
admin.site.register(QuestionCategory)
admin.site.register(QuestionCategoryGroup)
# Register your models here.
