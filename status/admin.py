from django.contrib import admin
from status.models import Status, Incident


class BaseAdmin(admin.ModelAdmin):

    """ Base module inherited by all other admin modules to save time setting various defaults. """

    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_on_top = True


class StatusAdmin(BaseAdmin):
    list_display = ['name', 'type', 'icon']


class IncidentAdmin(BaseAdmin):
    list_display = ['user', 'name', 'status', 'description']
    list_filter = ['user']


admin.site.register(Status, StatusAdmin)
admin.site.register(Incident, IncidentAdmin)
