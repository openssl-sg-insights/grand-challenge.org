# Generated by Django 3.1.6 on 2021-03-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algorithms", "0004_algorithm_social_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="average_duration",
            field=models.DurationField(
                default=None,
                editable=False,
                help_text="The average duration of successful jobs.",
                null=True,
            ),
        ),
    ]