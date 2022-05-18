from django.contrib import admin

from account.models import Category, Worker_card, Worker_cardImages, Location

admin.site.register(Worker_card)
admin.site.register(Category)
admin.site.register(Worker_cardImages)
admin.site.register(Location)
