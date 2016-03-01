from django.contrib import admin
from status.models import Status, Incident, IncidentUpdate


class BaseAdmin(admin.ModelAdmin):

    """ Base module inherited by all other admin modules to save time setting various defaults. """

    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_on_top = True


@admin.register(Status)
class StatusAdmin(BaseAdmin):
    list_display = ['pk', 'name', 'type', 'icon']


class IncidentUpdateInline(admin.TabularInline):
    model = IncidentUpdate


@admin.register(Incident)
class IncidentAdmin(BaseAdmin):
    list_display = ['pk', 'created', 'updated', 'user', 'name', 'hidden']
    list_filter = ['user', 'hidden']
    inlines = [IncidentUpdateInline, ]


@admin.register(IncidentUpdate)
class IncidentUpdateAdmin(BaseAdmin):
    list_display = ['pk', 'created', 'updated', 'incident', 'user', 'status', 'description']
    list_filter = ['user', 'status']
