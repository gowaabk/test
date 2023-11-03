from django.contrib import admin
from .models import Recipe, Category, CoockingItem

# Register your models here.


admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(CoockingItem)
