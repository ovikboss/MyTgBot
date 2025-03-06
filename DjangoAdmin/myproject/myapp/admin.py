from django.contrib import admin


from .models import User, FoodEntry, Recipe

admin.site.register(User)
admin.site.register(FoodEntry)
admin.site.register(Recipe)
# Register your models here.
