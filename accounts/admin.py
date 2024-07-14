from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username",]
    list_filter = ["username",]
    fieldsets = (
        (None, {"fields": ("username", "password", )}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )

    add_fieldsets = (
        (None, {"fields": ("username", "password", "password2", )}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )

    search_fields = ["username", ]

    ordering = ["username"]
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
