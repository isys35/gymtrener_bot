from django.contrib import admin

from webhook.models import Category, Exersice, ExerciseUse, Set, State, View, Keyboard, ReplyButton


class ExersiceAdmin(admin.ModelAdmin):
    fields = ('title', 'category', 'description', 'image')


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'button', 'name_parameter', 'parent', 'view_id')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'function', 'new_state_id')


admin.site.register(Category)
admin.site.register(Exersice, ExersiceAdmin)
admin.site.register(ExerciseUse)
admin.site.register(Set)
admin.site.register(State, StateAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Keyboard)
admin.site.register(ReplyButton)