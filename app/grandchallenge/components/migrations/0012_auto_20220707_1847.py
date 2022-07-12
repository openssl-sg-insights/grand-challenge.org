# Generated by Django 3.2.14 on 2022-07-07 18:47

import django.db.models.deletion
from django.db import migrations, models

import grandchallenge.core.validators


class Migration(migrations.Migration):

    dependencies = [
        (
            "workstation_configs",
            "0016_alter_workstationconfig_overlay_segments",
        ),
        ("components", "0011_auto_20220610_1020"),
    ]

    operations = [
        migrations.AddField(
            model_name="componentinterface",
            name="look_up_table",
            field=models.ForeignKey(
                blank=True,
                help_text="The look-up table that is applied when an overlay image is first shown",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="workstation_configs.lookuptable",
            ),
        ),
        migrations.AddField(
            model_name="componentinterface",
            name="overlay_segments",
            field=models.JSONField(
                blank=True,
                default=None,
                help_text="The schema that defines how categories of values in the overlay images are differentiated.",
                null=True,
                validators=[
                    grandchallenge.core.validators.JSONValidator(
                        schema={
                            "$id": "http://example.com/example.json",
                            "$schema": "http://json-schema.org/draft-06/schema",
                            "description": "Define the overlay segments for the LUT.",
                            "items": {
                                "$id": "#/items",
                                "additionalProperties": False,
                                "default": {},
                                "description": "Defines what each segment of the LUT represents.",
                                "examples": [
                                    {
                                        "metric_template": "{{metrics.volumes[0]}} mm³",
                                        "name": "Metastasis",
                                        "visible": True,
                                        "voxel_value": 1,
                                    }
                                ],
                                "maxItems": 32,
                                "properties": {
                                    "metric_template": {
                                        "$id": "#/items/properties/metric_template",
                                        "default": "",
                                        "description": "The jinja template to determine which property from the results.json should be used as the label text.",
                                        "examples": [
                                            "{{metrics.volumes[0]}} mm³"
                                        ],
                                        "title": "The Metric Template Schema",
                                        "type": "string",
                                    },
                                    "name": {
                                        "$id": "#/items/properties/name",
                                        "default": "",
                                        "description": "What this segment should be called.",
                                        "examples": ["Metastasis"],
                                        "title": "The Name Schema",
                                        "type": "string",
                                    },
                                    "visible": {
                                        "$id": "#/items/properties/visible",
                                        "default": True,
                                        "description": "Whether this segment is visible by default.",
                                        "examples": [True],
                                        "title": "The Visible Schema",
                                        "type": "boolean",
                                    },
                                    "voxel_value": {
                                        "$id": "#/items/properties/voxel_value",
                                        "default": 0,
                                        "description": "The value of the LUT for this segment.",
                                        "examples": [1],
                                        "title": "The Voxel Value Schema",
                                        "type": "integer",
                                    },
                                },
                                "required": ["voxel_value", "name", "visible"],
                                "title": "The Segment Schema",
                                "type": "object",
                            },
                            "title": "The Overlay Segments Schema",
                            "type": "array",
                        }
                    )
                ],
            ),
        ),
    ]
