from django.contrib import admin
from .models import Bike, Brand

# Register your models here.


class BikeAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'brand',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'frontend_name',
        'name',
    )


admin.site.register(Bike, BikeAdmin)
admin.site.register(Brand, BrandAdmin)
