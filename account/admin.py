from django.contrib import admin

from account.models import Category, Worker_card, Worker_cardImages, Location

from account.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(Worker_card)
admin.site.register(Category)
admin.site.register(Worker_cardImages)
admin.site.register(Location)
