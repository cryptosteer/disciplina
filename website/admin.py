from django.contrib import admin
from .models import Settings, HabitFrecuency
from sitetree.admin import TreeItemAdmin, override_item_admin


class CustomTreeItemAdmin(TreeItemAdmin):
    fieldsets = (
        (('Basic settings'), {
            'fields': ('parent', 'title', 'urlaspattern', 'url', 'icon', )
        }),
        (('Access settings'), {
            'classes': ('collapse',),
            'fields': ('access_loggedin', 'access_guest',
                       'access_restricted', 'access_permissions',
                       'access_perm_type')
        }),
        (('Display settings'), {
            'classes': ('collapse',),
            'fields': ('hidden', 'inmenu', 'inbreadcrumbs', 'insitetree')
        }),
        (('Additional settings'), {
            'classes': ('collapse',),
            'fields': ('hint', 'description', 'alias')
        }),
    )

admin.site.register(Settings)
admin.site.register(HabitFrecuency)
override_item_admin(CustomTreeItemAdmin)
