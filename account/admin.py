from django.contrib import admin

from account.models import Category, Post, PostImages

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostImages)
