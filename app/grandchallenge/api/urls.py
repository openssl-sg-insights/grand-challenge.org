from django.conf.urls import url, include
from rest_framework import routers

from grandchallenge.api.views import (
    ResultViewSet, SubmissionViewSet, JobViewSet, MethodViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'results', ResultViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'methods', MethodViewSet)
urlpatterns = [
    # Do not namespace the router.urls without updating the view names in
    # evaluation.serializers
    url(r'^v1/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
