from django.contrib import admin
from donaterinventory import models

# Register your models here.
admin.site.register(models.Restaurant)
admin.site.register(models.Dish)
admin.site.register(models.RestaurantReview)