from django.db import models

# Create your models here.

class Person(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30) 
    monday = models.CharField(max_length = 900, null = True)
    tuesday = models.CharField(max_length = 900, null = True) 
    wednesday = models.CharField(max_length = 900, null = True)
    thursday = models.CharField(max_length = 900, null = True)
    friday = models.CharField(max_length = 900, null = True) 
    fat = models.IntegerField(null = True)
    sodium = models.IntegerField(null = True)
    potassium = models.IntegerField(null = True)
    cholesterol = models.IntegerField(null = True)
    carbohydrates = models.IntegerField(null = True)
    fiber = models.IntegerField(null = True)
    sugar = models.IntegerField(null = True)

    def __str__(self):
        return self.username + " " + self.password
