from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import Group

from event_management.events.models import User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    model = User
    list_display = (
        "email",
        "is_staff",
    )
    list_filter = list_display
    readonly_fields = ["last_login", "email"]
    fieldsets = ((None, {"fields": ("email", "password", "is_staff")}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff"),
            },
        ),
    )
    search_fields = ("email",)
    filter_horizontal = ()
    ordering = ("email",)


admin.site.unregister(Group)
