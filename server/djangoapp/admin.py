# djangoapp/admin.py

from django.contrib import admin
from .models import CarMake, CarModel

# Define CarModelInline for managing CarModel and CarMake together
class CarModelInline(admin.TabularInline):
    model = CarModel

# Register CarModel model with CarModelInline
admin.site.register(CarModel)

# Register CarMake model with CarMakeAdmin
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)




