from django.contrib import admin

from webhook.models import Category, Exersice, ExerciseUse, Set


class ExersiceAdmin(admin.ModelAdmin):
    fields = ('title', 'category', 'description', 'image')


admin.site.register(Category)
admin.site.register(Exersice, ExersiceAdmin)
admin.site.register(ExerciseUse)
admin.site.register(Set)