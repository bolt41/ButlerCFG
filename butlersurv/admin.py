from django.contrib import admin
from .models import SystemSurv, PartitionSurv, QuestionSurv, AnswerSurv

class SystemSurvAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_use')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class PartitionSurvAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_use')
    list_display_links = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'type')


class QuestionSurvAdmin(admin.ModelAdmin):
    list_display = ('question', 'partition', 'get_variable', 'is_use')
    list_display_links = ('question', 'partition')
    list_filter = ('partition',)
    search_fields = ('question', 'partition')


class AnswerSurvAdmin(admin.ModelAdmin):
    list_display = ('variable', 'get_partition', 'question', 'is_use')
    list_display_links = ('question', 'variable')
    list_filter = ('question__partition', 'question')
    search_fields = ('question', 'variable')

admin.site.register(SystemSurv, SystemSurvAdmin)
admin.site.register(PartitionSurv, PartitionSurvAdmin)
admin.site.register(QuestionSurv, QuestionSurvAdmin)
admin.site.register(AnswerSurv, AnswerSurvAdmin)


