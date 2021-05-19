from django.contrib import admin
from .models import Product, Search, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'name_seller', 'phone_number', 'url', 'search')


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'pages',)
