from django.contrib import admin

from grandchallenge.core.admin import (
    GroupObjectPermissionAdmin,
    UserObjectPermissionAdmin,
)
from grandchallenge.workstation_configs.models import (
    LookUpTable,
    WindowPreset,
    WorkstationConfig,
    WorkstationConfigGroupObjectPermission,
    WorkstationConfigUserObjectPermission,
)


class WorkstationConfigAdmin(admin.ModelAdmin):
    readonly_fields = ("creator",)


admin.site.register(WorkstationConfig, WorkstationConfigAdmin)
admin.site.register(
    WorkstationConfigUserObjectPermission, UserObjectPermissionAdmin
)
admin.site.register(
    WorkstationConfigGroupObjectPermission, GroupObjectPermissionAdmin
)
admin.site.register(WindowPreset)
admin.site.register(LookUpTable)
