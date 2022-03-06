from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'avatarURL']

    fieldsets = (
        # None is title for section
        (None, {
            "fields": (
                'email', 'password'
            ),
        }),
        # if only one field, need to add coma
        (_('Personal Info'), {'fields': ('name', 'avatarURL')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'name', 'password1', 'password2', 'avatarURL')
        }),
    )


admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.Tweet)