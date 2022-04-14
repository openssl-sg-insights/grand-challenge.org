# Generated by Django 3.2.13 on 2022-04-13 09:45

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0015_auto_20220412_1038"),
        ("pages", "0003_historicalpage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalpage",
            old_name="title",
            new_name="slug",
        ),
        migrations.RenameField(
            model_name="page",
            old_name="title",
            new_name="slug",
        ),
        migrations.AlterField(
            model_name="historicalpage",
            name="display_title",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="page",
            name="display_title",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="historicalpage",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=64,
                populate_from="display_title",
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="slug",
            field=django_extensions.db.fields.AutoSlugField(
                blank=True,
                editable=False,
                max_length=64,
                populate_from="display_title",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="page",
            unique_together={("challenge", "slug")},
        ),
    ]
