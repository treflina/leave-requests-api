from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["last_name", "first_name"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = get_user_model()

    list_display = [
        "last_name",
        "first_name",
        "additional_identifier",
        "is_active",
        "is_staff",
    ]

    list_display_links = ["last_name", "first_name", "is_active"]

    list_filter = ["is_active", "is_staff"]

    readonly_fields = ["last_login"]

    fieldsets = (
        (_("Login Credentials"), {"fields": ("username", "password")}),
        (
            _("Basic Info"),
            {"fields": ("first_name", "last_name", "additional_identifier", "email")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "additional_identifier",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "additional_identifier",
    ]


admin.site.register(User, UserAdmin)
