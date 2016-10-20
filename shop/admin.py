# -*- encoding: UTF-8 -*-
from django.contrib import admin

from shop import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ['name']


class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0
    fields = ('product', 'customer', 'text')
    readonly_fields = ['product', 'customer', 'text']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
    inlines = [CommentInline]


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'price', 'get_categories')
    fields = ['name', 'content', 'price', 'categories']
    filter_horizontal = ("categories",)

    inlines = [ProductImageInline, CommentInline]


class CartItemInline(admin.StackedInline):
    model = models.CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status')
    fields = ['customer', 'status']
    readonly_fields = ['customer']
    inlines = [CartItemInline]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('cart', 'customer')
    fields = ['cart', 'customer']
    readonly_fields = ['cart', 'customer']


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Order, OrderAdmin)
