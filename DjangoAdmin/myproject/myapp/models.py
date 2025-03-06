from email.policy import default

from django.db import models
from django.utils import timezone



class User(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    subscription = models.DateTimeField(default=timezone.now)
    login = models.CharField(max_length=255)
    current_weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField()
    is_male = models.BooleanField(default=True)
    activity_level = models.FloatField()
    daily_message = models.BooleanField(default=False)
    breakfast_time = models.TimeField(default='08:00')  # Default 8:00 AM
    lunch_time = models.TimeField(default='13:00')  # Default 1:00 PM
    dinner_time = models.TimeField(default='19:00')  # Default 7:00 PM

    def __str__(self):
        return f"<User(id='{self.id}', name='{self.name}', subscription={self.subscription}, login='{self.login}')>"

    class Meta:
        db_table = 'users'


class FoodEntry(models.Model):
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_entries')

    def __str__(self):
        return f"<FoodEntry(name='{self.name}', calories={self.calories}, timestamp='{self.timestamp}')>"

    class Meta:
        db_table = 'food_entries'


class Recipe(models.Model):
    meal_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    text = models.TextField()

    def __str__(self):
        return f"Рецепт: {self.name}\nНа {self.calories} ккал\n{self.text}"

    class Meta:
        db_table = 'resipes'