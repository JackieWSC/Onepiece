from django.contrib import admin

# Register your models here.
from django.contrib import admin
from restaurants.models import Restaurant, Food, Comment

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    search_fields = ('name',)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')
    list_filter = ('is_spicy',)
    fields = ('price','restaurant')
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'email', 'date_time', 'content')


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Comment, CommentAdmin)