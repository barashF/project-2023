from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "author", "pub_date")
    search_fields = ["title",]
    list_filter = ["pub_date",]
admin.site.register(Post, PostAdmin)
# Register your models here.
