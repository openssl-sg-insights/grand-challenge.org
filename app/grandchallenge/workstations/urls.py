from django.urls import path

from grandchallenge.workstations.views import (
    SessionCreate,
    WorkstationCreate,
    WorkstationDetail,
    WorkstationEditorsUpdate,
    WorkstationImageCreate,
    WorkstationImageDetail,
    WorkstationImageUpdate,
    WorkstationList,
    WorkstationUpdate,
    WorkstationUsersUpdate,
)

app_name = "workstations"

urlpatterns = [
    path("", WorkstationList.as_view(), name="list"),
    path("create/", WorkstationCreate.as_view(), name="create"),
    # TODO - add region
    path(
        "sessions/create/",
        SessionCreate.as_view(),
        name="default-session-create",
    ),
    path(
        "<slug>/sessions/create/",
        SessionCreate.as_view(),
        name="workstation-session-create",
    ),
    path(
        "<slug>/editors/update/",
        WorkstationEditorsUpdate.as_view(),
        name="editors-update",
    ),
    path(
        "<slug>/users/update/",
        WorkstationUsersUpdate.as_view(),
        name="users-update",
    ),
    path("<slug>/", WorkstationDetail.as_view(), name="detail"),
    path("<slug>/update/", WorkstationUpdate.as_view(), name="update"),
    path(
        "<slug>/images/create/",
        WorkstationImageCreate.as_view(),
        name="image-create",
    ),
    path(
        "<slug>/images/<uuid:pk>/",
        WorkstationImageDetail.as_view(),
        name="image-detail",
    ),
    path(
        "<slug>/images/<uuid:pk>/update/",
        WorkstationImageUpdate.as_view(),
        name="image-update",
    ),
]
