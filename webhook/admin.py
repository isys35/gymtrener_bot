from django.contrib import admin

from webhook.models import Category, Exersice


class ExersiceAdmin(admin.ModelAdmin):
    fields = ('title', 'category', 'description', 'image')


admin.site.register(Category)
admin.site.register(Exersice, ExersiceAdmin)
