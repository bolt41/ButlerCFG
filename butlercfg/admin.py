from django.contrib import admin
from .models import Floor, Levels, Rooms, Systems, Params, Templates, Vendors, Devices, Constant


class ParamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')
    list_display_links = ('name', 'system')
    list_filter = ('system',)
    search_fields = ('name', 'system')


class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('room', 'get_system', 'param', 'count')
    list_display_links = ('room', 'param')
    list_filter = ('room',)
    search_fields = ('room', 'param')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'model', 'caption', 'get_levels', 'system', 'price')
    list_display_links = ('vendor', 'model', 'caption')
    list_filter = ('level', 'system', 'vendor')

class ConstantAdmin(admin.ModelAdmin):
    list_display = ('name', 'caption', 'value')


admin.site.register(Rooms)
admin.site.register(Systems)
admin.site.register(Floor)
admin.site.register(Levels)
admin.site.register(Params, ParamsAdmin)
admin.site.register(Templates, TemplatesAdmin)
admin.site.register(Vendors)
admin.site.register(Devices, DeviceAdmin)
admin.site.register(Constant, ConstantAdmin)
