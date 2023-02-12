from django.contrib import admin
from .models import Product, ImgProduct, Category, Subcategory, Basket, Brand, Status, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "price", "category", "subcategory","pub_date")
    search_fields = ["title",]
    list_filter = ["pub_date",]

class ImgProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "image", "product")
    search_fields = ["product",]
    list_filter = ["product",]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "image")
    search_fields = ["name",]

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "category", "image")
    search_fields = ["name",]

class BasketAdmin(admin.ModelAdmin):
    list_display = ("pk", "product", "pub_date")

class BrandAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")

class StatusAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "percent")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("pk", "product", "amount", "status", "price")

admin.site.register(Brand, BrandAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ImgProduct, ImgProductAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)