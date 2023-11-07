from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Department, EmployeeProfile, Position, WorkingTime


class PositionAdmin(admin.TabularInline):
    model = EmployeeProfile.position.through
    extra = 1


class WorkplaceAdmin(admin.TabularInline):
    model = EmployeeProfile.workplace.through
    extra = 1


class WorkingTimeAdmin(admin.TabularInline):
    model = WorkingTime
    extra = 1


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date_hire",
        "current_leave",
    ]
    list_display_links = ["user"]
    list_filter = ["position", "workplace"]

    fieldsets = (
        (None, {"fields": ("user", "gender", "work_email")}),
        (
            _("Employment Details"),
            {
                "fields": (
                    "date_hire",
                    "contract_end",
                    "additional_info",
                )
            },
        ),
        (
            _("Leave Entitlement"),
            {
                "fields": (
                    "annual_leave",
                    "current_leave",
                )
            },
        ),
        (
            _("API content permissions"),
            {
                "fields": (
                    "is_manager",
                )
            },
        ),
    )
    inlines = (WorkplaceAdmin, PositionAdmin, WorkingTimeAdmin)


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(WorkingTime)
admin.site.register(Position)
admin.site.register(Department)
