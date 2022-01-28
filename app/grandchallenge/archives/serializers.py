from rest_framework import serializers
from rest_framework.fields import ReadOnlyField, URLField
from rest_framework.relations import HyperlinkedRelatedField

from grandchallenge.archives.models import Archive, ArchiveItem
from grandchallenge.components.serializers import (
    ComponentInterfaceValueSerializer,
)


class ArchiveItemSerializer(serializers.ModelSerializer):
    archive = HyperlinkedRelatedField(
        read_only=True, view_name="api:archive-detail",
    )
    values = ComponentInterfaceValueSerializer(many=True)

    class Meta:
        model = ArchiveItem
        fields = (
            "id",
            "archive",
            "values",
        )


class ArchiveSerializer(serializers.ModelSerializer):
    algorithms = HyperlinkedRelatedField(
        read_only=True, many=True, view_name="api:algorithm-detail"
    )
    logo = URLField(source="logo.x20.url", read_only=True)
    url = URLField(source="get_absolute_url", read_only=True)
    # Include the read only name for legacy clients
    name = ReadOnlyField()

    class Meta:
        model = Archive
        fields = (
            "id",
            "name",
            "title",
            "algorithms",
            "logo",
            "description",
            "api_url",
            "url",
        )
